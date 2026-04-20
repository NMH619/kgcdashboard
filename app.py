import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- [설정] 본인의 구글 시트 ID를 입력하세요 ---
# 예: https://docs.google.com/spreadsheets/d/1abc123... 에서 ID 부분만 복사
SHEET_ID = "여기에_본인의_시트_ID를_넣으세요"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

st.set_page_config(page_title="KGC Dashboard", layout="wide")

# --- [데이터] 스프레드시트에서 데이터 가져오기 ---
def load_data_from_sheets():
    try:
        # 구글 시트를 판다스로 읽어옵니다.
        df = pd.read_csv(SHEET_URL)
        # 키(key) 열을 인덱스로 만들어서 값을 찾기 쉽게 변환합니다.
        data_dict = df.set_index('key')['value'].to_dict()
        
        # 가져온 데이터를 앱 형식에 맞게 정리
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
            "note": data_dict.get('note', "제언 내용이 없습니다."),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    except Exception as e:
        st.error(f"시트를 읽어오는데 실패했습니다: {e}")
        return None

data = load_data_from_sheets()

# 데이터 로드 성공 시에만 화면 출력
if data:
    # --- [디자인] CSS ---
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

    # --- [화면] 헤더 ---
    st.markdown(f"""
    <div class="header-box">
        <h1 style="margin:0; font-size: 2.2rem;">주간 마케팅 통찰 보고서</h1>
        <p style="margin:0; opacity:0.8;">실시간 시트 연동 중 (업데이트: {data['last_updated']})</p>
    </div>
    """, unsafe_allow_html=True)

    # --- [화면] KPI 카드 ---
    k1, k2, k3, k4 = st.columns(4)
    kpis = [(k1, "전체 모멘텀", f"{data['momentum']}%"), (k2, "지역 편차", f"{data['deviation']}%"),
            (k3, "MZ 도달율", f"{data['mz_reach']}%"), (k4, "NPS 점수", data['nps'])]

    for col, label, val in kpis:
        col.markdown(f'<div class="report-card"><p class="kpi-label">{label}</p><p class="kpi-value">{val}</p></div>', unsafe_allow_html=True)

    # --- [화면] 차트 ---
    c_left, c_right = st.columns([2, 1])
    with c_left:
        st.markdown('<div class="report-card"><h3>채널별 판매 성과</h3>', unsafe_allow_html=True)
        fig_bar = px.bar(x=['수도권(편점)', '수도권(기타)', '지방(마트)', '지방(기타)'], y=data['chart_data'], color=data['chart_data'], color_continuous_scale='Reds')
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_right:
        st.markdown('<div class="report-card"><h3>연령 비중</h3>', unsafe_allow_html=True)
        fig_pie = px.pie(values=[45, 38, 17], names=['2030', '4050', '60+'], hole=0.5, color_discrete_sequence=['#c53030', '#4a5568', '#a0aec0'])
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- [화면] 제언 ---
    st.markdown(f"""
    <div class="report-card" style="border-left: 10px solid #c53030;">
        <h3 style="color:#c53030; margin-top:0;">팀장 종합 제언</h3>
        <p style="font-size:1.1rem; line-height:1.6; color: #333;">{data['note']}</p>
    </div>
    """, unsafe_allow_html=True)
