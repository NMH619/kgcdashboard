import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")

# --- 2. 데이터 준비 ---
def load_data():
    return {
        "momentum": 6.5,
        "mz_reach": 45,
        "nps": 7.8,
        "deviation": 17.0,
        "chart_data": [15.0, 8.0, -2.0, 1.5],
        "note": "지방 거점 마트의 가시성 확보가 시급합니다. 오프라인 매대 진열을 강화하고 가족 단위 캠페인을 검토하세요.",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

data = load_data()

# --- 3. 스타일 설정 (CSS) ---
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

# --- 4. 상단 헤더 ---
st.markdown(f"""
<div class="header-box">
    <h1 style="margin:0; font-size: 2.2rem;">주간 마케팅 통찰 보고서</h1>
    <p style="margin:0; opacity:0.8;">최종 업데이트: {data['last_updated']}</p>
</div>
""", unsafe_allow_html=True)

# --- 5. KPI 카드 ---
k1, k2, k3, k4 = st.columns(4)
kpis = [
    (k1, "전체 모멘텀", f"{data['momentum']}%"),
    (k2, "지역 편차", f"{data['deviation']}%"),
    (k3, "MZ 도달율", f"{data['mz_reach']}%"),
    (k4, "NPS 점수", data['nps'])
]

for col, label, val in kpis:
    col.markdown(f"""
    <div class="report-card">
        <p class="kpi-label">{label}</p>
        <p class="kpi-value">{val}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. 차트 섹션 (에러 수정 지점) ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="report-card"><h3>채널별 판매 성과</h3>', unsafe_allow_html=True)
    fig_bar = px.bar(
        x=['수도권(편점)', '수도권(기타)', '지방(마트)', '지방(기타)'], 
        y=data['chart_data'], 
        color=data['chart_data'], 
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="report-card"><h3>연령 비중</h3>', unsafe_allow_html=True)
    fig_pie = px.pie(
        values=[45, 38, 17], 
        names=['2030', '4050', '60+'], 
        hole=0.5, 
        color_discrete_sequence=['#c53030', '#4a5568', '#a0aec0']
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 7. 하단 제언 ---
st.markdown(f"""
<div class="report-card" style="border-left: 10px solid #c53030;">
    <h3 style="color:#c53030; margin-top:0;">팀장 종합 제언</h3>
    <p style="font-size:1.1rem; line-height:1.6; color: #333;">{data['note']}</p>
</div>
""", unsafe_allow_html=True)
