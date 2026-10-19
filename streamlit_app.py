import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 및 치이카와풍 파스텔 테마 설정
st.set_page_config(page_title="나의 진로 나침반", page_icon="🐹", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FFF5F7; } 
    h1, h2, h3, h4 { color: #FF8E9E !important; } 
    .stButton>button { background-color: #A3D8F4; color: #333; border-radius: 20px; border: none; font-weight: bold; }
    div[data-testid="stExpander"] { background-color: #FFFFFF; border-radius: 15px; border: 2px solid #FFE4E1; }
    </style>
""", unsafe_allow_html=True)

st.title("🐹 나의 진로 나침반 (데이터 탐구 학습지)")
st.write("나의 성향을 입력하고 직업 데이터를 직접 분석하여 진로 로드맵을 완성해 보세요!")
st.divider()

# 2. 내부 데이터베이스 (DB 없이 DataFrame 활용)
data = [
    {"직업명": "소프트웨어 개발자", "MBTI_추천": "INTJ, INTP, ISTP", "홀랜드_추천": "탐구형(I), 현실형(R)", "창의성": 8, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 3},
    {"직업명": "데이터 사이언티스트", "MBTI_추천": "INTJ, INTP, ENTJ", "홀랜드_추천": "탐구형(I), 관습형(C)", "창의성": 7, "논리분석력": 10, "대인관계": 5, "AI대체위험도": 2},
    {"직업명": "콘텐츠 크리에이터", "MBTI_추천": "ENFP, ENTP, INFP", "홀랜드_추천": "예술형(A), 진취형(E)", "창의성": 10, "논리분석력": 4, "대인관계": 7, "AI대체위험도": 4},
    {"직업명": "마케팅 전문가", "MBTI_추천": "ENFJ, ESTJ, ENTJ", "홀랜드_추천": "진취형(E), 사회형(S)", "창의성": 8, "논리분석력": 6, "대인관계": 9, "AI대체위험도": 5},
    {"직업명": "상담 심리사", "MBTI_추천": "INFJ, INFP, ENFJ", "홀랜드_추천": "사회형(S), 예술형(A)", "창의성": 5, "논리분석력": 6, "대인관계": 10, "AI대체위험도": 1},
    {"직업명": "기계 공학자", "MBTI_추천": "ISTJ, ISTP, ESTJ", "홀랜드_추천": "현실형(R), 탐구형(I)", "창의성": 6, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 4},
    {"직업명": "경영 컨설턴트", "MBTI_추천": "ENTJ, ESTJ, INTJ", "홀랜드_추천": "진취형(E), 탐구형(I)", "창의성": 7, "논리분석력": 9, "대인관계": 8, "AI대체위험도": 6},
    {"직업명": "초중등 교사", "MBTI_추천": "ESFJ, ISFJ, ENFJ", "홀랜드_추천": "사회형(S), 관습형(C)", "창의성": 6, "논리분석력": 5, "대인관계": 9, "AI대체위험도": 3},
    {"직업명": "정보보안 전문가", "MBTI_추천": "INTJ, ISTJ, INTP", "홀랜드_추천": "탐구형(I), 관습형(C)", "창의성": 6, "논리분석력": 10, "대인관계": 3, "AI대체위험도": 2},
    {"직업명": "UI/UX 디자이너", "MBTI_추천": "INFP, ISFP, ENFP", "홀랜드_추천": "예술형(A), 탐구형(I)", "창의성": 9, "논리분석력": 6, "대인관계": 6, "AI대체위험도": 5},
]
df = pd.DataFrame(data)

# 3. 상단 2단 레이아웃 (MBTI 및 홀랜드 입력)
col1, col2 = st.columns(2)

with col1:
    st.subheader("🐰 1단계: 나의 MBTI 만들기")
    e_i = st.radio("에너지 방향", ["E (외향: 사람들과 어울림)", "I (내향: 혼자만의 시간)"], horizontal=True)
    s_n = st.radio("인식 방식", ["S (감각: 현실적, 꼼꼼함)", "N (직관: 상상력, 숲을 봄)"], horizontal=True)
    t_f = st.radio("판단 방식", ["T (사고: 논리적, 객관적)", "F (감정: 공감과 관계 중시)"], horizontal=True)
    j_p = st.radio("생활 양식", ["J (판단: 계획적, 체계적)", "P (인식: 융통성, 즉흥적)"], horizontal=True)
    
    my_mbti = e_i[0] + s_n[0] + t_f[0] + j_p[0]
    st.info(f"👉 조합된 나의 MBTI: **{my_mbti}**")

with col2:
    st.subheader("🐱 2단계: 나의 홀랜드 흥미 유형")
    st.write("나와 가장 잘 맞는 문장을 선택하세요.")
    st.checkbox("🛠️ (R) 몸을 움직이거나 기계를 다루는 게 좋다.")
    st.checkbox("🔬 (I) 현상의 원리를 파헤치고 분석하는 게 좋다.")
    st.checkbox("🎨 (A) 정해진 틀 없이 독창적으로 창작하는 게 좋다.")
    st.checkbox("🤝 (S) 다른 사람의 고민을 듣고 도와주는 게 좋다.")
    st.checkbox("🎤 (E) 목표를 세우고 사람들을 이끄는 게 좋다.")
    st.checkbox("📊 (C) 자료를 규칙에 맞게 꼼꼼히 정리하는 게 좋다.")

# 4. 데이터 매칭 및 탐구 시각화
st.divider()
st.subheader("📈 3단계: 직업 데이터 탐구 및 시각화")

if st.button("내 성향에 맞는 직업 데이터 불러오기", use_container_width=True):
    st.dataframe(df, use_container_width=True)
    
    sort_option = st.selectbox("📊 그래프 정렬 기준을 선택하여 비교해 보세요.", ["창의성", "논리분석력", "대인관계", "AI대체위험도"])
    df_sorted = df.sort_values(by=sort_option, ascending=False)
    
    fig = px.bar(df_sorted, x="직업명", y=sort_option, color="직업명", 
                 title=f"직업별 {sort_option} 비교", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# 5. 진로 로드맵 학습지 영역 (해설 포함)
st.divider()
st.subheader("📝 4단계: 나의 진로 로드맵 설계")

highschool_desc = {
    "일반고": "다양한 교과를 골고루 배우며 대학 진학을 준비하는 고등학교",
    "과학고/과학중점학급": "수학, 과학 분야 심화 이공계 전문 교육을 실시하는 학교",
    "외국어고/국제고": "외국어 능력 향상과 국제적 감각을 집중적으로 키우는 학교",
    "예술고/체육고": "음악, 미술, 무용, 체육 등 재능을 전문적으로 훈련하는 학교",
    "자사고": "자율적이고 특성화된 교육과정을 운영하는 학교",
    "직업계고": "졸업 후 전문 직업인으로 성장하기 위해 실무 중심의 기술을 배우는 학교"
}

major_desc = {
    "인문/사회계열": "언어, 문학, 경영, 언론 등 사회 현상을 연구하는 분야",
    "교육계열": "학생들을 가르치고 이끌어갈 교육 전문가를 양성하는 분야",
    "공학/자연계열": "수학, 과학, 컴퓨터, 기계 등 기술과 진리를 연구하는 분야",
    "의약계열": "의학, 약학, 간호학 등 인간의 생명과 건강을 다루는 분야",
    "예체능계열": "음악, 미술, 체육 등 창의성과 신체 능력을 발휘하는 분야"
}

selected_job = st.text_input("1. 위 데이터 탐구 결과를 바탕으로 가장 마음에 드는 직업 1개를 적어주세요.")
job_reason = st.text_area("2. 그 직업을 선택한 이유를 데이터(창의성, 논리성 등)에 근거하여 적어주세요.")

hs_choice = st.selectbox("3. 목표하는 고등학교 유형을 선택하세요.", list(highschool_desc.keys()))
st.info(f"🏫 **선택한 고등학교 특징:** {highschool_desc[hs_choice]}")

major_choice = st.selectbox("4. 목표하는 대학 계열을 선택하세요.", list(major_desc.keys()))
st.info(f"🎓 **선택한 대학 계열 특징:** {major_desc[major_choice]}")

action_plan = st.text_input("5. 이 목표를 위해 지금 당장 실천할 노력 1가지를 적어주세요.")

if st.button("✨ 나의 진로 로드맵 완성하기"):
    if selected_job and job_reason and action_plan:
        st.success("🎉 진로 로드맵이 완성되었습니다! 훌륭한 분석입니다.")
        with st.expander("결과 요약 카드 보기", expanded=True):
            st.markdown(f"**[목표 직업]** {selected_job}")
            st.markdown(f"**[선택 근거]** {job_reason}")
            st.markdown(f"**[진학 목표]** {hs_choice} ➡️ {major_choice}")
            st.markdown(f"**[액션 플랜]** {action_plan}")
    else:
        st.warning("빈칸을 모두 채워주세요.")