import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 및 테마 설정
st.set_page_config(page_title="나의 진로 나침반", page_icon="🐹", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #FFF5F7; } 
    h1, h2, h3, h4 { color: #FF8E9E !important; } 
    .stButton>button { background-color: #A3D8F4; color: #333; border-radius: 20px; border: none; font-weight: bold; }
    div[data-testid="stExpander"] { background-color: #FFFFFF; border-radius: 15px; border: 2px solid #FFE4E1; }
    </style>
""", unsafe_allow_html=True)

st.title("🐹 나의 진로 나침반 (심화 탐구 학습지)")

st.warning("""
**⚠️ 브라우저 자동 번역 기능 사용 주의 안내**  
본 애플리케이션은 한국어 환경에 맞춰 제작되었습니다. 브라우저의 '자동 번역' 기능이 활성화되어 있을 경우, 화면의 문장이나 선택지가 왜곡되어 잘못 표기될 수 있습니다. 정상적인 이용을 위해 주소창 우측의 번역 아이콘을 눌러 반드시 **'영어(원본)'** 상태로 유지해 주시기 바랍니다.
""")

st.write("나의 성향을 정밀하게 분석하고 직업별 지표를 비교하여 진로 로드맵을 완성해 보세요!")
st.divider()

# 2. 내부 데이터베이스 (50개 직업 풀)
data = [
    {"직업명": "소프트웨어 개발자", "MBTI_추천": "INTJ, INTP, ISTP, ENTJ", "홀랜드_추천": "I, R", "창의성": 8, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 4},
    {"직업명": "데이터 사이언티스트", "MBTI_추천": "INTJ, INTP, ENTJ, ISTJ", "홀랜드_추천": "I, C", "창의성": 7, "논리분석력": 10, "대인관계": 5, "AI대체위험도": 2},
    {"직업명": "인공지능 연구원", "MBTI_추천": "INTP, INTJ, ENTJ, ENTP", "홀랜드_추천": "I, R", "창의성": 9, "논리분석력": 10, "대인관계": 4, "AI대체위험도": 1},
    {"직업명": "정보보안 전문가", "MBTI_추천": "INTJ, ISTJ, INTP, ISTP", "홀랜드_추천": "I, C", "창의성": 6, "논리분석력": 10, "대인관계": 3, "AI대체위험도": 2},
    {"직업명": "클라우드 아키텍트", "MBTI_추천": "ENTJ, INTJ, ISTJ, ESTJ", "홀랜드_추천": "I, C, E", "창의성": 7, "논리분석력": 9, "대인관계": 6, "AI대체위험도": 3},
    {"직업명": "게임 개발자", "MBTI_추천": "ENTP, INTP, ENFP, ISTP", "홀랜드_추천": "I, A", "창의성": 9, "논리분석력": 8, "대인관계": 6, "AI대체위험도": 4},
    {"직업명": "기계 공학자", "MBTI_추천": "ISTJ, ISTP, ESTJ, INTJ", "홀랜드_추천": "R, I", "창의성": 6, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 5},
    {"직업명": "전자 공학자", "MBTI_추천": "ISTJ, INTP, INTJ, ISTP", "홀랜드_추천": "R, I", "창의성": 6, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 4},
    {"직업명": "로봇 공학자", "MBTI_추천": "INTP, INTJ, ENTJ, ENTP", "홀랜드_추천": "I, R", "창의성": 8, "논리분석력": 9, "대인관계": 5, "AI대체위험도": 2},
    {"직업명": "생명공학 연구원", "MBTI_추천": "INTJ, INTP, INFJ, ISTJ", "홀랜드_추천": "I, R", "창의성": 7, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 3},
    {"직업명": "환경 공학자", "MBTI_추천": "INFJ, INTJ, ENFJ, ISTJ", "홀랜드_추천": "I, S", "창의성": 6, "논리분석력": 8, "대인관계": 6, "AI대체위험도": 4},
    {"직업명": "화학 공학자", "MBTI_추천": "ISTJ, INTJ, ESTJ, INTP", "홀랜드_추천": "I, R", "창의성": 6, "논리분석력": 9, "대인관계": 4, "AI대체위험도": 4},
    {"직업명": "항공우주 공학자", "MBTI_추천": "INTJ, ENTJ, INTP, ISTP", "홀랜드_추천": "I, R", "창의성": 8, "논리분석력": 10, "대인관계": 5, "AI대체위험도": 3},
    {"직업명": "UI/UX 디자이너", "MBTI_추천": "INFP, ISFP, ENFP, INFJ", "홀랜드_추천": "A, I", "창의성": 9, "논리분석력": 6, "대인관계": 6, "AI대체위험도": 6},
    {"직업명": "시각 디자이너", "MBTI_추천": "ISFP, INFP, ENFP, ESFP", "홀랜드_추천": "A, R", "창의성": 10, "논리분석력": 4, "대인관계": 5, "AI대체위험도": 7},
    {"직업명": "인테리어 디자이너", "MBTI_추천": "ISFP, ENFJ, ESFP, ISTP", "홀랜드_추천": "A, R, E", "창의성": 9, "논리분석력": 5, "대인관계": 7, "AI대체위험도": 5},
    {"직업명": "방송 PD", "MBTI_추천": "ENTP, ENFP, ENTJ, ESTP", "홀랜드_추천": "A, E", "창의성": 9, "논리분석력": 7, "대인관계": 8, "AI대체위험도": 3},
    {"직업명": "영화 감독", "MBTI_추천": "ENTP, INFJ, ENFJ, INTJ", "홀랜드_추천": "A, E", "창의성": 10, "논리분석력": 6, "대인관계": 9, "AI대체위험도": 2},
    {"직업명": "콘텐츠 크리에이터", "MBTI_추천": "ENFP, ENTP, INFP, ESFP", "홀랜드_추천": "A, E", "창의성": 10, "논리분석력": 4, "대인관계": 7, "AI대체위험도": 4},
    {"직업명": "웹툰 작가", "MBTI_추천": "INFP, ISFP, INTP, ENFP", "홀랜드_추천": "A, I", "창의성": 10, "논리분석력": 4, "대인관계": 2, "AI대체위험도": 6},
    {"직업명": "마케팅 전문가", "MBTI_추천": "ENFJ, ESTJ, ENTJ, ESFJ", "홀랜드_추천": "E, S", "창의성": 8, "논리분석력": 6, "대인관계": 9, "AI대체위험도": 5},
    {"직업명": "광고 기획자(AE)", "MBTI_추천": "ENTP, ENFP, ENTJ, ESTP", "홀랜드_추천": "E, A", "창의성": 9, "논리분석력": 7, "대인관계": 9, "AI대체위험도": 4},
    {"직업명": "경영 컨설턴트", "MBTI_추천": "ENTJ, ESTJ, INTJ, ENTP", "홀랜드_추천": "E, I", "창의성": 7, "논리분석력": 9, "대인관계": 8, "AI대체위험도": 5},
    {"직업명": "인사(HR) 담당자", "MBTI_추천": "ESFJ, ENFJ, ISFJ, INFJ", "홀랜드_추천": "S, E, C", "창의성": 5, "논리분석력": 6, "대인관계": 10, "AI대체위험도": 6},
    {"직업명": "회계사", "MBTI_추천": "ISTJ, ESTJ, INTJ, ISFJ", "홀랜드_추천": "C, I", "창의성": 3, "논리분석력": 9, "대인관계": 5, "AI대체위험도": 8},
    {"직업명": "세무사", "MBTI_추천": "ISTJ, ESTJ, ISFJ, INTJ", "홀랜드_추천": "C, E", "창의성": 3, "논리분석력": 9, "대인관계": 6, "AI대체위험도": 8},
    {"직업명": "재무 분석가", "MBTI_추천": "ISTJ, INTJ, ESTJ, ENTJ", "홀랜드_추천": "C, I", "창의성": 4, "논리분석력": 10, "대인관계": 5, "AI대체위험도": 7},
    {"직업명": "무역 중개인", "MBTI_추천": "ESTP, ENTJ, ENFJ, ESTJ", "홀랜드_추천": "E, C", "창의성": 5, "논리분석력": 7, "대인관계": 9, "AI대체위험도": 6},
    {"직업명": "영업 관리자", "MBTI_추천": "ESTJ, ESFJ, ENTJ, ENFJ", "홀랜드_추천": "E, S", "창의성": 5, "논리분석력": 6, "대인관계": 10, "AI대체위험도": 5},
    {"직업명": "초중등 교사", "MBTI_추천": "ESFJ, ISFJ, ENFJ, INFJ", "홀랜드_추천": "S, C", "창의성": 6, "논리분석력": 5, "대인관계": 9, "AI대체위험도": 3},
    {"직업명": "유치원 교사", "MBTI_추천": "ESFJ, ISFJ, ENFP, ESFP", "홀랜드_추천": "S, A", "창의성": 7, "논리분석력": 4, "대인관계": 10, "AI대체위험도": 2},
    {"직업명": "특수 교사", "MBTI_추천": "INFJ, ISFJ, ENFJ, INFP", "홀랜드_추천": "S, I", "창의성": 6, "논리분석력": 6, "대인관계": 10, "AI대체위험도": 1},
    {"직업명": "상담 심리사", "MBTI_추천": "INFJ, INFP, ENFJ, ISFJ", "홀랜드_추천": "S, A", "창의성": 5, "논리분석력": 6, "대인관계": 10, "AI대체위험도": 1},
    {"직업명": "임상 심리사", "MBTI_추천": "INFJ, INTJ, INTP, INFP", "홀랜드_추천": "I, S", "창의성": 5, "논리분석력": 9, "대인관계": 9, "AI대체위험도": 2},
    {"직업명": "사회복지사", "MBTI_추천": "ESFJ, ISFJ, ENFJ, INFJ", "홀랜드_추천": "S, E", "창의성": 5, "논리분석력": 5, "대인관계": 10, "AI대체위험도": 2},
    {"직업명": "의사", "MBTI_추천": "ISTJ, INTJ, ESTJ, ISFJ", "홀랜드_추천": "I, S", "창의성": 5, "논리분석력": 10, "대인관계": 8, "AI대체위험도": 4},
    {"직업명": "간호사", "MBTI_추천": "ISFJ, ESFJ, INFJ, ISTJ", "홀랜드_추천": "S, R", "창의성": 4, "논리분석력": 7, "대인관계": 9, "AI대체위험도": 2},
    {"직업명": "물리치료사", "MBTI_추천": "ISFJ, ISTJ, ESFJ, ISFP", "홀랜드_추천": "S, R", "창의성": 4, "논리분석력": 6, "대인관계": 9, "AI대체위험도": 2},
    {"직업명": "수의사", "MBTI_추천": "ISTJ, INFP, ISFJ, INTJ", "홀랜드_추천": "I, R", "창의성": 4, "논리분석력": 9, "대인관계": 6, "AI대체위험도": 3},
    {"직업명": "요리사/셰프", "MBTI_추천": "ISTP, ISFP, ESTP, ESFP", "홀랜드_추천": "R, A", "창의성": 9, "논리분석력": 5, "대인관계": 6, "AI대체위험도": 5},
    {"직업명": "호텔리어", "MBTI_추천": "ESFJ, ISFJ, ENFJ, ESTP", "홀랜드_추천": "S, E", "창의성": 4, "논리분석력": 5, "대인관계": 10, "AI대체위험도": 6},
    {"직업명": "승무원", "MBTI_추천": "ESFJ, ENFJ, ESFP, ISFJ", "홀랜드_추천": "S, E", "창의성": 4, "논리분석력": 5, "대인관계": 10, "AI대체위험도": 6},
    {"직업명": "스포츠 마케터", "MBTI_추천": "ESTP, ESFP, ENTJ, ENFJ", "홀랜드_추천": "E, R", "창의성": 7, "논리분석력": 5, "대인관계": 9, "AI대체위험도": 5},
    {"직업명": "이벤트 기획자", "MBTI_추천": "ENFP, ENFJ, ESTP, ESFJ", "홀랜드_추천": "E, A", "창의성": 9, "논리분석력": 6, "대인관계": 9, "AI대체위험도": 4},
    {"직업명": "경찰관", "MBTI_추천": "ESTJ, ISTJ, ESTP, ESFJ", "홀랜드_추천": "R, S, E", "창의성": 4, "논리분석력": 7, "대인관계": 8, "AI대체위험도": 4},
    {"직업명": "소방관", "MBTI_추천": "ISTP, ESTP, ISFJ, ESTJ", "홀랜드_추천": "R, S", "창의성": 3, "논리분석력": 6, "대인관계": 8, "AI대체위험도": 2},
    {"직업명": "행정 공무원", "MBTI_추천": "ISTJ, ISFJ, ESTJ, ESFJ", "홀랜드_추천": "C, S", "창의성": 3, "논리분석력": 6, "대인관계": 7, "AI대체위험도": 7},
    {"직업명": "외교관", "MBTI_추천": "ENFJ, ENTJ, INFJ, INTJ", "홀랜드_추천": "E, S, I", "창의성": 6, "논리분석력": 9, "대인관계": 9, "AI대체위험도": 3},
    {"직업명": "변호사", "MBTI_추천": "ENTJ, INTJ, ESTJ, ENTP", "홀랜드_추천": "E, I, C", "창의성": 6, "논리분석력": 10, "대인관계": 8, "AI대체위험도": 5},
    {"직업명": "언론인(기자)", "MBTI_추천": "ENFP, ENTP, INFJ, ENTJ", "홀랜드_추천": "I, A, E", "창의성": 7, "논리분석력": 9, "대인관계": 8, "AI대체위험도": 6},
]
df = pd.DataFrame(data)

# 상태 저장을 위한 session_state 초기화
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

# 3. 상단 2단 레이아웃
col1, col2 = st.columns(2)

with col1:
    st.subheader("🐰 1단계: 정밀 MBTI 진단")
    with st.expander("📝 에너지 방향 (E/I)", expanded=True):
        ei_1 = st.radio("새로운 친구들을 만나는 자리에 가면?", ["E 다가가서 말을 건다.", "I 조용히 분위기를 파악한다."], index=0)
        ei_2 = st.radio("스트레스를 풀 때?", ["E 밖으로 나가 사람들을 만난다.", "I 혼자만의 시간을 보낸다."], index=0)
    with st.expander("📝 인식 방식 (S/N)", expanded=True):
        sn_1 = st.radio("과제를 할 때?", ["S 세부 내용을 확인한다.", "N 큰 그림을 본다."], index=0)
        sn_2 = st.radio("미래 상상?", ["S 실현 가능한 것을 생각한다.", "N 엉뚱한 상상을 한다."], index=0)
    with st.expander("📝 판단 방식 (T/F)", expanded=True):
        tf_1 = st.radio("친구가 고민을 털어놓을 때?", ["T 원인을 분석한다.", "F 깊이 공감해 준다."], index=0)
        tf_2 = st.radio("의사결정 시?", ["T 논리와 공정성", "F 사람들과의 관계와 조화"], index=0)
    with st.expander("📝 생활 양식 (J/P)", expanded=True):
        jp_1 = st.radio("여행을 갈 때?", ["J 계획표를 세운다.", "P 즉흥적으로 다닌다."], index=0)
        jp_2 = st.radio("일 처리?", ["J 미리미리 끝낸다.", "P 마감일 직전에 몰아서 한다."], index=0)
    
    my_e = "E" if (ei_1.startswith("E") or ei_2.startswith("E")) else "I"
    my_s = "S" if (sn_1.startswith("S") or sn_2.startswith("S")) else "N"
    my_t = "T" if (tf_1.startswith("T") or tf_2.startswith("T")) else "F"
    my_j = "J" if (jp_1.startswith("J") or jp_2.startswith("J")) else "P"
    my_mbti = my_e + my_s + my_t + my_j
    st.info(f"👉 심층 분석된 나의 MBTI: **{my_mbti}**")

with col2:
    st.subheader("🐱 2단계: 다면적 홀랜드 흥미 유형")
    st.write("평소 나와 가장 잘 맞는 문장을 모두 체크하세요.")
    
    st.markdown("**[R] 현실형**")
    r1 = st.checkbox("🛠️ 기계나 도구를 조립하고 고치는 것을 좋아한다.")
    r2 = st.checkbox("🏃‍♂️ 몸을 움직이는 야외 활동이나 스포츠가 즐겁다.")
    st.markdown("**[I] 탐구형**")
    i1 = st.checkbox("🔬 현상의 원리를 파헤치고 분석하는 게 좋다.")
    i2 = st.checkbox("📚 다큐멘터리를 보거나 호기심을 끝까지 탐구한다.")
    st.markdown("**[A] 예술형**")
    a1 = st.checkbox("🎨 정해진 틀 없이 독창적으로 창작하는 게 좋다.")
    a2 = st.checkbox("🎵 음악, 미술, 디자인 등 나만의 개성을 표현하고 싶다.")
    st.markdown("**[S] 사회형**")
    s1 = st.checkbox("🤝 다른 사람의 고민을 듣고 도와주는 게 좋다.")
    s2 = st.checkbox("🧑‍🏫 내가 아는 것을 다른 사람에게 가르쳐주는 게 뿌듯하다.")
    st.markdown("**[E] 진취형**")
    e1 = st.checkbox("🎤 목표를 세우고 사람들을 이끌어 성과를 내는 게 좋다.")
    e2 = st.checkbox("💡 새로운 프로젝트를 기획하고 사람들을 설득하는 일에 자신 있다.")
    st.markdown("**[C] 관습형**")
    c1 = st.checkbox("📊 자료를 규칙에 맞게 꼼꼼히 정리하는 게 편하다.")
    c2 = st.checkbox("📝 숫자를 다루거나 정해진 원칙에 따라 정확하게 일하는 게 좋다.")
    
    my_holland = []
    if r1 or r2: my_holland.append("R")
    if i1 or i2: my_holland.append("I")
    if a1 or a2: my_holland.append("A")
    if s1 or s2: my_holland.append("S")
    if e1 or e2: my_holland.append("E")
    if c1 or c2: my_holland.append("C")

# 4. 데이터 매칭 및 탐구 시각화
st.divider()
st.subheader("📈 3단계: 맞춤형 데이터 탐구 및 시각화")

if st.button("내 성향에 맞는 직업 데이터 불러오기", use_container_width=True):
    st.session_state.data_loaded = True

if st.session_state.data_loaded:
    
    def calculate_match_score(row):
        score = 0
        if my_mbti in row["MBTI_추천"]:
            score += 30
        job_hollands = [h.strip() for h in row["홀랜드_추천"].split(",")]
        for h in my_holland:
            if h in job_hollands:
                if h == job_hollands[0]:  
                    score += 50
                else:                     
                    score += 20
        return score
    
    # 적합도 종합점수 추가 및 정렬
    df['적합도 종합점수'] = df.apply(calculate_match_score, axis=1)
    
    if df['적합도 종합점수'].max() == 0:
        st.warning("⚠️ 2단계 홀랜드 흥미 유형을 1개 이상 체크해 주세요.")
    else:
        df_matched = df.sort_values(by='적합도 종합점수', ascending=False).head(5)
        
        # 데이터프레임 노출 전 컬럼명 정리 및 재배치
        display_df = df_matched.drop(columns=['MBTI_추천', '홀랜드_추천']).reset_index(drop=True)
        cols = ['직업명', '적합도 종합점수', '창의성', '논리분석력', '대인관계', 'AI대체위험도']
        display_df = display_df[cols]
        
        st.dataframe(display_df, use_container_width=True)
        
        # 종합점수를 기본 정렬 기준으로 추가
        sort_option = st.selectbox("📊 그래프 정렬 기준을 선택하여 비교해 보세요.", 
                                   ["적합도 종합점수", "창의성", "논리분석력", "대인관계", "AI대체위험도"])
        
        df_sorted = display_df.sort_values(by=sort_option, ascending=False)
        
        fig = px.bar(df_sorted, x="직업명", y=sort_option, color="직업명", 
                     title=f"추천 직업 TOP5의 {sort_option} 비교", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        
        if len(df_sorted) > 1:
            top1_job = df_sorted.iloc[0]['직업명']
            top2_job = df_sorted.iloc[1]['직업명']
            
            desc_map = {
                "적합도 종합점수": "입력하신 MBTI와 홀랜드 흥미 유형을 합산한 최종 매칭 점수입니다. 점수가 높을수록 본인의 성향과 가장 완벽하게 부합하는 직업임을 의미합니다.",
                "창의성": "새로운 아이디어를 기획하고, 무에서 유를 창조하는 유연한 사고력이 가장 중요함을 의미합니다.",
                "논리분석력": "복잡한 원리를 파악하고 객관적 데이터로 문제를 해결하는 역량이 핵심 요구사항임을 뜻합니다.",
                "대인관계": "타인과 소통하고 공감하며, 팀워크를 이끌어가는 능력이 업무의 성패를 좌우합니다.",
                "AI대체위험도": "이 수치가 높을수록 정형화되고 반복적인 업무 비중이 커, 향후 AI 기술로 대체될 확률이 상대적으로 높음을 시사합니다. 미래 진로 선택 시 주의가 필요합니다."
            }
            
            st.success(f"**💡 [데이터 분석 인사이트]**\n\n선택하신 **'{sort_option}'** 지표를 기준으로 볼 때, 추천된 직업 중 **{top1_job}**와(과) **{top2_job}**이(가) 가장 최상위권에 위치합니다. 이는 해당 직무에서 {desc_map[sort_option]}")

        st.info("""
        **📊 데이터 산출 근거 및 공식 출처 안내 (Reference)**
        * **직무별 요구 역량:** 한국고용정보원(KEIS) 직무 역량 데이터 (2024), 미국 노동부 O*NET Database 28.0 (2023-2024)
        * **AI 대체 위험도:** 세계경제포럼(WEF) 미래 일자리 보고서 (2023), 한국고용정보원 연구 보고서 (2023)
        """)

# 5. 진로 로드맵 학습지 영역
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