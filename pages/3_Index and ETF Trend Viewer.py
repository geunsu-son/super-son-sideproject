import streamlit as st
import pandas as pd
import yfinance as yf
import altair as alt

st.set_page_config(
    page_title="Index and ETF Trend Viewer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.write(
    """
    ### 연락처
    📞 Tel. 010-4430-2279  
    📩 E-mail. [gnsu0705@gmail.com](gnsu0705@gmail.com)  
    💻 Blog. [Super-Son](https://super-son.tistory.com/)  
    😎 Resume. [Super-Son](https://super-son-resume.streamlit.app)
    """
    )
    st.divider()
    # Slider for selecting time period in months
    months = st.slider('Select Time Period (months)', 1, 12, 6)

st.title('Index and ETF Trend Viewer')
st.write("""
나스닥, S&P 500 지수의 20일 이동평균 선 그래프를 제공하는 사이트를 찾지 못해 제가 사용하기 위해 직접 제작했습니다.  
보고 싶은 지수나 상품에 대한 그래프를 그리도록 제작했으며, 20일, 60일, 120일 이동평균 선을 기준으로 거래가격이 맞춰지면 사이드바에 알림이 표시됩니다.
""")
st.divider()

# Calculate the date for 1 year and 6 months ago from today
end_date = pd.Timestamp.today()
start_date = end_date - pd.DateOffset(months=18)

# Fetch data for NASDAQ and S&P 500 once
@st.cache_data(show_spinner="Loading Data...")
def fetch_data(ticker):
    with st.spinner(f'Please wait...Loading {ticker}'):
        # Retrieve stock data
        stock = yf.Ticker(ticker)
        history = stock.history(period="1y", interval="1d")
        data = pd.DataFrame(history)
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')  # Convert date to string format
        return data

nasdaq_data = fetch_data('^IXIC')
sp500_data = fetch_data('^GSPC')
soxl_data = fetch_data('SOXL')
usd_data = fetch_data('USD')
voo_data = fetch_data('VOO')
cony_data = fetch_data('CONY')


# Function to create moving average
def add_moving_averages(data):
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['MA_60'] = data['Close'].rolling(window=60).mean()
    data['MA_120'] = data['Close'].rolling(window=120).mean()
    return data

nasdaq_data = add_moving_averages(nasdaq_data)
sp500_data = add_moving_averages(sp500_data)
soxl_data = add_moving_averages(soxl_data)
usd_data = add_moving_averages(usd_data)
voo_data = add_moving_averages(voo_data)
cony_data = add_moving_averages(cony_data)


# Sidebar with last day 'Low' price comparison
def check_low_vs_moving_averages(data, name):
    last_row = data.iloc[-1]
    low_price = last_row['Low']
    ma20 = last_row['MA_20']
    ma60 = last_row['MA_60']
    ma120 = last_row['MA_120']

    if low_price < ma120:
        st.sidebar.info(f'''
### {name} - Last Day Low Price Check
120일 이동평균보다 낮은 가격에 거래한 기록이 있어요!
''')
    elif low_price < ma60:
        st.sidebar.info(f'''
### {name} - Last Day Low Price Check
60일 이동평균보다 낮은 가격에 거래한 기록이 있어요!
''')
    elif low_price < ma20:
        st.sidebar.info(f'''
### {name} - Last Day Low Price Check
20일 이동평균보다 낮은 가격에 거래한 기록이 있어요!
''')
    elif low_price*.99 < ma20:
        st.sidebar.info(f'''
### {name} - Last Day Low Price Check
가격이 1% 낮아지면 20일 이동평균보다 가격이 낮아져요!
''')

check_low_vs_moving_averages(nasdaq_data, 'NASDAQ')
check_low_vs_moving_averages(sp500_data, 'S&P 500')
check_low_vs_moving_averages(soxl_data, 'SOXL')
check_low_vs_moving_averages(usd_data, 'USD')
check_low_vs_moving_averages(voo_data, 'VOO')
check_low_vs_moving_averages(cony_data, 'CONY')

# Function to filter data based on the selected period
def filter_data(data, months):
    start_filter_date = end_date - pd.DateOffset(months=months)
    filtered_data = data[data['Date'] >= start_filter_date.strftime('%Y-%m-%d')]
    return filtered_data

nasdaq_data_filtered = filter_data(nasdaq_data, months)
sp500_data_filtered = filter_data(sp500_data, months)
soxl_data_filtered = filter_data(soxl_data, months)
usd_data_filtered = filter_data(usd_data, months)
voo_data_filtered = filter_data(voo_data, months)
cony_data_filtered = filter_data(cony_data, months)

# Function to create candlestick chart with moving averages
def create_candlestick_chart(data):
    base = alt.Chart(data).encode(
        alt.X('Date:T', title='Date')  # Date column is now in string format
    )

    open_close_color = alt.condition(
        "datum.Open <= datum.Close",
        alt.value("#FF0000"),  # Red for increasing
        alt.value("#0000FF")   # Blue for decreasing
    )

    rule = base.mark_rule().encode(
        alt.Y('Low:Q', scale=alt.Scale(zero=False)),
        alt.Y2('High:Q'),
        color=open_close_color
    )

    bar = base.mark_bar().encode(
        alt.Y('Open:Q'),
        alt.Y2('Close:Q'),
        color=open_close_color
    )

    ma20 = base.mark_line(color='orange').encode(
        alt.Y('MA_20:Q', title='Price')
    )

    ma60 = base.mark_line(color='green').encode(
        alt.Y('MA_60:Q', title='Price')
    )

    ma120 = base.mark_line(color='brown').encode(
        alt.Y('MA_120:Q', title='Price')
    )

    chart = (rule + bar + ma20 + ma60 + ma120).properties(
        width=800,
        height=400,
    )

    return chart

# Create and display charts
col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader('NASDAQ Index')
    nasdaq_chart = create_candlestick_chart(nasdaq_data_filtered)
    st.altair_chart(nasdaq_chart, use_container_width=True)

with col2:
    st.subheader('S&P 500 Index')
    sp500_chart = create_candlestick_chart(sp500_data_filtered)
    st.altair_chart(sp500_chart, use_container_width=True)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader('SOXL ETF')
    soxl_chart = create_candlestick_chart(soxl_data_filtered)
    st.altair_chart(soxl_chart, use_container_width=True)

with col2:
    st.subheader('USD ETF')
    usd_chart = create_candlestick_chart(usd_data_filtered)
    st.altair_chart(usd_chart, use_container_width=True)
    
col1, col2 = st.columns(2, gap="large")
with col1:
    st.subheader('VOO ETF')
    voo_chart = create_candlestick_chart(voo_data_filtered)
    st.altair_chart(voo_chart, use_container_width=True)

with col2:
    st.subheader('CONY ETF')
    cony_chart = create_candlestick_chart(cony_data_filtered)
    st.altair_chart(cony_chart, use_container_width=True)