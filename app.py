import io
from datetime import datetime

import streamlit as st

# ============================================================
# 🌿 NOURIVA AI — FINAL HACKATHON PROTOTYPE
# Nutrition • Education • Awareness
# ============================================================

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 🎨 DESIGN
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(46, 204, 113, .12), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(52, 152, 219, .10), transparent 25%),
            #f7faf8;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #073b2a 0%, #0b5d42 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 2.2rem;
        border-radius: 28px;
        background: linear-gradient(135deg, #073b2a, #0b7653);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 40px rgba(7,59,42,.16);
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: .3rem;
    }

    .hero p {
        font-size: 1.08rem;
        opacity: .92;
    }

    .card {
        padding: 1.25rem;
        border-radius: 20px;
        background: rgba(255,255,255,.94);
        border: 1px solid rgba(7,59,42,.08);
        box-shadow: 0 8px 24px rgba(0,0,0,.055);
        min-height: 175px;
        margin-bottom: 1rem;
    }

    .card h3 {
        margin-top: 0;
        color: #073b2a;
    }

    .metric {
        padding: 1rem;
        border-radius: 18px;
        background: white;
        text-align: center;
        border: 1px solid rgba(7,59,42,.08);
        box-shadow: 0 6px 18px rgba(0,0,0,.045);
    }

    .metric-number {
        font-size: 2rem;
        font-weight: 800;
        color: #087f5b;
    }

    .metric-label {
        color: #64748b;
        font-size: .9rem;
    }

    .section-title {
        color: #073b2a;
        font-weight: 800;
        margin-top: 1rem;
    }

    .tag {
        display: inline-block;
        padding: .35rem .7rem;
        border-radius: 999px;
        background: #dff7ec;
        color: #075c41;
        margin: .2rem;
        font-size: .82rem;
        font-weight: 600;
    }

    .result-box {
        padding: 1.4rem;
        border-radius: 20px;
        background: white;
        border-left: 6px solid #087f5b;
        box-shadow: 0 8px 22px rgba(0,0,0,.06);
        margin: 1rem 0;
    }

    .footer {
        text-align: center;
        padding: 2rem 0 1rem;
        color: #64748b;
        font-size: .85rem;
    }

    div.stButton > button {
        border-radius: 12px;
        font-weight: 700;
        min-height: 2.7rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DATA
# ============================================================

EDUCATION = {
    "🥗 Balanced Diet": {
        "summary": "A balanced diet combines a variety of foods to provide energy, protein, vitamins, minerals and other nutrients.",
        "key": [
            "Include foods from several food groups.",
            "Choose a variety of fruits and vegetables.",
            "Include appropriate protein sources.",
            "Prefer minimally processed foods when practical.",
            "Balance food choices with individual needs and circumstances.",
        ],
        "tip": "Think variety rather than relying on one food as the solution to nutrition.",
        "quiz": "Which statement best describes a balanced diet?",
        "options": [
            "Eating only one food group",
            "Eating a variety of foods that provide different nutrients",
            "Avoiding all carbohydrates",
            "Drinking water instead of eating",
        ],
        "answer": "Eating a variety of foods that provide different nutrients",
    },
    "💪 Protein": {
        "summary": "Protein contributes to growth, tissue maintenance and repair and many other body functions.",
        "key": [
            "Protein is made from amino acids.",
            "Common sources include eggs, dairy, pulses, fish, meat, nuts and seeds.",
            "Protein needs vary with age, body size, activity and health.",
            "Plant and animal foods can both contribute protein.",
        ],
        "tip": "Affordable options such as lentils, beans, eggs and dairy can be useful protein sources.",
        "quiz": "Which nutrient is especially important for tissue growth and repair?",
        "options": ["Protein", "Water only", "Salt only", "None of these"],
        "answer": "Protein",
    },
    "⚡ Carbohydrates": {
        "summary": "Carbohydrates are an important source of energy and are found in foods such as grains, fruits, vegetables and pulses.",
        "key": [
            "Carbohydrates provide energy.",
            "Whole grains can provide fiber and other nutrients.",
            "Fruits and vegetables also contain carbohydrates.",
            "Food quality and overall dietary pattern matter.",
        ],
        "tip": "Carbohydrates are not automatically unhealthy; the food source and overall dietary pattern matter.",
        "quiz": "What is a major role of carbohydrates?",
        "options": [
            "Providing energy",
            "Replacing all vitamins",
            "Making water unnecessary",
            "Preventing every disease",
        ],
        "answer": "Providing energy",
    },
    "🥑 Fats": {
        "summary": "Dietary fats provide energy and help the body absorb certain fat-soluble vitamins.",
        "key": [
            "Fats are energy-dense.",
            "Unsaturated fats are commonly found in nuts, seeds, fish and some plant oils.",
            "The type and amount of fat matter.",
            "A varied diet can provide different fatty acids.",
        ],
        "tip": "Focus on overall dietary quality rather than eliminating dietary fat completely.",
        "quiz": "Which is a function of dietary fat?",
        "options": [
            "Helping absorb certain vitamins",
            "Making the body independent of water",
            "Replacing protein completely",
            "Eliminating the need for minerals",
        ],
        "answer": "Helping absorb certain vitamins",
    },
    "🧬 Micronutrients": {
        "summary": "Vitamins and minerals are needed in relatively small amounts but are essential for normal body functions.",
        "key": [
            "Examples include iron, calcium, iodine, zinc and vitamin A.",
            "Requirements differ across life stages.",
            "A varied diet can help provide many micronutrients.",
            "Deficiencies can affect health and development.",
        ],
        "tip": "Micronutrients are small in quantity but important in function.",
        "quiz": "Which is a micronutrient?",
        "options": ["Iron", "Protein", "Water", "Starch"],
        "answer": "Iron",
    },
    "🩸 Iron": {
        "summary": "Iron is an essential mineral involved in important processes including oxygen transport.",
        "key": [
            "Iron is present in foods such as meat, pulses and some fortified foods.",
            "Vitamin C can improve absorption of non-heme iron from plant foods.",
            "Iron needs vary by age and physiological circumstances.",
            "Persistent symptoms or suspected deficiency require professional assessment.",
        ],
        "tip": "Nutrition education should not replace laboratory assessment when deficiency is suspected.",
        "quiz": "Which vitamin can improve absorption of non-heme iron?",
        "options": ["Vitamin C", "Vitamin K only", "Vitamin D only", "No vitamin"],
        "answer": "Vitamin C",
    },
    "💧 Hydration": {
        "summary": "Water is essential for many normal physiological processes.",
        "key": [
            "Fluid needs vary with climate, activity and individual circumstances.",
            "Water is an important source of hydration.",
            "Sweating can increase fluid requirements.",
            "Severe dehydration can be dangerous.",
        ],
        "tip": "Thirst, urine color and environmental conditions can provide useful everyday cues, but medical situations require professional advice.",
        "quiz": "Why is adequate fluid intake important?",
        "options": [
            "Water supports many normal body functions",
            "It replaces every nutrient",
            "It removes the need for food",
            "It guarantees disease prevention",
        ],
        "answer": "Water supports many normal body functions",
    },
    "🛡️ Food Safety": {
        "summary": "Food safety practices help reduce the risk of foodborne illness.",
        "key": [
            "Keep hands and surfaces clean.",
            "Separate raw and ready-to-eat foods.",
            "Cook foods appropriately.",
            "Store food safely.",
            "Use safe water and ingredients.",
        ],
        "tip": "Clean, separate, cook and chill are useful principles for everyday food safety.",
        "quiz": "Which practice helps reduce cross-contamination?",
        "options": [
            "Separating raw and ready-to-eat foods",
            "Using the same dirty knife",
            "Leaving food uncovered",
            "Ignoring storage conditions",
        ],
        "answer": "Separating raw and ready-to-eat foods",
    },
    "🌾 Food Security": {
        "summary": "Food security concerns reliable access to sufficient, safe and nutritious food.",
        "key": [
            "Availability is one component of food security.",
            "Access and affordability also matter.",
            "Food utilization and nutritional quality matter.",
            "Stability over time is important.",
        ],
        "tip": "Nutrition is influenced not only by personal choices but also by social and economic conditions.",
        "quiz": "Which factor can affect food security?",
        "options": [
            "Food affordability",
            "Only food color",
            "Only meal timing",
            "None",
        ],
        "answer": "Food affordability",
    },
    "🌱 Undernutrition": {
        "summary": "Undernutrition can involve inadequate energy or nutrient intake and may include wasting, stunting and deficiencies.",
        "key": [
            "Undernutrition has multiple causes.",
            "Food access, illness and social conditions can contribute.",
            "Children require age-appropriate assessment.",
            "Screening tools identify potential concerns rather than diagnosing disease.",
        ],
        "tip": "A screening result should be interpreted in context and followed by professional assessment when appropriate.",
        "quiz": "What is an important limitation of a basic BMI screen?",
        "options": [
            "It cannot diagnose all forms of malnutrition",
            "It measures every nutrient",
            "It replaces clinical assessment",
            "It diagnoses disease automatically",
        ],
        "answer": "It cannot diagnose all forms of malnutrition",
    },
    "👶 Child Nutrition": {
        "summary": "Children have changing nutritional needs during growth and development.",
        "key": [
            "Growth should be interpreted using age- and sex-specific references.",
            "BMI categories for children differ from adult categories.",
            "Growth patterns over time can be more informative than one measurement.",
            "Professional assessment is important when growth concerns exist.",
        ],
        "tip": "Never apply adult BMI cutoffs to children as if they were adults.",
        "quiz": "How should child BMI generally be interpreted?",
        "options": [
            "Using age- and sex-specific references",
            "Using adult cutoffs only",
            "Ignoring age",
            "Using weight alone",
        ],
        "answer": "Using age- and sex-specific references",
    },
}

MEALS = {
    "Balanced nutrition": [
        ("Breakfast", "Eggs + roti + fruit + milk"),
        ("Snack", "Seasonal fruit + yogurt"),
        ("Lunch", "Daal + rice/roti + vegetables + salad"),
        ("Snack", "Roasted chickpeas or nuts + water"),
        ("Dinner", "Chicken/fish/beans + roti + vegetables"),
    ],
    "Healthy weight gain": [
        ("Breakfast", "Eggs + roti/paratha + milk + banana"),
        ("Snack", "Yogurt + nuts/seeds"),
        ("Lunch", "Rice/roti + daal + chicken + vegetables"),
        ("Snack", "Milk + banana or fruit"),
        ("Dinner", "Roti + beans/meat + vegetables + yogurt"),
    ],
    "Athletic nutrition": [
        ("Breakfast", "Eggs + oats/roti + milk + fruit"),
        ("Snack", "Yogurt + banana"),
        ("Lunch", "Rice + chicken/fish + vegetables"),
        ("Pre/post activity", "Fruit + milk/yogurt"),
        ("Dinner", "Roti + lentils/meat + vegetables"),
    ],
    "Budget-friendly": [
        ("Breakfast", "Eggs + roti + seasonal fruit"),
        ("Snack", "Roasted chickpeas"),
        ("Lunch", "Daal + rice + seasonal vegetables"),
        ("Snack", "Milk or yogurt"),
        ("Dinner", "Beans/chickpeas + roti + vegetables"),
    ],
}

GLOBAL_TOPICS = {
    "Undernutrition": "Undernutrition includes conditions associated with inadequate energy or nutrient intake and can affect growth, development and health.",
    "Food insecurity": "Food insecurity involves uncertain or limited access to enough safe and nutritious food.",
    "Micronutrient deficiencies": "Deficiencies of vitamins and minerals can occur for many reasons, including limited dietary variety and increased needs.",
    "Child growth": "Growth monitoring requires age- and sex-specific references and interpretation of measurements over time.",
    "Healthy diets": "Healthy dietary patterns emphasize variety, appropriate energy intake and adequate nutrients while considering local food availability.",
}

COACH_RESPONSES = {
    "protein": "Protein supports growth, tissue maintenance and repair. Examples include eggs, dairy, pulses, fish, meat, nuts and seeds.",
    "iron": "Iron is important for oxygen-related functions. Sources include meat, pulses and fortified foods. Vitamin C can improve absorption of non-heme iron.",
    "water": "Water supports many normal body functions. Fluid needs vary with activity, climate and individual circumstances.",
    "bmi": "BMI is calculated from weight and height. It is a screening indicator, not a diagnosis, and adult and child interpretation are different.",
    "diet": "A balanced dietary pattern generally includes a variety of foods, including vegetables, fruits, grains or other carbohydrate sources, protein foods and appropriate fats.",
    "weight": "Weight concerns should be considered alongside age, growth pattern, diet, health status and other factors. A professional can provide individualized assessment.",
}

# ============================================================
# HELPERS
# ============================================================

def bmi_value(weight, height):
    if height <= 0:
        return None
    return round(weight / ((height / 100) ** 2), 1)


def bmi_category(age, bmi):
    if age < 18:
        return (
            "Child/adolescent BMI requires age- and sex-specific growth references."
        )
    if bmi < 18.5:
        return "Below the standard adult BMI range."
    if bmi < 25:
        return "Within the standard adult BMI range."
    if bmi < 30:
        return "Above the standard adult BMI range."
    return "High adult BMI range."


def risk_assessment(age, bmi, meals, protein, fruit_veg, food_access):
    score = 0
    factors = []

    if age >= 18 and bmi < 18.5:
        score += 2
        factors.append("BMI below the standard adult range")

    if meals <= 2:
        score += 1
        factors.append("Low reported meal frequency")

    if not protein:
        score += 1
        factors.append("No protein source selected")

    if fruit_veg == "Rarely":
        score += 1
        factors.append("Rare fruit and vegetable intake")

    if food_access == "Often difficult":
        score += 2
        factors.append("Frequent difficulty accessing sufficient food")
    elif food_access == "Sometimes difficult":
        score += 1
        factors.append("Occasional difficulty accessing sufficient food")

    if score >= 4:
        level = "Higher potential risk factors"
    elif score >= 2:
        level = "Some potential risk factors"
    else:
        level = "Few factors identified in this basic screen"

    return score, level, factors


def navigate(page):
    st.session_state["page"] = page


def card_button(page, label):
    if st.button(label, use_container_width=True):
        navigate(page)
        st.rerun()


def report_text(data):
    lines = [
        "NOURIVA AI — EDUCATIONAL SCREENING REPORT",
        "=" * 48,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "IMPORTANT: This is an educational prototype report.",
        "It is not a diagnosis and does not replace professional healthcare.",
        "",
        "USER INPUT",
        f"Age: {data['age']}",
        f"Sex: {data['sex']}",
        f"Height: {data['height']} cm",
        f"Weight: {data['weight']} kg",
        "",
        "SCREENING",
        f"BMI: {data['bmi']}",
        f"Interpretation: {data['bmi_category']}",
        f"Risk assessment: {data['risk_level']}",
        "",
        "RISK FACTORS IDENTIFIED",
    ]

    if data["factors"]:
        lines.extend([f"- {x}" for x in data["factors"]])
    else:
        lines.append("- None identified by this basic prototype screen.")

    lines.extend(
        [
            "",
            "GENERAL EDUCATIONAL GUIDANCE",
            "- Aim for dietary variety.",
            "- Include appropriate protein sources.",
            "- Include fruits and vegetables regularly.",
            "- Maintain adequate hydration.",
            "- Seek qualified professional advice for health concerns.",
            "",
            "Nouriva AI — Student Health-Technology Prototype",
        ]
    )

    return "\n".join(lines)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:10px 0 20px;">
            <div style="font-size:3rem;">🌿</div>
            <h2 style="margin:0;">Nouriva AI</h2>
            <p style="opacity:.85;">Nutrition • Education • Awareness</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pages = [
        "🏠 Dashboard",
        "🔍 Nutrition Scan",
        "🍽️ Diet Planner",
        "🤖 Nutrition Coach",
        "📚 Education",
        "📊 Nutrition Insights",
        "🧒 Growth Monitor",
        "📷 Food Scanner",
        "🌍 Global Nutrition",
        "📄 Health Report",
        "ℹ️ About Nouriva",
    ]

    selected = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.page),
    )

    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

    st.markdown("---")
    st.caption("Student Health-Technology Prototype")
    st.caption("Nouriva AI • 2026")

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🌿 Nouriva AI</h1>
        <p>AI-Assisted Nutrition Screening & Education</p>
        <p>
        Nutrition awareness, preliminary screening, education,
        meal planning and global nutrition learning in one prototype.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "🏠 Dashboard":

    st.markdown(
        """
        <h2 class="section-title">Your Nutrition Hub</h2>
        <p>Choose a tool to explore Nouriva AI.</p>
        """,
        unsafe_allow_html=True,
    )

    modules = [
        (
            "🔍",
            "Nutrition Scan",
            "BMI and preliminary nutrition-risk screening.",
            "🔍 Nutrition Scan",
        ),
        (
            "🍽️",
            "Diet Planner",
            "Create example meal plans using practical food choices.",
            "🍽️ Diet Planner",
        ),
        (
            "🤖",
            "Nutrition Coach",
            "Explore general nutrition education questions.",
            "🤖 Nutrition Coach",
        ),
        (
            "📚",
            "Education",
            "Structured lessons, key points and knowledge checks.",
            "📚 Education",
        ),
        (
            "📊",
            "Nutrition Insights",
            "Explore indicators and Sustainable Development Goals.",
            "📊 Nutrition Insights",
        ),
        (
            "🧒",
            "Growth Monitor",
            "Explore age- and sex-specific growth assessment concepts.",
            "🧒 Growth Monitor",
        ),
        (
            "📷",
            "Food Scanner",
            "Upload a food image and explore the prototype workflow.",
            "📷 Food Scanner",
        ),
        (
            "🌍",
            "Global Nutrition",
            "Learn about major global nutrition challenges.",
            "🌍 Global Nutrition",
        ),
        (
            "📄",
            "Health Report",
            "Generate a downloadable educational screening report.",
            "📄 Health Report",
        ),
    ]

    for row in range(0, len(modules), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            if row + i >= len(modules):
                break

            icon, title, desc, page = modules[row + i]

            with col:
                st.markdown(
                    f"""
                    <div class="card">
                        <div style="font-size:2.1rem;">{icon}</div>
                        <h3>{title}</h3>
                        <p>{desc}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                card_button(page, f"Open {title} →")

    st.markdown("### Nouriva at a Glance")

    cols = st.columns(4)

    metrics = [
        ("9", "Core Tools"),
        ("11+", "Education Areas"),
        ("5", "SDG Connections"),
        ("MVP+", "Working Prototype"),
    ]

    for col, (number, label) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-number">{number}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 🌱 Our Purpose")

    st.info(
        "Nouriva AI demonstrates how accessible digital tools can "
        "support nutrition awareness, preliminary screening and "
        "nutrition education. It is a student-built prototype, "
        "not a diagnostic medical system."
    )

# ============================================================
# NUTRITION SCAN
# ============================================================

elif st.session_state.page == "🔍 Nutrition Scan":

    st.header("🔍 Nutrition Scan")
    st.write(
        "Enter basic information to explore a preliminary nutrition screen."
    )

    c1, c2 = st.columns(2)

    with c1:
        age = st.number_input("Age (years)", 1, 120, 20)
        sex = st.selectbox("Sex", ["Male", "Female"])

    with c2:
        height = st.number_input("Height (cm)", 30.0, 250.0, 170.0)
        weight = st.number_input("Weight (kg)", 1.0, 300.0, 55.0)

    meals = st.select_slider(
        "Typical meals per day",
        options=[1, 2, 3, 4, 5],
        value=3,
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

    fruit_veg = st.select_slider(
        "Fruit & vegetable intake",
        options=["Rarely", "Sometimes", "Daily"],
        value="Daily",
    )

    food_access = st.select_slider(
        "Access to sufficient food",
        options=[
            "Usually sufficient",
            "Sometimes difficult",
            "Often difficult",
        ],
        value="Usually sufficient",
    )

    if st.button("🔍 Analyze My Nutrition", type="primary", use_container_width=True):

        bmi = bmi_value(weight, height)
        category = bmi_category(age, bmi)

        score, level, factors = risk_assessment(
            age,
            bmi,
            meals,
            protein,
            fruit_veg,
            food_access,
        )

        st.session_state.report_data = {
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "bmi_category": category,
            "risk_level": level,
            "factors": factors,
        }

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.metric("BMI", bmi)

        with c2:
            st.metric("Screening Score", score)

        if age < 18:
            st.info(
                "For children and adolescents, BMI should be interpreted "
                "using validated age- and sex-specific growth references."
            )
        elif bmi < 18.5:
            st.warning(category)
        elif bmi < 25:
            st.success(category)
        elif bmi < 30:
            st.info(category)
        else:
            st.warning(category)

        st.markdown("### 🌱 Preliminary Nutrition Risk")
        st.info(level)

        if factors:
            st.markdown("**Factors contributing to this prototype score:**")
            for factor in factors:
                st.write(f"• {factor}")
        else:
            st.success("No risk factors were identified by this basic screen.")

        st.markdown("### 💡 Educational Guidance")

        guidance = [
            "Aim for dietary variety.",
            "Include appropriate protein sources.",
            "Include fruits and vegetables regularly.",
            "Maintain adequate fluid intake.",
            "Consider affordability and food access when planning meals.",
            "Seek qualified professional advice when you have health concerns.",
        ]

        for item in guidance:
            st.write(f"• {item}")

        st.caption(
            "This score is a prototype screening model created for education. "
            "It has not been clinically validated and cannot diagnose disease."
        )

# ============================================================
# DIET PLANNER
# ============================================================

elif st.session_state.page == "🍽️ Diet Planner":

    st.header("🍽️ Diet Planner")
    st.write(
        "Build an example day around a general nutrition goal."
    )

    goal = st.selectbox(
        "General goal",
        list(MEALS.keys()),
    )

    style = st.selectbox(
        "Food style",
        [
            "Local / practical foods",
            "Simple foods",
            "Flexible",
        ],
    )

    st.info(
        f"Selected goal: **{goal}** • Style: **{style}**"
    )

    plan = MEALS[goal]

    for meal, foods in plan:
        st.markdown(
            f"""
            <div class="card" style="min-height:0;">
                <h3>{meal}</h3>
                <p>{foods}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.warning(
        "These are example educational meal ideas, not individualized "
        "medical diets. Personal dietary needs can vary."
    )

# ============================================================
# NUTRITION COACH
# ============================================================

elif st.session_state.page == "🤖 Nutrition Coach":

    st.header("🤖 Nouriva Nutrition Coach")

    st.write(
        "Ask a general nutrition education question. "
        "The current prototype uses a curated educational knowledge base."
    )

    question = st.text_input(
        "Example: Why is protein important?"
    )

    if question:
        q = question.lower()
        answer = None

        for keyword, response in COACH_RESPONSES.items():
            if keyword in q:
                answer = response
                break

        if answer:
            st.success(answer)
        else:
            st.info(
                "Try asking about **protein, iron, water, BMI, diet, "
                "or weight**. More topics can be added to the knowledge base."
            )

    st.markdown("### Suggested Questions")

    suggestions = [
        "Why is protein important?",
        "What foods contain iron?",
        "How does BMI work?",
        "Why do we need water?",
        "What is a balanced diet?",
    ]

    for item in suggestions:
        st.write(f"• {item}")

    st.caption(
        "Educational assistant only. It does not diagnose conditions "
        "or replace a qualified nutrition or healthcare professional."
    )

# ============================================================
# EDUCATION
# ============================================================

elif st.session_state.page == "📚 Education":

    st.header("📚 Nutrition Education")

    st.write(
        "Explore structured nutrition lessons instead of relying only on quizzes."
    )

    topic = st.selectbox(
        "Choose a learning area",
        list(EDUCATION.keys()),
    )

    lesson = EDUCATION[topic]

    st.markdown(
        f"""
        <div class="card">
            <h2>{topic}</h2>
            <p>{lesson["summary"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔑 Key Learning Points")

    for point in lesson["key"]:
        st.write(f"• {point}")

    st.markdown("### 💡 Practical Takeaway")
    st.success(lesson["tip"])

    st.markdown("### 🧠 Knowledge Check")

    answer = st.radio(
        lesson["quiz"],
        lesson["options"],
        key=f"quiz_{topic}",
    )

    if st.button("Check Answer", use_container_width=True):
        if answer == lesson["answer"]:
            st.success("✅ Correct!")
        else:
            st.error(f"Not quite. The best answer is: **{lesson['answer']}**")

# ============================================================
# INSIGHTS
# ============================================================

elif st.session_state.page == "📊 Nutrition Insights":

    st.header("📊 Nutrition Insights")

    st.write(
        "A high-level educational view of nutrition indicators and SDG connections."
    )

    cols = st.columns(4)

    insight_metrics = [
        ("BMI", "Screening indicator"),
        ("Diet", "Behavioral factors"),
        ("Food access", "Social determinant"),
        ("Growth", "Development indicator"),
    ]

    for col, (number, label) in zip(cols, insight_metrics):
        with col:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-number">{number}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### 🌍 Why multiple indicators matter")

    st.write(
        "Nutrition is influenced by diet, health, growth, food access, "
        "social conditions and many other factors. A single number such "
        "as BMI cannot describe complete nutritional status."
    )

    st.markdown("### 🌎 Sustainable Development Goal Connections")

    sdgs = {
        "SDG 2 — Zero Hunger": "Food security, adequate nutrition and sustainable food systems.",
        "SDG 3 — Good Health and Well-Being": "Health awareness, prevention and healthy living.",
        "SDG 4 — Quality Education": "Accessible nutrition education and health literacy.",
        "SDG 10 — Reduced Inequalities": "Awareness of barriers to adequate nutrition.",
        "SDG 12 — Responsible Consumption": "Food choices, waste awareness and sustainable consumption.",
    }

    for title, description in sdgs.items():
        st.markdown(
            f"""
            <div class="card" style="min-height:0;">
                <h3>{title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# GROWTH MONITOR
# ============================================================

elif st.session_state.page == "🧒 Growth Monitor":

    st.header("🧒 Growth Monitor")

    st.write(
        "Educational demonstration of how growth measurements can be recorded."
    )

    age = st.number_input(
        "Child/adolescent age (years)",
        0.0,
        18.0,
        10.0,
        step=0.1,
    )

    sex = st.selectbox(
        "Sex",
        ["Male", "Female"],
        key="growth_sex",
    )

    height = st.number_input(
        "Height (cm)",
        30.0,
        220.0,
        135.0,
        key="growth_height",
    )

    weight = st.number_input(
        "Weight (kg)",
        1.0,
        150.0,
        30.0,
        key="growth_weight",
    )

    bmi = bmi_value(weight, height)

    st.metric("Calculated BMI", bmi)

    st.info(
        "BMI alone cannot determine whether a child is growing normally. "
        "Clinical growth assessment requires validated age- and sex-specific "
        "references and, ideally, measurements tracked over time."
    )

    st.markdown("### 📈 What a production growth system would consider")

    for item in [
        "Age",
        "Sex",
        "Height/length",
        "Weight",
        "BMI-for-age",
        "Growth trajectory over time",
        "Validated reference standards",
        "Clinical context",
    ]:
        st.write(f"• {item}")

# ============================================================
# FOOD SCANNER
# ============================================================

elif st.session_state.page == "📷 Food Scanner":

    st.header("📷 Food Scanner")

    st.write(
        "Upload a food image to demonstrate Nouriva's future food-analysis workflow."
    )

    uploaded = st.file_uploader(
        "Upload food image",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded:

        st.image(
            uploaded,
            caption="Uploaded food image",
            use_container_width=True,
        )

        st.success("✅ Image received successfully.")

        st.markdown("### 🔬 Prototype Analysis Workflow")

        steps = [
            "1. Image received",
            "2. Food region would be identified",
            "3. Food category would be classified",
            "4. Nutrient information could be retrieved",
            "5. Results would be presented with confidence information",
        ]

        for step in steps:
            st.write(step)

        st.warning(
            "The current hackathon prototype does not claim to identify "
            "nutrients or diagnose conditions from the image. A validated "
            "computer-vision model would be required for production use."
        )

# ============================================================
# GLOBAL NUTRITION
# ============================================================

elif st.session_state.page == "🌍 Global Nutrition":

    st.header("🌍 Global Nutrition")

    st.write(
        "Explore major nutrition challenges and their connection to global development."
    )

    topic = st.selectbox(
        "Choose a global nutrition topic",
        list(GLOBAL_TOPICS.keys()),
    )

    st.markdown(
        f"""
        <div class="card">
            <h2>{topic}</h2>
            <p>{GLOBAL_TOPICS[topic]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🌎 Why this matters")

    st.write(
        "Nutrition challenges are shaped by health, food availability, "
        "economic conditions, education, environment and access to services. "
        "Solutions therefore require more than a single intervention."
    )

    st.markdown("### 🎯 SDG Connection")

    st.success(
        "Nouriva primarily connects with SDG 2 (Zero Hunger), SDG 3 "
        "(Good Health and Well-Being) and SDG 4 (Quality Education)."
    )

# ============================================================
# HEALTH REPORT
# ============================================================

elif st.session_state.page == "📄 Health Report":

    st.header("📄 Educational Health Report")

    st.write(
        "Generate a downloadable summary from the most recent Nutrition Scan."
    )

    if "report_data" not in st.session_state:

        st.info(
            "No screening result is available yet. Go to Nutrition Scan, "
            "run an analysis, then return here."
        )

        if st.button("Go to Nutrition Scan", use_container_width=True):
            navigate("🔍 Nutrition Scan")
            st.rerun()

    else:

        data = st.session_state.report_data

        st.markdown(
            f"""
            <div class="result-box">
                <h3>🌿 Nouriva AI Screening Summary</h3>
                <p><b>BMI:</b> {data["bmi"]}</p>
                <p><b>Interpretation:</b> {data["bmi_category"]}</p>
                <p><b>Risk:</b> {data["risk_level"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        txt = report_text(data)

        st.download_button(
            "⬇️ Download Educational Report",
            data=txt,
            file_name="Nouriva_AI_Educational_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )

        st.caption(
            "This report is educational and should not be treated as a medical diagnosis."
        )

# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "ℹ️ About Nouriva":

    st.header("ℹ️ About Nouriva AI")

    st.markdown(
        """
        ### 🌿 Nouriva AI

        Nouriva AI is a student-built health-technology prototype focused on:

        - Nutrition awareness
        - Preliminary nutrition screening
        - Nutrition education
        - Meal-planning education
        - Growth-awareness concepts
        - Global nutrition awareness
        - Sustainable Development Goal connections

        ### 💡 Vision

        To demonstrate how accessible digital tools can help people
        better understand nutrition and potential nutrition-related
        concerns.

        ### 👨‍💻 Creator

        **Muhammad Ahsan Shahzad**

        BS Human Nutrition & Dietetics Student

        Pakistan

        ### 🚀 Hackathon Prototype

        Nouriva AI demonstrates an integrated digital nutrition
        education and screening concept built as a student prototype.

        ### ⚠️ Important

        Nouriva AI does **not** diagnose disease, replace healthcare
        professionals or provide definitive medical advice.

        Screening outputs are educational demonstrations and should
        not be used as a substitute for clinical assessment.
        """
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
