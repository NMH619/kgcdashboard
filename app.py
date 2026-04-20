import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 설정 ---
# 시트 ID는 그대로 유지했습니다.
SHEET_ID = "1u2QkksoyVFS7NWoHi-H93WlxKynAyEx8s5Q_OBNnsl0"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")

@st.cache_data(ttl=10)
def load_data():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return None
        
        df = pd.read_csv(io.StringIO(response.text))
        
        # [보안 1] 컬럼명(key, value) 앞뒤 공백 제거 및 소문자 통일
        df.columns = [c.strip().lower() for c in df.columns]
        
        # [보안 2] key 열의 데이터들 앞뒤 공백 제거
        if 'key' in df.columns and 'value' in df.columns:
            df['key'] = df['key'].astype(str).str.strip()
            return df.set_index('key')['value'].to_dict()
        else:
            st.error("시트의 1행 제목이 'key'와 'value'인지 확인해주세요.")
            return None
    except Exception as e:
        st.error(f"데이터 연결 오류: {e}")
        return None

raw_data = load_data()

# 데이터 로드 성공 시에만 화면 출력
if raw_data:
    # --- [2] 디자인 스타일 (CSS) ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
        * { font-family: 'Pretendard', sans-serif; }
        .report-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 1rem; }
        .header-box { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem; }
        .kpi-value { font-size: 2.1rem; font-weight: 900; color: #1a202c; margin: 0; }
        .kpi-label { font-size: 0.85rem; font-weight: 700; color: #718096; margin-bottom: 0.5rem; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

    # --- [3] 상단 헤더 ---
    st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.2rem; font-weight: 900;">주간 마케팅 통찰 보고서</h1>
        <p style="margin:0; opacity:0.8;">실시간 시트 연동 중 (업데이트: {datetime.now().strftime('%H:%M:%S')})</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [4] 주요 지표 (KPI) ---
    k1, k2, k3, k4 = st.columns(4)
    
    # 데이터가 없을 경우 0으로 표시하도록 안전장치 강화
    def get_val(key_name, default=0):
        val = raw_data.get(key_name, default)
        return val
