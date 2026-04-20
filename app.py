import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 ID 설정 ---
# ⚠️ 주의: 아래 "여기에_본인의_시트_ID만_복사해서_넣으세요" 문구 전체를 지우고 ID만 넣으세요.
# 예: SHEET_ID = "1AbC_dEfG-hiJkL_mnoPQR"
SHEET_ID = "여기에_본인의_시트_ID만_복사해서_넣으세요" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard", layout="wide")

@st.cache_data(ttl=30) # 30초마다 시트 업데이트 확인
def load_data_from_sheets():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return None
        df = pd.read_csv(io.StringIO(response.text))
        return df.set_index('key')['value'].to_dict()
    except:
        return None

raw_data = load_data_from_sheets()

if raw_data:
    # --- [2] CSS 스타일 ---
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

    # --- [3] 헤더 ---
    st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.2rem;">주간 마케팅 통찰 보고서</h1>
        <p style="margin:0; opacity:0.8;">구글 시트 연동 중 ({datetime.now().strftime('%H:%M:%S')} 기준)</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [4] KPI 카드 ---
    k1, k2, k3, k4 = st.columns(4)
    kpi_map = [
        (k1, "전체 모멘텀", f"{raw_data.get('momentum', 0)}%"),
        (k2, "지역 편차", f"{raw_data.get('deviation', 0)}%"),
        (k3, "MZ 도달율", f"{raw_data.get('mz_reach', 0)}%"),
        (k4, "NPS 점수", raw_data.get('nps', 0))
    ]
    for col, lab, val in kpi_map:
        col.markdown(f'<div class="report-card"><p class="kpi-label">{lab}</p><p class="kpi-value">{val}</p></div>', unsafe_allow_html=True)

    # --- [5] 차트 및 제언 ---
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.markdown('<div class="report-card"><h3>채널별 판매 성과</h3>', unsafe_allow_html=True)
        chart_vals = [
            float(raw_data.get('chart_1', 0)), float(raw_data.get('chart_2', 0)),
            float(raw_data.get('chart_3', 0)), float(raw_data.get('chart_4', 0))
        ]
        fig = px.bar(x=['수도권(편점)', '수도권(기타)', '지방(마트)', '지방(기타)'], y=chart_vals, color=chart_vals, color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown(f"""
        <div class="report-card" style="height: 100%; border-left: 10px solid #c53030;">
            <h3 style="color:#c53030; margin-top:0;">팀장 종합 제언</h3>
            <p style="font-size:1.1rem; line-height:1.6; color: #333;">{raw_data.get('note', '내용 없음')}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("⚠️ 시트 ID를 확인하거나 공유 설정을 '링크가 있는 모든 사용자'로 바꿔주세요.")
