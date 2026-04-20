import streamlit as st
import pandas as pd
import plotly.express as px
import json
from datetime import datetime

# --- 1. 기본 설정 및 데이터 로드 ---
st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")

def load_data():
    # 데이터베이스 연결 전까지 사용할 기본값
    default_data = {
        "momentum": 6.5, "mz_reach": 45, "nps": 7.8, "deviation": 17.0,
        "chart_data": [15.0, 8.0, -2.0, 1.5],
        "note": "지방 거점 마트의 가시성 확보가 시급합니다. 제품 진열 위치를 재조정하세요.",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = default_data
    return st.session_state.stored_data

data = load_data()

# --- 2. CSS 스타일 (따옴표 오류 수정됨) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .report-card { background: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 1rem; }
    .gradient-header { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 100%); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem; }
    .kpi-value { font-size: 2rem; font-weight: 900; color: #1a202c; }
    .kpi-label { font-size: 0.85rem; font-weight: 700; color: #718096; }
</style>
""", unsafe_allow_html=True)

# --- 3. 대시보드 헤더 ---
header_html = f"""
<div class="gradient-header">
    <h1 style="margin:0; font-size: 2.5rem;">주간 마케팅 통찰 보고서</h1>
    <p style="margin:0; opacity:0.8;">최종 업데이트: {data['last_updated']}</p>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# --- 4. KPI 카드 ---
k1, k2, k3, k4 = st.columns(4)
kpis = [("전체 모멘텀", f"{data['momentum']}%"), ("지역 편차", f"{data['deviation']}%"), 
        ("MZ 도달율", f"{data['mz_reach']}%"), ("NPS 점수", data['nps'])]

for col, (label, val) in zip([k1, k2, k3, k4], kpis):
    col.markdown(f'<div class="report-card"><p class="kpi-label">{label}</p><p class="kpi-value">{val}</p></div>', unsafe_allow_html=True)

# --- 5. 차트 섹션 ---
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
    fig_pie = px.pie(values=[45, 38, 17], names=['2030', '4050', '60+'], hole=0.5, color_discrete_sequence=['#c53030', '#4a5568', '#a0aec0'])
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('
