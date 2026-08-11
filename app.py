import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io
from datetime import datetime


# ============================================================
# NOURIVA AI — FINAL SINGLE-FILE APP
# ============================================================

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "screening" not in st.session_state:
    st.session_state.screening = None

if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = None

if "coach_history" not in st.session_state:
    st.session_state.coach_history = []

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

if "growth_result" not in st.session_state:
    st.session_state.growth_result = None

if "food_result" not in st.session_state:
    st.session_state.food_result = None


# ============================================================
# NAVIGATION
# ============================================================

NAV_ITEMS = [
    ("Dashboard", "🏠"),
    ("Nutrition Scan", "🔍"),
    ("Diet Planner", "🍽️"),
    ("Nutrition Coach", "🤖"),
    ("Education", "📚"),
    ("Nutrition Insights", "📊"),
    ("Growth Monitor", "🧒"),
    ("Food Scanner", "📷"),
    ("Global Nutrition", "🌍"),
    ("Health Report", "📄"),
    ("About", "ℹ️"),
]


def go(page):
    st.session_state.page = page
    st.rerun()


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 5% 0%, rgba(32,190,132,.10), transparent 25%),
        radial-gradient(circle at 95% 5%, rgba(60,130,255,.08), transparent 25%),
        #f7faf9;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 1.2rem;
    padding-bottom: 4rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* BRAND */

.brand {
    display:flex;
    align-items:center;
    gap:12px;
    margin-bottom:20px;
}

.brand-icon {
    width:46px;
    height:46px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#0b5c40,#21b77e);
    color:white;
    font-size:25px;
    box-shadow:0 8px 22px rgba(11,92,64,.20);
}

.brand-name {
    font-size:24px;
    font-weight:850;
    color:#123b2e;
    line-height:1;
}

.brand-sub {
    color:#75827c;
    font-size:12px;
    margin-top:4px;
}

/* NAV */

.nav-wrap {
    background:white;
    border:1px solid #e0ebe6;
    border-radius:18px;
    padding:7px;
    margin-bottom:25px;
    box-shadow:0 5px 20px rgba(18,55,43,.045);
}

/* HERO */

.hero {
    position:relative;
    overflow:hidden;
    padding:45px;
    border-radius:30px;
    background:
        radial-gradient(circle at 85% 20%,rgba(255,255,255,.18),transparent 24%),
        linear-gradient(135deg,#073c2b,#0b694a,#19a974);
    color:white;
    box-shadow:0 18px 45px rgba(11,82,57,.18);
    margin-bottom:30px;
}

.hero h1 {
    font-size:clamp(34px,5vw,54px);
    line-height:1.05;
    margin:0 0 12px 0;
}

.hero p {
    max-width:760px;
    font-size:17px;
    line-height:1.65;
    opacity:.93;
}

.hero-label {
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:.1em;
    font-weight:800;
    opacity:.8;
    margin-bottom:12px;
}

/* TITLES */

.section-title {
    font-size:28px;
    font-weight:850;
    color:#173b2f;
    margin-top:30px;
    margin-bottom:5px;
}

.section-sub {
    color:#748078;
    margin-bottom:20px;
}

/* CARDS */

.card {
    background:white;
    border:1px solid #e0ebe6;
    border-radius:22px;
    padding:24px;
    min-height:175px;
    box-shadow:0 7px 24px rgba(18,55,43,.05);
    margin-bottom:18px;
}

.card h3 {
    color:#123f30;
    margin-top:0;
}

.card p {
    color:#68766f;
    line-height:1.6;
}

/* ICON */

.icon {
    width:50px;
    height:50px;
    border-radius:16px;
    background:#edf8f3;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:25px;
    margin-bottom:14px;
}

/* METRICS */

.metric {
    background:white;
    border:1px solid #e0ebe6;
    border-radius:20px;
    padding:20px;
    box-shadow:0 7px 22px rgba(18,55,43,.045);
}

.metric-label {
    color:#78847e;
    font-size:13px;
}

.metric-value {
    color:#123f30;
    font-size:28px;
    font-weight:850;
    margin-top:6px;
}

/* RESULT */

.result {
    background:white;
    border:1px solid #dce9e3;
    border-left:6px solid #159467;
    border-radius:20px;
    padding:24px;
    box-shadow:0 8px 26px rgba(18,55,43,.055);
    margin:18px 0;
}

/* DARK */

.dark-card {
    background:linear-gradient(135deg,#103e30,#17664b);
    color:white;
    border-radius:24px;
    padding:28px;
    box-shadow:0 12px 30px rgba(16,62,48,.15);
}

.dark-card h2,
.dark-card h3 {
    color:white;
}

/* LESSON */

.lesson {
    background:white;
    border:1px solid #e0ebe6;
    border-radius:22px;
    padding:28px;
    box-shadow:0 7px 24px rgba(18,55,43,.05);
}

.lesson-tag {
    color:#149466;
    font-size:12px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:.08em;
}

/* FOOTER */

.footer {
    text-align:center;
    color:#7b8580;
    padding:35px 10px 10px;
    font-size:13px;
}

/* BUTTONS */

.stButton > button,
.stDownloadButton > button {
    border-radius:13px !important;
    min-height:44px !important;
    font-weight:700 !important;
}

/* INPUTS */

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    border-radius:12px !important;
}

/* MOBILE */

@media(max-width:700px) {

    .main .block-container {
        padding-left:1rem;
        padding-right:1rem;
    }

    .hero {
        padding:28px 22px;
        border-radius:23px;
    }

    .hero p {
        font-size:15px;
    }

    .brand-name {
        font-size:21px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# TOP BRAND
# ============================================================

st.markdown(
    """
<div class="brand">
    <div class="brand-icon">🌿</div>
    <div>
        <div class="brand-name">Nouriva AI</div>
        <div class="brand-sub">Nutrition • Education • Awareness</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGATION BAR
# ============================================================

with st.container():
    nav_cols = st.columns(6)

    visible_nav = [
        ("Dashboard", "🏠"),
        ("Nutrition Scan", "🔍"),
        ("Diet Planner", "🍽️"),
        ("Education", "📚"),
        ("Nutrition Coach", "🤖"),
        ("More", "☰"),
    ]

    for i, (name, icon) in enumerate(visible_nav):

        with nav_cols[i]:

            if name == "More":

                with st.popover("☰ More"):

                    for page_name, page_icon in NAV_ITEMS:

                        if page_name in [
                            "Dashboard",
                            "Nutrition Scan",
                            "Diet Planner",
                            "Education",
                            "Nutrition Coach",
                        ]:
                            continue

                        if st.button(
                            f"{page_icon} {page_name}",
                            key=f"nav_{page_name}",
                            use_container_width=True,
                        ):
                            go(page_name)

            else:

                if st.button(
                    f"{icon} {name}",
                    key=f"top_{name}",
                    use_container_width=True,
                ):
                    go(name)


# ============================================================
# COMMON HELPERS
# ============================================================

def bmi(height, weight):
    if height <= 0:
        return 0
    m = height / 100
    return round(weight / (m * m), 1)


def bmi_category(value):
    if value < 18.5:
        return "Below standard adult BMI range"
    if value < 25:
        return "Standard adult BMI range"
    if value < 30:
        return "Above standard adult BMI range"
    return "High adult BMI range"


def calculate_risk(age, bmi_value, meals, protein, fruits, access):

    score = 0
    factors = []

    if age >= 18 and bmi_value < 18.5:
        score += 2
        factors.append("BMI below standard adult screening range.")

    if age >= 18 and bmi_value >= 30:
        score += 1
        factors.append("BMI in a high adult screening range.")

    if meals <= 2:
        score += 1
        factors.append("Low reported meal frequency.")

    if not protein:
        score += 1
        factors.append("No protein source selected.")

    if fruits == "Rarely":
        score += 1
        factors.append("Low reported fruit and vegetable intake.")

    if access == "Often difficult":
        score += 2
        factors.append("Reported difficulty accessing sufficient food.")

    elif access == "Sometimes difficult":
        score += 1
        factors.append("Occasional difficulty accessing sufficient food.")

    if score >= 5:
        level = "Higher potential risk factors"
    elif score >= 3:
        level = "Several potential risk factors"
    elif score >= 1:
        level = "Some potential risk factors"
    else:
        level = "Few identified risk factors"

    return score, level, factors


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        """
<div class="hero">
    <div class="hero-label">Student Health-Technology Prototype • 2026</div>
    <h1>🌿 Nouriva AI</h1>
    <p>
        AI-assisted nutrition screening, education, meal planning,
        growth awareness and global nutrition learning — brought together
        in one accessible platform.
    </p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Your Nutrition Hub</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Choose a tool and start exploring.</div>',
        unsafe_allow_html=True,
    )

    tools = [
        (
            "Nutrition Scan",
            "🔍",
            "Calculate BMI and explore preliminary nutrition-related indicators.",
        ),
        (
            "Diet Planner",
            "🍽️",
            "Build practical example meals around a general nutrition goal.",
        ),
        (
            "Nutrition Coach",
            "🤖",
            "Ask general nutrition education questions.",
        ),
        (
            "Education",
            "📚",
            "Learn through structured lessons, key points and quizzes.",
        ),
        (
            "Nutrition Insights",
            "📊",
            "Explore nutrition indicators, charts and SDG connections.",
        ),
        (
            "Growth Monitor",
            "🧒",
            "Explore age- and sex-specific growth assessment concepts.",
        ),
        (
            "Food Scanner",
            "📷",
            "Upload an image and explore a transparent food-analysis workflow.",
        ),
        (
            "Global Nutrition",
            "🌍",
            "Explore major nutrition challenges around the world.",
        ),
        (
            "Health Report",
            "📄",
            "Generate a downloadable educational screening report.",
        ),
    ]

    for row in range(0, len(tools), 3):

        cols = st.columns(3)

        for col_index in range(3):

            index = row + col_index

            if index >= len(tools):
                continue

            title, icon, description = tools[index]

            with cols[col_index]:

                st.markdown(
                    f"""
<div class="card">
    <div class="icon">{icon}</div>
    <h3>{title}</h3>
    <p>{description}</p>
</div>
""",
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Open {title}",
                    key=f"dashboard_{title}",
                    use_container_width=True,
                ):
                    go(title)

    st.markdown(
        '<div class="section-title">Nouriva at a Glance</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)

    metrics = [
        ("Core Tools", "9"),
        ("Education Areas", "10+"),
        ("SDG Connections", "5"),
        ("Status", "Working"),
    ]

    for col, (label, value) in zip(
        [m1, m2, m3, m4],
        metrics,
    ):

        with col:
            st.markdown(
                f"""
<div class="metric">
    <div class="metric-label">{label}</div>
    <div class="metric-value">{value}</div>
</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="dark-card">
    <h2>🌱 Our purpose</h2>
    <p>
        Nouriva AI demonstrates how accessible digital tools can support
        nutrition awareness, preliminary screening and nutrition education.
    </p>
    <p>
        It is a student-built educational prototype and is not intended
        to diagnose disease or replace professional healthcare.
    </p>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# NUTRITION SCAN
# ============================================================

elif st.session_state.page == "Nutrition Scan":

    st.markdown(
        '<div class="section-title">🔍 Nutrition Scan</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Preliminary nutrition screening and BMI assessment.</div>',
        unsafe_allow_html=True,
    )

    with st.form("nutrition_scan_form"):

        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input(
                "Age (years)",
                min_value=1,
                max_value=120,
                value=20,
            )

            sex = st.selectbox(
                "Sex",
                ["Male", "Female"],
            )

            meals = st.selectbox(
                "Typical meals per day",
                [1, 2, 3, 4, 5],
                index=2,
            )

        with c2:

            height = st.number_input(
                "Height (cm)",
                min_value=30.0,
                max_value=250.0,
                value=170.0,
                step=0.5,
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=300.0,
                value=55.0,
                step=0.5,
            )

            fruit_veg = st.selectbox(
                "Fruit & vegetable intake",
                ["Rarely", "Sometimes", "Daily"],
            )

        protein = st.multiselect(
            "Common protein sources",
            [
                "Eggs",
                "Milk / Dairy",
                "Pulses / Lentils",
                "Fish",
                "Chicken / Meat",
                "Nuts / Seeds",
            ],
        )

        access = st.selectbox(
            "Access to sufficient food",
            [
                "Usually sufficient",
                "Sometimes difficult",
                "Often difficult",
            ],
        )

        submitted = st.form_submit_button(
            "🔍 Analyze My Nutrition",
            use_container_width=True,
        )

    if submitted:

        calculated_bmi = bmi(height, weight)

        score, level, factors = calculate_risk(
            age,
            calculated_bmi,
            meals,
            protein,
            fruit_veg,
            access,
        )

        st.session_state.screening = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "bmi": calculated_bmi,
            "meals": meals,
            "protein": protein,
            "fruit_veg": fruit_veg,
            "access": access,
            "score": score,
            "level": level,
            "factors": factors,
        }

    if st.session_state.screening:

        data = st.session_state.screening

        st.markdown(
            '<div class="section-title">📊 Screening Result</div>',
            unsafe_allow_html=True,
        )

        a, b, c = st.columns(3)

        with a:
            st.markdown(
                f"""
<div class="metric">
<div class="metric-label">BMI</div>
<div class="metric-value">{data["bmi"]}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with b:
            st.markdown(
                f"""
<div class="metric">
<div class="metric-label">Risk Score</div>
<div class="metric-value">{data["score"]}</div>
</div>
""",
                unsafe_allow_html=True,
            )

        with c:
            st.markdown(
                f"""
<div class="metric">
<div class="metric-label">Screening Result</div>
<div class="metric-value" style="font-size:18px;">
{data["level"]}
</div>
</div>
""",
                unsafe_allow_html=True,
            )

        if data["age"] >= 18:

            category = bmi_category(data["bmi"])

            if data["bmi"] < 18.5:
                st.warning(f"⚠️ {category}")

            elif data["bmi"] < 25:
                st.success(f"✅ {category}")

            elif data["bmi"] < 30:
                st.info(f"ℹ️ {category}")

            else:
                st.warning(f"⚠️ {category}")

        else:

            st.info(
                "For people under 18, BMI should be interpreted using "
                "age- and sex-specific growth references rather than adult BMI categories."
            )

        st.markdown(
            '<div class="section-title">🌱 Identified Factors</div>',
            unsafe_allow_html=True,
        )

        if data["factors"]:

            for factor in data["factors"]:
                st.write("•", factor)

        else:
            st.success(
                "No basic risk indicators were identified by this prototype."
            )

        st.markdown(
            '<div class="section-title">💡 General Guidance</div>',
            unsafe_allow_html=True,
        )

        guidance = [
            "Aim for a varied and balanced eating pattern.",
            "Include appropriate protein sources regularly.",
            "Include fruits and vegetables regularly.",
            "Maintain appropriate fluid intake.",
            "Seek professional advice for persistent health or nutrition concerns.",
        ]

        for item in guidance:
            st.write("•", item)

        st.caption(
            "BMI and the prototype risk score are screening/educational tools, "
            "not diagnoses or validated clinical risk scores."
        )


# ============================================================
# DIET PLANNER
# ============================================================

elif st.session_state.page == "Diet Planner":

    st.markdown(
        '<div class="section-title">🍽️ Diet Planner</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Create an example day around a general nutrition goal.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        goal = st.selectbox(
            "General goal",
            [
                "Balanced nutrition",
                "Healthy weight gain",
                "Healthy weight management",
                "Athletic nutrition",
            ],
        )

        food_style = st.selectbox(
            "Food style",
            [
                "Simple foods",
                "Budget-friendly",
            ],
        )

    with c2:

        vegetarian = st.checkbox(
            "Vegetarian pattern",
        )

        allergies = st.multiselect(
            "Foods to flag for review",
            [
                "Milk",
                "Eggs",
                "Nuts",
                "Fish",
                "Chicken",
            ],
        )

    if st.button(
        "🍽️ Generate Meal Plan",
        use_container_width=True,
    ):

        protein = (
            "dal, beans, chickpeas, yogurt, milk, eggs"
            if vegetarian
            else "dal, eggs, chicken, fish, yogurt"
        )

        if goal == "Healthy weight gain":

            plan = [
                ("Breakfast", "Eggs + roti/paratha + milk + banana"),
                ("Morning Snack", "Yogurt + nuts/seeds or roasted chickpeas"),
                (
                    "Lunch",
                    f"Rice/roti + dal + "
                    f"{'beans/chickpeas' if vegetarian else 'chicken'} "
                    "+ vegetables",
                ),
                ("Evening Snack", "Milk + banana or seasonal fruit"),
                (
                    "Dinner",
                    f"Roti + "
                    f"{'dal/beans' if vegetarian else 'meat/fish'} "
                    "+ vegetables + yogurt",
                ),
            ]

        elif goal == "Healthy weight management":

            plan = [
                ("Breakfast", "Eggs or yogurt + whole-grain roti + fruit"),
                ("Morning Snack", "Fruit + unsweetened yogurt"),
                (
                    "Lunch",
                    f"Roti/rice + "
                    f"{'dal/beans' if vegetarian else 'chicken/fish'} "
                    "+ vegetables",
                ),
                ("Evening Snack", "Fruit + water or milk"),
                (
                    "Dinner",
                    f"Roti + "
                    f"{'dal/beans' if vegetarian else 'fish/chicken'} "
                    "+ vegetables",
                ),
            ]

        elif goal == "Athletic nutrition":

            plan = [
                ("Breakfast", "Eggs + oats/roti + milk + fruit"),
                ("Activity Snack", "Banana + yogurt or milk"),
                (
                    "Lunch",
                    f"Rice/roti + "
                    f"{'dal/beans' if vegetarian else 'chicken/fish'} "
                    "+ vegetables",
                ),
                ("Snack", "Fruit + yogurt + nuts/seeds"),
                (
                    "Dinner",
                    f"Roti/rice + "
                    f"{'beans/dal' if vegetarian else 'chicken/fish'} "
                    "+ vegetables",
                ),
            ]

        else:

            plan = [
                ("Breakfast", "Eggs/yogurt + roti + fruit"),
                ("Morning Snack", "Fruit + yogurt"),
                (
                    "Lunch",
                    f"Rice/roti + "
                    f"{'dal/beans' if vegetarian else 'chicken/fish'} "
                    "+ vegetables",
                ),
                ("Evening Snack", "Milk + fruit"),
                (
                    "Dinner",
                    f"Roti + "
                    f"{'dal/beans' if vegetarian else 'protein source'} "
                    "+ vegetables",
                ),
            ]

        warnings = []

        for allergy in allergies:

            for meal_name, meal_text in plan:

                if allergy.lower() in meal_text.lower():

                    warnings.append(
                        f"{meal_name}: review this suggestion because "
                        f"it may contain {allergy}."
                    )

        st.session_state.diet_plan = {
            "goal": goal,
            "style": food_style,
            "plan": plan,
            "warnings": warnings,
        }

    if st.session_state.diet_plan:

        plan_data = st.session_state.diet_plan

        st.success(
            f"Plan generated • {plan_data['goal']} • {plan_data['style']}"
        )

        for meal, food in plan_data["plan"]:

            st.markdown(
                f"""
<div class="card">
<h3>{meal}</h3>
<p>{food}</p>
</div>
""",
                unsafe_allow_html=True,
            )

        if plan_data["warnings"]:

            for warning in plan_data["warnings"]:
                st.warning(warning)

        st.info(
            "These are general educational meal ideas, not individualized medical diets."
        )


# ============================================================
# NUTRITION COACH
# ============================================================

elif st.session_state.page == "Nutrition Coach":

    st.markdown(
        '<div class="section-title">🤖 Nutrition Coach</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Ask Nouriva a general nutrition education question.</div>',
        unsafe_allow_html=True,
    )

    knowledge = {
        "protein": (
            "Protein supports tissue maintenance and repair and many body functions. "
            "Common sources include eggs, dairy, pulses, fish, meat, nuts and seeds."
        ),
        "hydration": (
            "Water is essential for normal body functions. Fluid requirements vary "
            "with age, activity, climate and health status."
        ),
        "iron": (
            "Iron is important for hemoglobin formation and oxygen transport. "
            "Sources include meat, pulses, leafy vegetables and fortified foods."
        ),
        "calcium": (
            "Calcium supports bones and teeth and also contributes to muscle and "
            "nerve function. Dairy and fortified foods are common sources."
        ),
        "fiber": (
            "Dietary fiber supports digestive health. Fruits, vegetables, pulses "
            "and whole grains are common sources."
        ),
        "vitamin": (
            "Vitamins are micronutrients needed for many biological processes. "
            "Different vitamins have different roles and food sources."
        ),
        "bmi": (
            "BMI is calculated from weight and height. In adults it can be used "
            "as a screening measure, but it does not diagnose health status."
        ),
        "food safety": (
            "Food safety includes hand hygiene, separating raw and cooked foods, "
            "adequate cooking and safe storage."
        ),
        "balanced diet": (
            "A balanced eating pattern includes a variety of foods that provide "
            "energy, protein, vitamins, minerals and other nutrients."
        ),
        "malnutrition": (
            "Malnutrition is a broad term covering several forms of nutrition "
            "imbalance. Proper assessment depends on age, context and health status."
        ),
    }

    question = st.text_input(
        "Ask your question",
        placeholder="Example: Why is protein important?",
    )

    if st.button(
        "🤖 Ask Nouriva",
        use_container_width=True,
    ):

        if question.strip():

            q = question.lower()

            answer = None

            for keyword, response in knowledge.items():

                if keyword in q:
                    answer = response
                    break

            if answer is None:

                answer = (
                    "I can provide general nutrition education about protein, "
                    "hydration, iron, calcium, fiber, vitamins, BMI, balanced diets, "
                    "food safety and malnutrition. For personal medical concerns, "
                    "please consult a qualified professional."
                )

            st.session_state.coach_history.append(
                {
                    "question": question,
                    "answer": answer,
                }
            )

    if st.session_state.coach_history:

        for item in reversed(
            st.session_state.coach_history[-8:]
        ):

            st.markdown(
                f"""
<div class="result">
<strong>You</strong><br>
{item["question"]}
<br><br>
<strong>🌿 Nouriva Coach</strong><br>
{item["answer"]}
</div>
""",
                unsafe_allow_html=True,
            )

    st.caption(
        "Educational prototype. The Coach does not diagnose or prescribe treatment."
    )


# ============================================================
# EDUCATION
# ============================================================

elif st.session_state.page == "Education":

    st.markdown(
        '<div class="section-title">📚 Nutrition Education</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Structured nutrition learning — not just MCQs.</div>',
        unsafe_allow_html=True,
    )

    lessons = {

        "Balanced Diet": {
            "overview": "A balanced eating pattern includes a variety of foods that provide energy, protein, vitamins, minerals and other nutrients.",
            "points": [
                "Include different food groups.",
                "Include appropriate protein sources.",
                "Eat fruits and vegetables regularly.",
                "Consider hydration.",
                "Limit excessive intake of highly processed foods."
            ],
            "quiz": (
                "Which best describes a balanced diet?",
                [
                    "Only one food group",
                    "A variety of foods providing different nutrients",
                    "Only protein",
                    "Only fruit"
                ],
                1,
            ),
        },

        "Protein": {
            "overview": "Protein is required for tissue maintenance, repair, growth and many physiological functions.",
            "points": [
                "Proteins are made from amino acids.",
                "Sources include pulses, eggs, dairy, fish and meat.",
                "Protein needs vary between individuals.",
                "Plant-based foods can contribute significant protein."
            ],
            "quiz": (
                "Which nutrient is especially important for tissue growth and repair?",
                [
                    "Protein",
                    "Water only",
                    "Salt only",
                    "None"
                ],
                0,
            ),
        },

        "Carbohydrates": {
            "overview": "Carbohydrates are an important source of energy and occur in foods such as grains, fruits, vegetables and pulses.",
            "points": [
                "Carbohydrates can provide energy.",
                "Whole grains can provide fiber.",
                "Fruits and vegetables contain carbohydrate.",
                "Food quality matters, not just the nutrient name."
            ],
            "quiz": (
                "Which food commonly provides carbohydrate?",
                [
                    "Rice",
                    "Only water",
                    "Salt",
                    "None"
                ],
                0,
            ),
        },

        "Fats": {
            "overview": "Dietary fats provide energy and support cell structures and absorption of fat-soluble vitamins.",
            "points": [
                "Fats are energy-dense.",
                "Different fats have different characteristics.",
                "Nuts and seeds provide dietary fats.",
                "Portion and overall dietary pattern matter."
            ],
            "quiz": (
                "Which food can provide dietary fat?",
                [
                    "Nuts",
                    "Water",
                    "Salt",
                    "None"
                ],
                0,
            ),
        },

        "Micronutrients": {
            "overview": "Micronutrients include vitamins and minerals required in smaller amounts.",
            "points": [
                "Iron supports hemoglobin formation.",
                "Calcium supports bones and teeth.",
                "Different vitamins have different functions.",
                "A varied diet can improve micronutrient diversity."
            ],
            "quiz": (
                "Iron is particularly important for:",
                [
                    "Hemoglobin formation",
                    "Making water",
                    "Replacing all protein",
                    "None"
                ],
                0,
            ),
        },

        "Hydration": {
            "overview": "Adequate fluid intake supports normal physiological functions.",
            "points": [
                "Water is essential for life.",
                "Fluid needs vary.",
                "Activity and heat can increase fluid losses.",
                "Foods can also contribute to fluid intake."
            ],
            "quiz": (
                "Which substance is essential for hydration?",
                [
                    "Water",
                    "Salt only",
                    "Protein only",
                    "None"
                ],
                0,
            ),
        },

        "Fiber": {
            "overview": "Dietary fiber occurs mainly in plant foods and supports digestive health.",
            "points": [
                "Pulses are useful sources.",
                "Whole grains can provide fiber.",
                "Fruits and vegetables contain fiber.",
                "Adequate fluids support normal bowel function."
            ],
            "quiz": (
                "Which is a common source of dietary fiber?",
                [
                    "Pulses",
                    "Table salt",
                    "Water",
                    "None"
                ],
                0,
            ),
        },

        "Food Safety": {
            "overview": "Food safety practices help reduce foodborne illness.",
            "points": [
                "Wash hands and surfaces.",
                "Separate raw and cooked foods.",
                "Cook foods appropriately.",
                "Store foods safely."
            ],
            "quiz": (
                "Which practice helps reduce contamination?",
                [
                    "Separating raw and cooked foods",
                    "Leaving food uncovered for days",
                    "Using dirty utensils",
                    "None"
                ],
                0,
            ),
        },

        "Food Security": {
            "overview": "Food security involves reliable access to sufficient, safe and nutritious food.",
            "points": [
                "Availability matters.",
                "Access and affordability matter.",
                "Food utilization and safety matter.",
                "Stability over time matters."
            ],
            "quiz": (
                "Food security mainly concerns:",
                [
                    "Reliable access to sufficient safe and nutritious food",
                    "Only restaurant availability",
                    "Only calorie counting",
                    "None"
                ],
                0,
            ),
        },

        "Undernutrition": {
            "overview": "Undernutrition can occur when energy or nutrient intake is inadequate or needs are not met.",
            "points": [
                "It can affect growth and health.",
                "Children require age-specific assessment.",
                "Causes can include illness and inadequate intake.",
                "Food insecurity can contribute."
            ],
            "quiz": (
                "Child growth assessment should consider:",
                [
                    "Age- and sex-specific references",
                    "Adult BMI categories only",
                    "Height alone",
                    "None"
                ],
                0,
            ),
        },

        "Nutrition Across Life": {
            "overview": "Nutrition needs and assessment approaches change across stages of life.",
            "points": [
                "Children require growth-focused assessment.",
                "Adults have different screening considerations.",
                "Older adults may have changing needs.",
                "Pregnancy and other stages require specialized guidance."
            ],
            "quiz": (
                "Do nutritional needs remain exactly the same throughout life?",
                [
                    "No",
                    "Yes",
                    "Only for children",
                    "Only for athletes"
                ],
                0,
            ),
        },
    }

    topic = st.selectbox(
        "Choose a learning topic",
        list(lessons.keys()),
    )

    lesson = lessons[topic]

    st.markdown(
        f"""
<div class="lesson">
<div class="lesson-tag">Nutrition lesson</div>
<h2>{topic}</h2>
<p>{lesson["overview"]}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">📌 Key Learning Points</div>',
        unsafe_allow_html=True,
    )

    for point in lesson["points"]:
        st.write("•", point)

    with st.expander("🔎 Learn More"):

        st.write(
            f"""
This lesson is designed as introductory nutrition education.
For real clinical decision-making, assessment should consider
the person's age, health status, dietary pattern and professional
nutrition/medical guidance.
"""
        )

    st.markdown(
        '<div class="section-title">🧠 Knowledge Check</div>',
        unsafe_allow_html=True,
    )

    question, options, correct = lesson["quiz"]

    selected = st.radio(
        question,
        options,
        key=f"education_{topic}",
    )

    if st.button(
        "Check Answer",
        use_container_width=True,
    ):

        selected_index = options.index(selected)

        st.session_state.quiz_total += 1

        if selected_index == correct:

            st.session_state.quiz_score += 1

            st.success("✅ Correct!")

        else:

            st.error(
                f"❌ Not quite. Correct answer: {options[correct]}"
            )

    if st.session_state.quiz_total > 0:

        st.metric(
            "Learning Progress",
            f"{st.session_state.quiz_score} / {st.session_state.quiz_total}",
        )


# ============================================================
# NUTRITION INSIGHTS
# ============================================================

elif st.session_state.page == "Nutrition Insights":

    st.markdown(
        '<div class="section-title">📊 Nutrition Insights</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Explore screening concepts, nutrition factors and global connections.</div>',
        unsafe_allow_html=True,
    )

    insight = st.selectbox(
        "Choose an insight",
        [
            "Adult BMI Screening",
            "Prototype Risk Factors",
            "SDG Connections",
        ],
    )

    if insight == "Adult BMI Screening":

        df = pd.DataFrame(
            {
                "Category": [
                    "Below 18.5",
                    "18.5–24.9",
                    "25–29.9",
                    "30+",
                ],
                "Threshold": [
                    18.5,
                    24.9,
                    29.9,
                    30,
                ],
            }
        )

        st.bar_chart(
            df.set_index("Category")
        )

        st.info(
            "These are adult BMI screening categories. BMI is not a complete measure of health."
        )

    elif insight == "Prototype Risk Factors":

        df = pd.DataFrame(
            {
                "Factor": [
                    "Low meals",
                    "No protein",
                    "Low fruit/veg",
                    "Food access",
                ],
                "Prototype Weight": [
                    1,
                    1,
                    1,
                    2,
                ],
            }
        )

        st.bar_chart(
            df.set_index("Factor")
        )

        st.info(
            "These are demonstration weights created for this student prototype. "
            "They are not validated clinical risk scores."
        )

    else:

        df = pd.DataFrame(
            {
                "SDG": [
                    "SDG 1",
                    "SDG 2",
                    "SDG 3",
                    "SDG 4",
                    "SDG 12",
                ],
                "Relevance": [
                    2,
                    5,
                    5,
                    4,
                    3,
                ],
            }
        )

        st.bar_chart(
            df.set_index("SDG")
        )

        st.success(
            "Nouriva connects most directly with SDG 2, SDG 3 and SDG 4."
        )


# ============================================================
# GROWTH MONITOR
# ============================================================

elif st.session_state.page == "Growth Monitor":

    st.markdown(
        '<div class="section-title">🧒 Growth Monitor</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Educational demonstration of growth assessment.</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        child_age = st.number_input(
            "Age (years)",
            min_value=0.1,
            max_value=19.0,
            value=10.0,
            step=0.1,
        )

        child_sex = st.selectbox(
            "Sex",
            ["Male", "Female"],
            key="growth_gender",
        )

    with c2:

        child_height = st.number_input(
            "Height (cm)",
            min_value=30.0,
            max_value=220.0,
            value=140.0,
        )

        child_weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=150.0,
            value=35.0,
        )

    if st.button(
        "🧒 Analyze Growth Information",
        use_container_width=True,
    ):

        child_bmi = bmi(
            child_height,
            child_weight,
        )

        st.session_state.growth_result = {
            "age": child_age,
            "sex": child_sex,
            "height": child_height,
            "weight": child_weight,
            "bmi": child_bmi,
        }

    if st.session_state.growth_result:

        result = st.session_state.growth_result

        a, b, c = st.columns(3)

        with a:
            st.metric(
                "BMI",
                result["bmi"],
            )

        with b:
            st.metric(
                "Age",
                f'{result["age"]:.1f} years',
            )

        with c:
            st.metric(
                "Height",
                f'{result["height"]:.1f} cm',
            )

        st.warning(
            "BMI alone cannot determine whether a child is growing normally. "
            "Child growth assessment requires validated age- and sex-specific "
            "growth references and professional interpretation."
        )

        if result["age"] < 5:

            st.info(
                "Young-child growth assessment requires specialized growth standards."
            )

        else:

            st.success(
                "The prototype has captured the basic measurements needed "
                "for a future validated growth-reference workflow."
            )


# ============================================================
# FOOD SCANNER
# ============================================================

elif st.session_state.page == "Food Scanner":

    st.markdown(
        '<div class="section-title">📷 Food Scanner</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Transparent image-analysis prototype — no fake AI claims.</div>',
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "Upload a food image",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
        ],
    )

    if uploaded:

        image_bytes = uploaded.getvalue()

        try:

            image = Image.open(
                io.BytesIO(image_bytes)
            )

            st.image(
                image,
                caption="Uploaded food image",
                use_container_width=True,
            )

            width, height = image.size

            st.markdown(
                '<div class="section-title">🔬 Image Analysis</div>',
                unsafe_allow_html=True,
            )

            a, b, c = st.columns(3)

            with a:
                st.metric(
                    "Width",
                    f"{width}px",
                )

            with b:
                st.metric(
                    "Height",
                    f"{height}px",
                )

            with c:
                st.metric(
                    "File Size",
                    f"{len(image_bytes)/1024:.1f} KB",
                )

            st.success(
                "Image successfully received and processed."
            )

            st.info(
                "This prototype does not claim to identify foods or calories "
                "without a trained computer-vision model. A future production "
                "version could connect image recognition to a validated nutrition database."
            )

            if st.button(
                "📊 Save Image Analysis",
                use_container_width=True,
            ):

                st.session_state.food_result = {
                    "filename": uploaded.name,
                    "width": width,
                    "height": height,
                    "size": len(image_bytes),
                }

                st.success(
                    "Image analysis summary saved for this session."
                )

        except Exception as error:

            st.error(
                f"Could not process this image: {error}"
            )


# ============================================================
# GLOBAL NUTRITION
# ============================================================

elif st.session_state.page == "Global Nutrition":

    st.markdown(
        '<div class="section-title">🌍 Global Nutrition</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Explore major nutrition challenges and global development.</div>',
        unsafe_allow_html=True,
    )

    topics = {

        "Undernutrition": (
            "Undernutrition refers to conditions associated with inadequate energy "
            "or nutrient intake and can affect growth, development and health.",
            "SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being",
        ),

        "Food Security": (
            "Food security involves reliable access to sufficient, safe and nutritious food.",
            "SDG 2 • Zero Hunger | SDG 1 • No Poverty",
        ),

        "Micronutrient Deficiencies": (
            "Micronutrient deficiencies occur when the body does not receive or absorb enough essential vitamins or minerals.",
            "SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being",
        ),

        "Child Malnutrition": (
            "Child nutrition assessment requires appropriate measures of growth, development and nutritional status.",
            "SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being",
        ),

        "Sustainable Nutrition": (
            "Sustainable nutrition considers health, food systems, resources and environmental impacts.",
            "SDG 2 • Zero Hunger | SDG 12 • Responsible Consumption and Production",
        ),

        "Nutrition Education": (
            "Nutrition education can help people understand food choices, dietary patterns and basic nutrition concepts.",
            "SDG 3 • Good Health and Well-Being | SDG 4 • Quality Education",
        ),
    }

    topic = st.selectbox(
        "Choose a global nutrition topic",
        list(topics.keys()),
    )

    description, sdgs = topics[topic]

    st.markdown(
        f"""
<div class="dark-card">
<h2>🌎 {topic}</h2>
<p>{description}</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">🎯 SDG Connection</div>',
        unsafe_allow_html=True,
    )

    st.success(sdgs)

    st.markdown(
        '<div class="section-title">Why it matters</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Nutrition challenges are influenced by health, food availability, "
        "economic conditions, education, environment and access to services. "
        "They therefore require broader solutions rather than a single intervention."
    )


# ============================================================
# HEALTH REPORT
# ============================================================

elif st.session_state.page == "Health Report":

    st.markdown(
        '<div class="section-title">📄 Health Report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-sub">Generate a downloadable educational screening summary.</div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.screening:

        st.warning(
            "Complete Nutrition Scan first."
        )

        if st.button(
            "Go to Nutrition Scan",
            use_container_width=True,
        ):
            go("Nutrition Scan")

    else:

        data = st.session_state.screening

        report = f"""
NOURIVA AI
Nutrition Screening & Education Report
========================================

Generated:
{data["date"]}

PERSON INFORMATION
------------------
Age: {data["age"]}
Sex: {data["sex"]}
Height: {data["height"]} cm
Weight: {data["weight"]} kg

SCREENING
---------
BMI: {data["bmi"]}

BMI category:
{
    bmi_category(data["bmi"])
    if data["age"] >= 18
    else "Age-specific interpretation required"
}

Reported meals per day: {data["meals"]}

Protein sources:
{
    ", ".join(data["protein"])
    if data["protein"]
    else "None selected"
}

Fruit & vegetable intake:
{data["fruit_veg"]}

Food access:
{data["access"]}

PROTOTYPE RISK SCREEN
---------------------
Score: {data["score"]}
Result: {data["level"]}

Factors:
{
    chr(10).join("- " + x for x in data["factors"])
    if data["factors"]
    else "- No basic risk indicators identified"
}

GENERAL EDUCATIONAL GUIDANCE
----------------------------
- Aim for a varied and balanced eating pattern.
- Include appropriate protein sources.
- Include fruits and vegetables regularly.
- Maintain appropriate fluid intake.
- Seek professional advice for persistent concerns.

IMPORTANT
---------
This report was generated by a student-built educational prototype.

It is NOT a medical diagnosis.
It does NOT replace assessment by a qualified healthcare or nutrition professional.

Nouriva AI • Nutrition • Education • Awareness
Student Health-Technology Prototype • 2026
"""

        st.text_area(
            "Report Preview",
            report,
            height=480,
        )

        st.download_button(
            "⬇️ Download Nouriva Report",
            data=report,
            file_name="Nouriva_AI_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About":

    st.markdown(
        '<div class="section-title">ℹ️ About Nouriva AI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="dark-card">

<h2>🌿 Nouriva AI</h2>

<p>
Nouriva AI is a student-built health-technology prototype focused on
nutrition awareness, preliminary screening and accessible digital education.
</p>

<h3>🎯 Focus</h3>

<p>
Nutrition screening • Education • Meal planning • Growth awareness •
Global nutrition learning
</p>

<h3>🌍 Global Perspective</h3>

<p>
The platform connects nutrition awareness with broader issues including
food security, undernutrition, micronutrient deficiencies and sustainable
development.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">👨‍💻 Creator</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "**Muhammad Ahsan Shahzad**"
    )

    st.write(
        "BS Human Nutrition & Dietetics Student • Pakistan"
    )

    st.markdown(
        '<div class="section-title">⚠️ Important</div>',
        unsafe_allow_html=True,
    )

    st.warning(
        "Nouriva AI is an educational prototype. "
        "It does not diagnose disease, prescribe treatment or replace qualified healthcare professionals."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    🌿 <b>Nouriva AI</b> • Nutrition • Education • Awareness<br>
    Student Health-Technology Prototype • 2026<br><br>
    Educational prototype — not a diagnostic medical system.
</div>
""",
    unsafe_allow_html=True,
)
