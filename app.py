import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import io
from datetime import datetime

# --- [1] 구글 시트 설정 (새 시트 ID 적용) ---
SHEET_ID = "1p6KwL_FxoJtCtkhQoeq_aqIzFJ50e7lshyfWhtK030s"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="Everytime Balance Dashboard", layout="wide")

@st.cache_data(ttl=10)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        if res.status_code != 200: return None
        df = pd.read_csv(io.StringIO(res.text))
        df['key'] = df['key'].astype(str).str.strip()
        return df.set_index('key')['value'].to_dict()
    except: return None

raw = load_data()

if raw:
    # --- [2] 디자인 스타일 ---
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
        * { font-family: 'Pretendard', sans-serif; }
        .report-card { background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; margin-bottom: 1rem; }
        .header-box { background: #000; padding: 2.5rem; border-radius: 15px; color: white; margin-bottom: 2rem; border-left: 10px solid #c53030; }
        .kpi-val { font-size: 2.2rem; font-weight: 900; color: #1a202c; margin: 0; }
        .kpi-sub { font-size: 0.9rem; color: #c53030; font-weight: 700; margin-top: 5px; }
        .tag { background: #f7fafc; padding: 5px 12px; border-radius: 20px; font-size: 0.85rem; color: #4a5568; border: 1px solid #edf2f7; display: inline-block; margin-right: 5px; }
        .voc-pos { color: #2c5282; font-size: 0.95rem; line-height: 1.6; }
        .voc-neg { color: #9b2c2c; font-size: 0.95rem; line-height: 1.6; }
    </style>
    """, unsafe_allow_html=True)

    # --- [3] 헤더 ---
    st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.4rem;">{raw.get('title')}</h1>
        <p style="margin:5px 0 0 0; opacity:0.7;">{raw.get('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [4] KPI 섹션 ---
    cols = st.columns(4)
    for i in range(1, 5):
        with cols[i-1]:
            st.markdown(f"""
            <div class="report-card">
                <p style="font-size:0.9rem; font-weight:700; color:#718096; margin-bottom:10px;">{raw.get(f'kpi_{i}_label')}</p>
                <p class="kpi-val">{raw.get(f'kpi_{i}_val')}</p>
                <p class="kpi-sub">{raw_data.get(f'kpi_{i}_sub') if 'raw_data' in locals() else raw.get(f'kpi_{i}_sub')}</p>
            </div>
            """, unsafe_allow_html=True)

    # --- [5] 차트 섹션 ---
    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown('<div class="report-card"><h3>지역별 판매 성장률 (%)</h3>', unsafe_allow_html=True)
        cv = [float(raw.get('chart_bar_1', 0)), float(raw_data.get('chart_bar_2', 0)) if 'raw_data' in locals() else float(raw.get('chart_bar_2', 0))]
        fig1 = px.bar(x=['수도권(편의점)', '지방(대형마트)'], y=cv, color=cv, color_continuous_scale='Reds')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with c2:
        st.markdown('<div class="report-card"><h3>소비자 연령대 분포</h3>', unsafe_allow_html=True)
        pv = [float(raw.get('chart_pie_1', 0)), float(raw.get('chart_pie_2', 0)), float(raw.get('chart_pie_3', 0))]
        fig2 = px.pie(values=pv, names=['2030 사회초년생', '4050 부모세대', '기타'], hole=0.6, color_discrete_sequence=['#c53030', '#4a5568', '#cbd5e0'])
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- [6] VOC & 트렌드 ---
    v1, v2 = st.columns(2)
    with v1:
        st.markdown(f"""
        <div class="report-card">
            <h3>실시간 고객의 소리 (VOC)</h3>
            <p class="voc-pos"><b>✅ 긍정:</b> {raw.get('voc_pos_1')}<br>{raw.get('voc_pos_2')}</p>
            <p class="voc-neg"><b>⚠️ 개선:</b> {raw.get('voc_neg_1')}<br>{raw.get('voc_neg_2')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with v2:
        tags = raw.get('trend_tags', '').split(' ')
        tag_html = "".join([f'<span class="tag">{t}</span>' for t in tags])
        st.markdown(f"""
        <div class="report-card">
            <h3>급상승 트렌드 키워드</h3>
            <div style="margin-top:15px;">{tag_html}</div>
            <hr style="margin:20px 0; border:0; border-top:1px solid #eee;">
            <p style="font-weight:700; color:#c53030; margin-bottom:5px;">💡 오늘의 한 줄 요약</p>
            <p style="font-size:0.95rem; line-height:1.6;">{raw.get('summary')}</p>
        </div>
        """, unsafe_allow_html=True)

    # --- [7] 팀장 액션 아이템 ---
    st.markdown(f"""
    <div class="report-card" style="border-top: 5px solid #000;">
        <h3 style="margin-top:0;">🚀 팀장 주요 액션 아이템 (Action Items)</h3>
        <ul style="line-height:2; font-size:1.05rem;">
            <li>{raw.get('action_1')}</li>
            <li>{raw.get('action_2')}</li>
            <li>{raw.get('action_3')}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("데이터 로드 실패. 시트 공유 설정을 확인하세요.")
