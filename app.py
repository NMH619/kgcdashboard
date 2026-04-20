import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime

# Firebase 관련 라이브러리 (환경에 따라 사용 가능 여부 확인 필요)
try:
    from google.cloud import firestore
    from google.oauth2 import service_account
except ImportError:
    st.error("Required libraries (google-cloud-firestore) are missing. Please install them.")

# --- 1. 환경 설정 및 Firebase 초기화 ---
def init_db():
    """환경 변수로부터 Firebase 설정을 읽어 Firestore 클라이언트를 반환합니다."""
    # 시스템에서 제공하는 글로벌 변수 확인
    app_id = globals().get('__app_id', 'kgc-strategy-app')
    firebase_config_str = globals().get('__firebase_config', '{}')
    
    try:
        config = json.loads(firebase_config_str)
        # 실제 환경에서는 서비스 계정 키나 토큰을 통해 인증하지만, 
        # 여기서는 클라이언트 직접 생성을 가정합니다.
        db = firestore.Client() 
        return db, app_id
    except Exception as e:
        # 인증 오류 시 로컬 테스트를 위해 None 반환 (실제 배포 시 구성 필요)
        return None, app_id

db, APP_ID = init_db()

# --- 2. 데이터 관리 로직 ---
COLLECTION_PATH = f"artifacts/{APP_ID}/public/data/marketing_dashboard"
DOC_ID = "current_state"

def load_data():
    """클라우드에서 데이터를 불러옵니다. 없을 경우 기본값을 반환합니다."""
    default_data = {
        "momentum": 6.5,
        "mz_reach": 45,
        "nps": 7.8,
        "deviation": 17.0,
        "chart_data": [15.0, 8.0, -2.0, 1.5],
        "note": "수도권 편의점 강세는 확인되었으나, 지방 대형마트 정체가 우려됩니다. 지방 거점 마트에서는 '가족 단위 건강 캠페인'으로 소구점을 전환하여 오프라인 매대 가시성을 확보해야 합니다.",
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
    
    # 데이터가 없거나 DB 연결 실패 시 세션 상태 또는 기본값 사용
    if 'stored_data' not in st.session_state:
        st.session_state.stored_data = default_data
    return st.session_state.stored_data

def save_data(new_data):
    """수정된 데이터를 클라우드(또는 세션)에 저장합니다."""
    new_data["last_updated"] = datetime.now().isoformat()
    if db:
        try:
            doc_ref = db.document(f"{COLLECTION_PATH}/{DOC_ID}")
            doc_ref.set(new_data)
            return True
        except Exception as e:
            st.error(f"저장 실패: {e}")
    
    # 폴백: 세션에 저장
    st.session_state.stored_data = new_data
    return True

# --- 3. UI 및 페이지 설정 ---
st.set_page_config(page_title="KGC Strategy Dashboard", layout="wide")

# 데이터 로드
data = load_data()

# CSS 주입 (기존 스타일 유지)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
    * { font-family: 'Pretendard', sans-serif; }
    .main { background-color: #f3f4f6; }
    .report-card { background: white; padding: 1.5rem; border-radius: 1.25rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); border: 1px solid #e5e7eb; margin-bottom: 1rem; }
    .gradient-header { background: linear-gradient(135deg, #c53030 0%, #9b1c1c 100%); padding: 2.5rem; border-radius: 1.25rem; color: white; margin-bottom: 2rem; }
    .kpi-value { font-size: 2.25rem; font-weight: 800; color: #1e293b; line-height: 1; }
    .kpi-label { font-size: 0.875rem; font-weight: 700; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# --- 4. 사이드바 편집 모드 ---
with st.sidebar:
    st.header("⚙️ 관리자 편집 모드")
    edit_mode = st.toggle("편집 기능 활성화", value=False)
    
    if edit_mode:
        st.subheader("1. 주요 KPI 수정")
        new_momentum = st.number_input("판매 모멘텀 (%)", value=data['momentum'])
        new_mz = st.slider("MZ 도달율 (%)", 0, 100, data['mz_reach'])
        new_nps = st.number_input("NPS 점수", 0.0, 10.0, data['nps'])
        new_dev = st.number_input("지역 편차 (%)", 0.0, 100.0, data['deviation'])
        
        st.divider()
        st.subheader("2. 차트 데이터 (증감률 %)")
        c1 = st.number_input("수도권(편의점)", value=data['chart_data'][0])
        c2 = st.number_input("수도권(기타)", value=data['chart_data'][1])
        c3 = st.number_input("지방(대형마트)", value=data['chart_data'][2])
        c4 = st.number_input("지방(기타)", value=data['chart_data'][3])
        
        st.divider()
        st.subheader("3. 제언 내용")
        new_note = st.text_area("Action Plan", value=data['note'], height=200)
        
        if st.button("🚀 클라우드에 최종 저장", use_container_width=True):
            updated_payload = {
                "momentum": new_momentum,
                "mz_reach": new_mz,
                "nps": new_nps,
                "deviation": new_dev,
                "chart_data": [c1, c2, c3, c4],
                "note": new_note
            }
            if save_data(updated_payload):
                st.success("데이터가 성공적으로 저장되었습니다!")
                st.rerun()

# --- 5. 메인 대시보드 렌더링 ---

# 헤더
st.markdown(f"""
    <div class="gradient-header">
        <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 8px; font-size: 12px; font-weight: 700;">Secretariat</span>
        <h1 style="margin: 10px 0; font-size: 40px; font-weight: 900;">주간 마케팅 통찰 보고서</h1>
        <p style="margin: 0; opacity: 0.8;">최종 업데이트: {data['last_updated']}</p>
    </div>
""", unsafe_allow_html=True)

# KPI
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown(f'<div class="report-card"><p class="kpi-label">전체 모멘텀</p><p class="kpi-value">{data["momentum"]}%</p></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="report-card"><p class="kpi-label">지역 편차</p><p class="kpi-value">{data["deviation"]}%</p></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="report-card"><p class="kpi-label">MZ 도달</p><p class="kpi-value">{data["mz_reach"]}%</p></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="report-card"><p class="kpi-label">NPS 점수</p><p class="kpi-value">{data["nps"]}</p></div>', unsafe_allow_html=True)

# 차트
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<div class="report-card"><h3>채널별 판매 성과</h3>', unsafe_allow_html=True)
    fig_bar = px.bar(
        x=['수도권(편의점)', '수도권(기타)', '지방(대형마트)', '지방(기타)'],
        y=data['chart_data'],
        color=data['chart_data'],
        color_continuous_scale='Reds',
        labels={'x': '채널', 'y': '증감률 (%)'}
    )
    fig_bar.update_layout(height=400, margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="report-card"><h3>연령 비중</h3>', unsafe_allow_html=True)
    fig_pie = px.pie(values=[45, 38, 17], names=['2030', '4050', '60+'], hole=0.6, color_discrete_sequence=['#c53030', '#475569', '#cbd5e1'])
    fig_pie.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 제언
st.markdown(f"""
    <div class="report-card" style="border-left: 8px solid #c53030;">
        <h3 style="color: #c53030; margin-top: 0;">팀장 종합 제언</h3>
        <p style="font-size: 16px; line-height: 1.6; color: #334155;">{data['note']}</p>
    </div>
""", unsafe_allow_html=True)
