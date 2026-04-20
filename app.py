import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [중요] 본인의 구글 시트 ID로 교체하세요 ---
# 주소창의 /d/ 와 /edit 사이의 영문+숫자 조합입니다.
SHEET_ID = "여기에_본인의_시트_ID만_복사해서_넣으세요" 
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard", layout="wide")

@st.cache_data(ttl=600) # 10분마다 데이터를 새로고침합니다.
def load_data_from_sheets():
    try:
        # 한글 인코딩 에러를 방지하기 위해 requests를 사용합니다.
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8' # 한글 깨짐 방지 설정
        
        if response.status_code != 200:
            st.error("시트 ID가 올바르지 않거나 공유 설정(링크가 있는 모든 사용자에게 공개)을 확인해 주세요.")
            return None

        # 읽어온 데이터를 데이터프레임으로 변환
        df = pd.read_csv(io.StringIO(response.text))
        data_dict = df.set_index('key')['value'].to_dict()
        
        return {
            "momentum": float(data_dict.get('momentum', 0)),
            "mz_reach": float(data_dict.get('mz_reach', 0)),
            "nps": float(data_dict.get('nps', 0)),
            "deviation": float(data_dict.get('deviation', 0)),
            "chart_data": [
                float(data_dict.get('chart_1', 0)),
                float(data_dict.get('chart_2', 0)),
                float(data_dict.get('chart_3', 0)),
                float(data_dict.get('chart_4', 0))
            ],
            "note": str(data_dict.get('note', "제언 내용이 없습니다.")),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    except Exception as e:
        st.error(f"데이터 로딩 중 오류가 발생했습니다: {e}")
        return None

data = load_data_from_sheets()

# 데이터 로드 성공 시 화면 출력
if data:
    # --- [디자인] CSS 스타일 ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
        * { font-family: 'Pretendard', sans-
