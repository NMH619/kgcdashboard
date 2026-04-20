import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime

# --- 1. Firebase 라이브러리 체크 ---
try:
    from google.cloud import firestore
except ImportError:
    st.error("라이브러리가 부족합니다. requirements.txt를 먼저 확인해 주세요.")

# --- 2. 초기화 및 데이터 로드 ---
def init_db():
    app_id = globals().get('__app_id', 'kgc-strategy-app')
    firebase_config_str = globals().get('__firebase_config', '{}')
    try:
        db = firestore.Client() 
        return db, app_id
    except Exception:
        return None, app_id

db, APP_ID = init_db()

def load_data():
    default_data = {
        "momentum": 6.5, "mz_reach": 45, "nps": 7.8, "deviation": 17.0,
        "chart_data": [15.0, 8.0, -2.0, 1.5],
        "note": "지방 거점 마트 가시성 확보가 필요합니다.",
        "last_updated": datetime.now().isoformat()
    }
    if db:
        try:
            doc_ref = db.document(f"artifacts/{APP_ID}/public/data/marketing_dashboard/current_state")
            doc = doc_ref.get()
            if doc.exists: return doc.to_dict()
        except: pass
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = default_data
    return st.session_state.stored_data

# --- 3. UI 설정 (따옴표 오류 수정 지점) ---
st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")
data = load_data()

# CSS 스타일 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .report-card { background: white; padding: 1.5rem; border-radius: 1.25rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; margin-bottom: 1rem; }
    .gradient-header { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 100%); padding: 2.5rem; border-radius: 1.25rem; color: white; margin-bottom: 2rem; }
    .kpi-value { font-
