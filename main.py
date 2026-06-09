import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 추천소 ✨",
    page_icon="🌟",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ffdde1 0%, #ee9ca7 30%, #a1c4fd 70%, #c2e9fb 100%);
    color: #222;
}

.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 900;
    color: white;
    text-shadow: 3px 3px 8px rgba(0,0,0,0.25);
    margin-bottom: 0.3rem;
}

.sub-title {
    text-align: center;
    font-size: 1.3rem;
    color: white;
    margin-bottom: 2rem;
}

.card {
    background: rgba(255,255,255,0.85);
    padding: 25px;
    border-radius: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    margin-bottom: 20px;
}

.job-card {
    background: linear-gradient(135deg, #ffffff, #f8f9ff);
    padding: 20px;
    border-radius: 20px;
    border-left: 8px solid #ff7eb3;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    margin: 15px 0;
}

.big-emoji {
    font-size: 3rem;
    text-align: center;
}

.badge {
    display: inline-block;
    padding: 8px 14px;
    background: #ff7eb3;
    color: white;
    border-radius: 999px;
    font-weight: bold;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Data ----------------
mbti_data = {
    "INTJ": {
        "emoji": "🧠🚀",
        "title": "전략가형",
        "desc": "큰 그림을 보고 계획을 세우는 데 강해요. 혼자 깊이 생각하고 문제를 구조적으로 해결하는 스타일이에요.",
        "jobs": ["데이터 분석가 📊", "소프트웨어 개발자 💻", "연구원 🔬", "전략 컨설턴트 🧩", "건축가 🏛️"],
        "tip": "복잡한 문제를 분석하고 장기 계획을 세우는 활동을 해보면 좋아요."
    },
    "INTP": {
        "emoji": "🔍💡",
        "title": "논리탐구형",
        "desc": "궁금한 것을 파고들고 원리를 이해하는 데 강해요. 새로운 아이디어를 탐색하는 걸 좋아해요.",
        "jobs": ["과학자 🔬", "프로그래머 👨‍💻", "발명가 ⚙️", "철학자 📚", "게임 기획자 🎮"],
        "tip": "탐구 보고서, 코딩, 과학 실험처럼 생각을 확장하는 활동이 잘 맞아요."
    },
    "ENTJ": {
        "emoji": "👑📈",
        "title": "지휘관형",
        "desc": "목표를 정하고 사람들을 이끌어 성과를 내는 데 강해요. 리더십과 추진력이 돋보여요.",
        "jobs": ["CEO 🏢", "프로젝트 매니저 📋", "변호사 ⚖️", "정치인 🏛️", "마케팅 전략가 📣"],
        "tip": "토론, 발표, 팀 프로젝트 리더 역할을 경험해보면 좋아요."
    },
    "ENTP": {
        "emoji": "⚡🎤",
        "title": "아이디어 발명형",
        "desc": "새로운 생각을 제안하고 토론하는 걸 즐겨요. 변화와 도전을 좋아하는 스타일이에요.",
        "jobs": ["창업가 🚀", "광고 기획자 🎨", "방송인 🎙️", "기획자 🧠", "제품 디자이너 📱"],
        "tip": "창의적인 문제 해결 활동이나 모의 창업 프로젝트가 잘 맞아요."
    },
    "INFJ": {
        "emoji": "🌙🤝",
        "title": "통찰가형",
        "desc": "사람의 마음을 잘 이해하고 의미 있는 일을 추구해요. 조용하지만 깊은 영향력을 가진 타입이에요.",
        "jobs": ["상담사 🧡", "교사 👩‍🏫", "작가 ✍️", "심리학자 🧠", "사회복지사 🤲"],
        "tip": "누군가를 돕거나 글로 생각을 표현하는 활동을 해보면 좋아요."
    },
    "INFP": {
        "emoji": "🌷🎨",
        "title": "이상주의자형",
        "desc": "가치와 감성을 중요하게 생각해요. 자신만의 세계와 창의적인 표현력이 강해요.",
        "jobs": ["작가 ✍️", "일러스트레이터 🎨", "음악가 🎵", "상담사 💬", "콘텐츠 크리에이터 📸"],
        "tip": "글쓰기, 미술, 음악처럼 감정을 표현하는 활동이 잘 맞아요."
    },
    "ENFJ": {
        "emoji": "🌟🫶",
        "title": "선도자형",
        "desc": "사람들을 격려하고 함께 성장하도록 돕는 데 강해요. 따뜻한 리더십이 있어요.",
        "jobs": ["교사 👩‍🏫", "강연가 🎤", "상담가 💬", "인사 담당자 🧑‍💼", "사회운동가 🌍"],
        "tip": "멘토링, 발표, 봉사활동처럼 사람과 연결되는 경험이 좋아요."
    },
    "ENFP": {
        "emoji": "🌈🔥",
        "title": "재기발랄형",
        "desc": "열정과 상상력이 풍부해요. 사람들과 어울리며 새로운 가능성을 찾는 걸 좋아해요.",
        "jobs": ["크리에이터 🎬", "마케터 📣", "기자 📰", "배우 🎭", "이벤트 기획자 🎪"],
        "tip": "다양한 사람을 만나고 새로운 프로젝트를 시도해보면 좋아요."
    },
    "ISTJ": {
        "emoji": "📘✅",
        "title": "책임관리형",
        "desc": "꼼꼼하고 책임감이 강해요. 규칙과 계획을 바탕으로 안정적으로 일하는 데 강해요.",
        "jobs": ["공무원 🏢", "회계사 💰", "법무사 ⚖️", "품질관리자 🔎", "행정 전문가 📑"],
        "tip": "자료 정리, 계획 세우기, 규칙 기반 업무를 경험해보면 좋아요."
    },
    "ISFJ": {
        "emoji": "🧸🌼",
        "title": "따뜻한 보호자형",
        "desc": "다른 사람을 세심하게 챙기고 책임감 있게 도와주는 스타일이에요.",
        "jobs": ["간호사 🏥", "교사 👩‍🏫", "사회복지사 🤲", "영양사 🍱", "도서관 사서 📚"],
        "tip": "돌봄, 교육, 봉사와 관련된 활동을 해보면 좋아요."
    },
    "ESTJ": {
        "emoji": "📋🏆",
        "title": "실행관리형",
        "desc": "현실적이고 체계적이에요. 조직을 관리하고 목표를 완수하는 데 강해요.",
        "jobs": ["관리자 🧑‍💼", "경찰관 👮", "군인 🎖️", "경영자 🏢", "행정가 📑"],
        "tip": "역할 분담이 필요한 팀 활동에서 강점을 발견할 수 있어요."
    },
    "ESFJ": {
        "emoji": "🎀🤗",
        "title": "친화도움형",
        "desc": "사람들과 잘 어울리고 분위기를 따뜻하게 만드는 데 강해요.",
        "jobs": ["교사 👩‍🏫", "간호사 🏥", "서비스 매니저 🛎️", "상담사 💬", "홍보 담당자 📣"],
        "tip": "협동 활동, 봉사활동, 행사 운영 경험이 잘 맞아요."
    },
    "ISTP": {
        "emoji": "🛠️🏍️",
        "title": "문제해결형",
        "desc": "손으로 직접 만들고 고치는 활동에 강해요. 현실적인 해결 능력이 뛰어나요.",
        "jobs": ["엔지니어 ⚙️", "정비사 🚗", "파일럿 ✈️", "응급구조사 🚑", "스포츠 선수 🏅"],
        "tip": "실습, 제작, 도구를 활용하는 활동을 해보면 좋아요."
    },
    "ISFP": {
        "emoji": "🎨🌿",
        "title": "감성예술형",
        "desc": "감각적이고 섬세해요. 아름다움과 자유로운 표현을 중요하게 생각해요.",
        "jobs": ["디자이너 👗", "사진작가 📷", "요리사 👨‍🍳", "음악가 🎵", "플로리스트 🌸"],
        "tip": "미술, 사진, 요리처럼 감각을 활용하는 활동이 잘 맞아요."
    },
    "ESTP": {
        "emoji": "🏃‍♂️🔥",
        "title": "활동도전형",
        "desc": "에너지가 넘치고 현실 감각이 좋아요. 빠르게 판단하고 행동하는 데 강해요.",
        "jobs": ["사업가 💼", "운동선수 🏅", "경찰관 👮", "영업 전문가 🤝", "응급구조사 🚑"],
        "tip": "현장 체험, 스포츠, 발표 활동에서 강점을 찾을 수 있어요."
    },
    "ESFP": {
        "emoji": "🎉🎭",
        "title": "분위기메이커형",
        "desc": "사람들과 함께 즐겁게 활동하는 걸 좋아해요. 표현력과 친화력이 뛰어나요.",
        "jobs": ["배우 🎭", "MC 🎤", "관광 가이드 🧳", "이벤트 기획자 🎪", "뷰티 전문가 💄"],
        "tip": "무대 활동, 발표, 행사 기획처럼 표현하는 경험이 좋아요."
    },
}

# ---------------- UI ----------------
st.markdown('<div class="main-title">🌟 MBTI 진로 추천소 🌟</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">나의 성향에 어울리는 미래 직업을 찾아보자! 🚀✨</div>', unsafe_allow_html=True)

left, right = st.columns([1, 2])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🧭 MBTI 선택하기")
    selected = st.selectbox(
        "나의 MBTI는?",
        list(mbti_data.keys())
    )

    st.write("👇 선택한 MBTI")
    st.markdown(f"""
    <div class="big-emoji">{mbti_data[selected]["emoji"]}</div>
    <h2 style="text-align:center;">{selected}</h2>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    data = mbti_data[selected]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"## {data['emoji']} {selected} : {data['title']}")
    st.write(data["desc"])

    st.markdown("### ✨ 추천 직업")
    for job in data["jobs"]:
        st.markdown(f"""
        <div class="job-card">
            <h3>{job}</h3>
            <p>이 MBTI의 성향과 잘 어울리는 진로 후보예요. 물론 인간은 16칸짜리 표에 다 들어가지 않지만, 교육용으로는 꽤 쓸 만하죠.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🎯 진로 탐색 팁")
    st.info(data["tip"])

    st.markdown("### 🌱 나에게 해볼 질문")
    st.markdown("""
    <span class="badge">나는 어떤 활동을 할 때 시간이 빨리 갈까?</span>
    <span class="badge">사람과 함께할 때 에너지가 생길까?</span>
    <span class="badge">혼자 깊이 생각하는 일이 좋을까?</span>
    <span class="badge">만들기, 표현하기, 분석하기 중 무엇이 좋을까?</span>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<div class="card">
<h2>💡 진로 교육 안내</h2>
<p>
MBTI는 진로를 결정하는 절대적인 기준이 아니에요.  
자신의 흥미, 가치관, 능력, 경험을 함께 생각해야 더 좋은 선택을 할 수 있어요.  
그러니까 MBTI 하나로 인생을 정하려는 인간의 대담함은 잠시 내려놓고, 다양한 체험을 해봅시다. 🌈
</p>
</div>
""", unsafe_allow_html=True)
