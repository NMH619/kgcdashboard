import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 설정 ---
# ⚠️ 주의: 반드시 아래 따옴표 안의 한글을 지우고 본인의 시트 ID(영문+숫자 조합)만 넣으세요.
SHEET_ID = "여기에_본인의_시트_ID만_복사해서_넣으세요" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard", layout="wide")

@st.cache_data(ttl=60) # 1분 동안 데이터를 캐시하여 성능을 높입니다.
def load_data_from_sheets():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return None
        
        df = pd.read_csv(io.StringIO(response.text))
        # 'key' 열을 인덱스로 만들고 'value' 값을 가져와 딕셔너리로 변환
        return df.set_index('key')['value'].to_dict()
    except Exception:
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
        <p style="margin:0; opacity:0.8;">실시간 시트 연동 중 (업데이트: {datetime.now().strftime('%H:%M:%S')})</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [4] 주요 KPI 카드 (데이터 안전하게 불러오기) ---
    k1, k2, k3, k4 = st.columns(4)
    
    # 데이터가 없을 경우를 대비해 기본값(0) 설정
    momentum = raw_data.get('momentum', 0)
    deviation = raw_data.get('deviation', 0)
    mz_reach = raw_data.get('mz_reach', 0)
    nps = raw_data.get('nps', 0)

    kpis = [
        (k1, "전체 모멘텀", f"{momentum}%"),
        (k2, "지역 편차", f"{deviation}%"),
        (k3, "MZ 도달율", f"{mz_reach}%"),
        (k4, "NPS 점수", nps)
    ]

    for col, lab, val in kpis:
