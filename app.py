import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 설정 ---
# ⚠️ 주의: 반드시 아래 따옴표 안의 한글을 지우고 본인의 시트 ID만 넣으세요.
SHEET_ID = "여기에_본인의_시트_ID만_복사해서_넣으세요" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard", layout="wide")

@st.cache_data(ttl=30) # 30초마다 데이터 갱신
def load_data_from_sheets():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return None
        
        df = pd.read_csv(io.StringIO(response.text))
        
        # [보완] 시트 제목 줄에 앞뒤 공백이 있어도 인식하게 만듭니다.
        df.columns = [c.strip() for c in df.columns]
        
        if 'key' not in df.columns or 'value' not in df.columns:
            st.error("시트의 제목(1행)이 정확히 'key'와 'value'인지 확인해 주세요.")
            return None
        
        # [보완] 내용물(key)에 공백이 섞여 있어도 자동으로 제거합니다.
        df['key'] = df['key'].astype(str).str.strip()
        
        return df.set_index('key')['value'].to_dict()
    except Exception as e:
        st.error(f"데이터 연결 중 오류: {e}")
        return None

raw_data = load_data_from_sheets()

# 데이터 로드 성공 시 화면을 그립니다.
if raw_data:
    # --- [2] CSS 디자인 ---
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
        <p style="margin:0; opacity:0.8;">스프레드시트 데이터 연동 중 (업데이트: {datetime.now().strftime('%H:%M:%S')})</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [4] 주요 KPI 카드 (KeyError 방지 로직) ---
    k1, k2, k3, k4 = st.columns(4)
    
    # .get()을 사용해 해당 값이 없으면 0이나 문구를 대신 출력합니다.
    kpis = [
        (k1, "전체 모멘텀", f"{raw_data.get('momentum', '0')}%"),
        (k2, "지역 편차", f"{raw_data.get('deviation', '0')}%"),
        (k3, "MZ 도달율", f"{raw_data.get('mz_reach', '0')}%"),
        (k4, "NPS 점수", raw_data.get('nps', '0'))
    ]

    for col, lab, val in kpis:
        col.markdown(f"""
        <div class="report-card">
            <p class="kpi-label">{lab}</p>
            <p class="kpi-value">{val}</p>
        </div>
        """, unsafe_allow_html=True)

    # --- [5] 차트 및 제언 섹션 ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="report-card"><h3>채널별 판매 성과</h3>', unsafe_allow_html
