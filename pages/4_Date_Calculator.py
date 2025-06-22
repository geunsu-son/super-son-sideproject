import streamlit as st
import pandas as pd
import datetime
from modules.streamlit_utils import sidebar_info

st.set_page_config(
    page_title="Date Calculator",
    page_icon="🗓",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    sidebar_info()
    st.divider()

st.title("Date Calculator")
st.write(
    """
D-day 등을 계산할 수 있는 계산기입니다.
"""
)
st.divider()

# 1. 오늘 날짜 가져오기
today = datetime.date.today()
st.write(f"**오늘 날짜:** {today.strftime('%Y-%m-%d')}")

# 2. 날짜 더하기/빼기
st.subheader("날짜 더하기/빼기")
days_delta = st.number_input("며칠을 더하거나 뺄까요? (음수 입력 시 빼기)", value=0, step=1)
calc_date = today + datetime.timedelta(days=days_delta)
st.write(f"계산된 날짜: **{calc_date.strftime('%Y-%m-%d')}**")

st.divider()

# 3. D-day 계산
st.subheader("D-day 계산기")
target_date = st.date_input("목표 날짜를 선택하세요", value=today)
d_day = (target_date - today).days
if d_day > 0:
    st.write(f"D-{d_day}")
elif d_day == 0:
    st.write("D-day!")
else:
    st.write(f"D+{abs(d_day)} (이미 지남)")

st.divider()

# 추가 기능: 두 날짜 사이의 일수 계산
st.subheader("두 날짜 사이의 일수 계산")
start_date = st.date_input("시작 날짜", value=today, key="start")
end_date = st.date_input("종료 날짜", value=today, key="end")
diff_days = (end_date - start_date).days
st.write(f"총 {diff_days}일 차이")
