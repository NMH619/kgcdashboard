import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
from datetime import datetime

# --- 1. 라이브러리 체크 및 데이터 로드 설정 ---
try:
    from google.cloud import firestore
except ImportError:
    pass

def load_data():
    # 기본값 설정
    default_data = {
        "momentum": 6.5, "mz_reach": 45, "nps": 7.8, "deviation": 17.0,
        "chart_data": [15.0, 8.0, -2.0, 1.5],
        "note": "지방 거점 마트 가시성 확보가 필요합니다. 오프라인 매대 진열을 강화하세요.",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = default_data
    return st.session_state.stored_data

# --- 2. 페이지 설정 및 디자인 ---
st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")
data = load_data()

# CSS 주입 (따옴표 오류 완벽 수정)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .report-card { background: white; padding: 1.5rem; border-radius: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 1rem; }
    .gradient-header { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 100%); padding: 2rem; border-radius: 1rem; color: white; margin-bottom: 2rem; }
    .kpi-value { font-size: 2rem; font-weight: 900; color: #1a202c; }
    .kpi-label { font-size: 0.8rem; font-weight: 700; color: #718096; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- 3. 대시보드 상단 헤더 ---
st.markdown(f"""
<div class="gradient-header">
    <h1 style="margin:0;">주간 마케팅 통
