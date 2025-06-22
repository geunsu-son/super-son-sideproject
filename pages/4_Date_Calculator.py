import streamlit as st
import datetime
from korean_lunar_calendar import KoreanLunarCalendar
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
    다양한 날짜 계산 기능을 제공합니다:
    - 원하는 날짜 기준으로 날짜 더하기/빼기
    - D-day 계산
    - 양력 ↔ 음력 변환
    - 두 날짜 사이의 일수 계산
    """
)
st.divider()

today = datetime.date.today()

# 날짜 계산기 섹션 (기준 날짜 + 날짜 더하기/빼기)
st.subheader("📅 날짜 계산기")
st.write("기준 날짜를 선택하고, 원하는 단위로 날짜를 더하거나 뺄 수 있습니다.")
col1, col2, col3 = st.columns(3)

delta_unit = "일"  # 기본 단위
with col1:
    base_date = st.date_input("기준 날짜를 선택해주세요", value=today)
with col2:
    delta_value = st.number_input(f"몇 {delta_unit}을 더하거나 뺄까요? (음수 입력 시 빼기)", value=7, step=1)
with col3:
    delta_unit = st.selectbox("단위 선택", ["일", "주", "개월", "년"])

if delta_unit == "일":
    calc_date = base_date + datetime.timedelta(days=delta_value)
elif delta_unit == "주":
    calc_date = base_date + datetime.timedelta(weeks=delta_value)
elif delta_unit == "개월":
    month = base_date.month + delta_value
    year = base_date.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    day = min(base_date.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    try:
        calc_date = datetime.date(year, month, day)
    except:
        calc_date = base_date
elif delta_unit == "년":
    try:
        calc_date = datetime.date(base_date.year + delta_value, base_date.month, base_date.day)
    except:
        calc_date = base_date

st.success(f"🗓 계산된 날짜: **{calc_date.strftime('%Y-%m-%d')}**")
st.divider()

# D-day 계산기
st.subheader("📌 D-day 계산기")
st.write("목표 날짜와 기준 날짜를 설정하여 D-day를 계산합니다.")
include_today = st.checkbox("당일 포함", value=False)
col1, col2 = st.columns(2)
with col1:
    base_date = st.date_input("기준 날짜 선택", value=today, key="base_date")
with col2:
    default_start = base_date + datetime.timedelta(days=30)
    gap_date = st.date_input(label="목표 날짜를 선택해주세요 (기본값: 기준 날짜 + 30일)",value=(today+ datetime.timedelta(days=30)), key="gap_date")

d_day = (gap_date - base_date).days + (1 if include_today else 0)
if d_day > 0:
    st.success(f"⏳ D-{d_day}")
elif d_day == 0:
    st.success("🎉 D-day!")
else:
    st.info(f"📅 D+{abs(d_day)} (이미 지남)")
st.divider()


# 양력 ↔ 음력 변환기
st.subheader("🔄 양력 ↔ 음력 변환기")
st.write("양력과 음력 날짜를 상호 변환할 수 있습니다.")
col1, col2 = st.columns(2)
with col1:
    st.warning("음력 → 양력")
    lunar_input = st.date_input("음력 날짜 (YYYY-MM-DD)", value=default_start)
    try:
        y, m, d = map(int, str(lunar_input).split("-"))
        cal = KoreanLunarCalendar()
        cal.setLunarDate(y, m, d, False)
        solar = cal.LunarIsoFormat()
        st.success(f"📆 양력 날짜: **{solar}**")
    except Exception as e:
        st.warning(f"음력 날짜 입력을 확인해주세요 (YYYY-MM-DD) - {e}")
with col2:
    st.warning("양력 → 음력")
    solar_input = st.date_input("양력 날짜 (YYYY-MM-DD)", value=default_start)
    try:
        y, m, d = map(int, str(solar_input).split("-"))
        cal = KoreanLunarCalendar()
        cal.setSolarDate(y, m, d)
        lunar = cal.LunarIsoFormat()
        st.success(f"🌙 음력 날짜: **{lunar}**")
    except Exception as e:
        st.warning(f"양력 날짜 입력을 확인해주세요 (YYYY-MM-DD) - {e}")
st.divider()

# 두 날짜 간 차이 계산
st.subheader("📏 두 날짜 사이의 일수 계산")
st.write("두 날짜 사이의 일수를 계산합니다.")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("시작 날짜", value=today, key="start")
with col2:
    end_date = st.date_input("종료 날짜", value=(today + datetime.timedelta(days=7)), key="end")
diff_days = (end_date - start_date).days
st.success(f"📐 총 **{diff_days}일** 차이")
st.divider()
