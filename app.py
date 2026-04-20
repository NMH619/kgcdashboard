import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 ID 설정 ---
# ⚠️ 반드시 본인의 시트 ID(주소창의 영문+숫자 조합)를 넣으세요!
SHEET_ID = "1u2QkksoyVFS7NWoHi-H93WlxKynAyEx8s5Q_OBNnsl0" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard Debug", layout="wide")

# 데이터 강제 새로고침 버튼 (사이드바)
if st.sidebar.button("🔄 데이터 강제 새로고침"):
    st.cache_data.clear()
    st.rerun()

@st.cache_data(ttl=10)
def load_data():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            return "CONNECTION_ERROR", None
        
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = [c.strip().lower() for c in df.columns]
        
        if 'key' not in df.columns or 'value' not in df.columns:
            return "HEADER_ERROR", df.columns.tolist()
            
        df['key'] = df['key'].astype(str).str.strip()
        return "SUCCESS", df.set_index('key')['value'].to_dict()
    except Exception as e:
        return "EXCEPTION", str(e)

status, result = load_data()

# --- [2] 에러 진단 및 화면 출력 ---
if status != "SUCCESS":
    st.error(f"❌ 데이터 로드 실패: {status}")
    if status == "CONNECTION_ERROR":
        st.info("구글 시트 공유 설정이 '링크가 있는 모든 사용자'로 되어 있나요?")
    elif status == "HEADER_ERROR":
        st.warning(f"시트의 제목이 'key'와 'value'가 아닙니다. 현재 감지된 제목: {result}")
    elif status == "EXCEPTION":
        st.code(result) # 구체적인 에러 메시지 출력
else:
    # 정상 작동 시 대시보드 그리기
    raw_data = result
    
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
        * { font-family: 'Pretendard', sans-serif; }
        .report-card { background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 1rem; }
        .header-box { background: linear-gradient(135deg, #c53030 0%, #9b1c1c
