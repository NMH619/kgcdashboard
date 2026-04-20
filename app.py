import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="KGC 브랜드전략실 - 3월 4주차 대시보드", layout="wide")

# --- [데이터 로드 섹션] ---
# 구글 시트 주소 설정 (본인의 시트 ID와 gid 번호를 아래에 입력하세요)
# 시트 URL 끝의 /edit... 부분을 /export?format=csv&gid=... 로 수정해야 합니다.

# 예시 주소 (실제 본인의 시트 주소로 교체 필요)
KPI_URL = "https://docs.google.com/spreadsheets/d/1eDRHR3Jfd0P7hwmZy1d_Ncdb-AXhGhwe62lFaNKjF8s/export?format=csv&gid=0"
REGION_URL = "https://docs.google.com/spreadsheets/d/1eDRHR3Jfd0P7hwmZy1d_Ncdb-AXhGhwe62lFaNKjF8s/export?format=csv&gid=1330935199"
AGE_URL = "https://docs.google.com/spreadsheets/d/1eDRHR3Jfd0P7hwmZy1d_Ncdb-AXhGhwe62lFaNKjF8s/export?format=csv&gid=547463562"

@st.cache_data(ttl=600)  # 10분간 캐시 유지 (성능 최적화)
def load_data(url):
    return pd.read_csv(url)

try:
    df_kpi = load_data(KPI_URL)
    df_region = load_data(REGION_URL)
    df_age = load_data(AGE_URL)
except Exception as e:
    st.error("⚠️ 데이터를 불러올 수 없습니다. 구글 시트 공유 설정과 URL을 확인해주세요.")
    st.stop()
# -----------------------

# 2. 커스텀 CSS
st.markdown("""
    <style>
    .kpi-value { font-size: 28px; font-weight: bold; color: #A6192E; }
    </style>
""", unsafe_allow_html=True)

# 3. 헤더 영역
col_header1, col_header2 = st.columns([3, 1])
with col_header1:
    st.title("📈 에브리타임 밸런스 마케팅 대시보드")
    st.markdown("**2026년 3월 4주차 | 리뉴얼 제품 판매 현황 분석**")
with col_header2:
    st.write("") 
    st.info("👤 **팀장: 인선미** (Brand Strategy)")

st.markdown("---")

# 4. KPI 카드 영역 (구글 시트 데이터 기반)
# 시트 구성: label, value, delta 컬럼이 있다고 가정
kpi_cols = st.columns(len(df_kpi))

for i, col in enumerate(kpi_cols):
    # delta_color는 2번째(index 1), 4번째(index 3) 카드일 때 off 처리 (기존 로직 유지)
    d_color = "off" if i in [1, 3] else "normal"
    col.metric(
        label=df_kpi.iloc[i]['label'], 
        value=df_kpi.iloc[i]['value'], 
        delta=df_kpi.iloc[i]['delta'],
        delta_color=d_color
    )

st.markdown("<br>", unsafe_allow_html=True)

# 5. 차트 영역
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("지역별 판매 성장률 (%)")
    # 시트 구성: 지역, 성장률 컬럼
    fig_region = px.bar(
        df_region, x="지역", y="성장률", text="성장률", 
        color="지역", color_discrete_sequence=['#A6192E', '#94a3b8']
    )
    fig_region.update_layout(showlegend=False, margin=dict(t=20, b=20, l=0, r=0))
    st.plotly_chart(fig_region, use_container_width=True)

with chart_col2:
    st.subheader("소비자 연령대 분포")
    # 시트 구성: 연령대, 비중 컬럼
    fig_age = px.pie(
        df_age, values="비중", names="연령대", hole=0.5,
        color_discrete_sequence=['#A6192E', '#C5A059', '#cbd5e1']
    )
    fig_age.update_layout(margin=dict(t=20, b=20, l=0, r=0), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_age, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 6. 피드백 및 인사이트
bottom_col1, bottom_col2 = st.columns([2, 1])

with bottom_col1:
    st.subheader("💬 실시간 고객 VOC 분석")
    voc1, voc2 = st.columns(2)
    with voc1:
        st.success("**🟢 Positive**\n\n- 포장이 세련되어 선물용으로 최고입니다.\n- 기존 홍삼보다 쓴맛이 덜해서 먹기 편해요.")
    with voc2:
        st.error("**🔴 Improvement**\n\n- 리뉴얼 후 가격이 조금 오른 것 같아요.\n- **박스 개봉 시 가끔 뻑뻑함이 느껴집니다.**")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("💡 팀장 전략 제언 (Action Items)")
    st.info("""
    1. **아웃도어 마케팅:** 테니스/등산 커뮤니티 연계 '오운완' 캠페인 즉시 실행
    2. **채널 최적화:** 지방권 대형마트 '가족 건강 키트' 번들 기획 구성
    3. **품질 개선:** 패키지 개봉 편의성(Easy-off) 관련 생산 파트 피드백 전달
    """)

with bottom_col2:
    st.subheader("🔥 트렌드 키워드")
    st.markdown("`#사회초년생` `#테니스` `#오운완` `#선물추천` `#등산` `#에너지부스터`")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### 📌 Today's Summary")
    st.caption("2030 라이프스타일 깊숙이 침투하는 것이 이번 리뉴얼의 핵심입니다. 단순 건강기능식품을 넘어 패션과 스포츠의 영역으로 확장합시다.")
