import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime

# Firebase 관련 라이브러리 (오류 방지를 위한 try-except)
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ImportError:
    st.error("설치되지 않은 라이브러리가 있습니다. requirements.txt를 확인해 주세요.")

# --- 1. 환경 설정 및 Firebase 초기화 ---
def init_db():
    app_id = globals().get('__app_id', 'kgc-strategy-app')
    firebase_config_str = globals().get('__firebase_config', '{}')
    
    try:
        config = json.loads(firebase_config_str)
        db = firestore.Client() 
        return db, app_id
    except Exception:
        return None, app_id

db, APP_ID = init_db()

# --- 2. 데이터 관리 로직 ---
COLLECTION_PATH = f"artifacts/{APP_ID}/public/data/marketing_dashboard"
DOC_ID = "current_state"

def load_data():
    default_data = {
        "momentum": 6.5,
        "mz_reach": 45,
        "nps": 7.8,
        "deviation": 17.0,
        "chart_data": [15.0, 8.0, -2.0, 1.5],
        "note": "수도권 편의점 강세는 확인되었으나, 지방 대형마트 정체가 우려됩니다.",
        "last_updated": datetime.now().isoformat()
    }
    
    if db:
        try:
            doc_ref = db.document(f"{COLLECTION_PATH}/{DOC_ID}")
            doc = doc_ref.get()
            if doc.exists:
                return doc.to_dict()
        except Exception:
            pass
    
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = default_data
    return st.session_state.stored_data

def save_data(new_data):
    new_data["last_updated"] = datetime.now().isoformat()
    if db:
        try:
            doc_ref = db.document(f"{COLLECTION_PATH}/{DOC_ID}")
            doc_ref.set(new_data)
            return True
        except Exception as e:
            st.error(f"저장 실패: {e}")
    
    st.session_state.stored_data = new_data
    return True

# --- 3. UI 및 페이지 설정 ---
st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")
data = load_data()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .report-card { background: white; padding: 1.5rem; border-radius: 1.25rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; margin-bottom: 1rem; }
    .gradient-header { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 10
