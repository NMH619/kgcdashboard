import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 ID 설정 ---
# 본인의 구글 시트 주소창에서 ID 부분만 복사해서 아래 따옴표 안에 넣으세요.
SHEET_ID = "여기에_본인의_시트_ID만_복사해서_넣으세요" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard", layout="wide")

@st.cache_data(ttl=60) # 1분마다 데이터를 새로고침합니다.
def load_data_from_sheets():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8' # 한글 깨짐 방지
        if response.status_code != 200:
            st.error("시트 ID를 확인하거나 공유 설정을 '링크가 있는 모든 사용자'로 바꿔주세요.")
            return None
        df = pd.read_csv(io.StringIO(response.text))
        # key 열을 인덱스로 설정하여 딕셔너리로 변환
        return df.set_index('key')['value'].to_dict()
    except Exception as e:
        st.error(f"데이터 로딩 실패: {e}")
        return None

raw_data = load_sheet_data = load_data_from_sheets()

# 데이터 로드 성공 시에만 화면을 그립니다.
if raw_data:
    # --- [2] CSS 스타일 (끊겼던 부분 수정 완료) ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
        * { font-family: 'Pretendard', sans-serif; }
        .report-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 1rem; }
        .header-box { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem; }
        .kpi-value { font-size: 2rem; font-weight: 900; color: #1a202c; margin: 0; }
        .kpi-label { font-size: 0.85rem; font-weight: 700; color: #718096; margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

    # --- [3] 상단 헤더 ---
    st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.2rem;">주간 마케팅 통찰 보고서</h1>
        <p style="margin:0; opacity:0.8;">실시간 시트 연동 중 (업데이트: {datetime.now().strftime('%H:%M:%S')})</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [4] 주요 지표 (KPI) ---
    k1,
