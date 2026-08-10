import streamlit as st
import math
import io
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f4fbf6 0%, #eef7ff 100%);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #103c2c 0%, #17624a 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 28px;
        border-radius: 24px;
        background: linear-gradient(135deg, #0d5138, #16805d);
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,.10);
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 18px;
        opacity: .95;
    }

    .card {
        padding: 22px;
        border-radius: 18px;
        background: white;
        border: 1px solid #dcebe4;
        box-shadow: 0 5px 18px rgba(0,0,0,.06);
        min-height: 150px;
        margin-bottom: 15px;
    }

    .card h3 {
        color: #105b40;
    }

    .small {
        color: #667085;
        font-size: 14px;
    }

    .result {
        padding: 22px;
        border-radius: 18px;
        background: #ffffff;
        border-left: 6px solid #15956b;
        box-shadow: 0 5px 18px rgba(0,0,0,.06);
        margin: 15px 0;
    }

    .metric-box {
        padding: 18px;
        border-radius: 16px;
        background: white;
        text-align: center;
        border: 1px solid #dcebe4;
    }

    .footer {
        text-align: center;
        color: #667085;
        padding: 25px;
        margin-top: 35px;
    }

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "screening" not in st.session_state:
    st.session_state.screening = None

if "diet_plan" not in st.session_state:
    st.session_state.diet_plan = None

if "coach_history" not in st.session_state:
    st.session_state.coach_history = []

if "education_score" not in st.session_state:
    st.session_state.education_score = None


# =========================================================
# HELPERS
# =========================================================

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    if height_m <= 0:
        return 0
    return round(weight_kg / (height_m ** 2), 1)


def adult_bmi_category(bmi):
    if bmi < 18.5:
        return "Below standard adult BMI range"
    elif bmi < 25:
        return "Standard adult BMI range"
    elif bmi < 30:
        return "Above standard adult BMI range"
    return "High adult BMI range"


def risk_level(score):
    if score >= 5:
        return "Higher potential risk factors"
    elif score >= 3:
        return "Several potential risk factors"
    elif score >= 1:
        return "Some potential risk factors"
    return "Few identified risk factors"


def nutrition_risk(age, bmi, meals, protein, fruit_veg, food_access):
    score = 0
    factors = []

    if age >= 18 and bmi < 18.5:
        score += 2
        factors.append("BMI below the standard adult range")

    if age >= 18 and bmi >= 30:
        score += 1
        factors.append("BMI in a high adult BMI range")

    if meals <= 2:
        score += 1
        factors.append("Low reported meal frequency")

    if len(protein) == 0:
        score += 1
        factors.append("No listed protein source")

    if fruit_veg == "Rarely":
        score += 1
        factors.append("Low fruit and vegetable intake")

    if food_access == "Often difficult":
        score += 2
        factors.append("Reported difficulty accessing sufficient food")
    elif food_access == "Sometimes difficult":
        score += 1
        factors.append("Occasional difficulty accessing sufficient food")

    return score, factors


def build_diet_plan(goal, style, vegetarian, allergies):
    allergy_text = [a.lower() for a in allergies]

    def allowed(text):
        return not any(a in text.lower() for a in allergy_text)

    if vegetarian:
        protein_options = "dal, beans, chickpeas, yogurt, milk, eggs"
    else:
        protein_options = "dal, eggs, chicken, fish, yogurt"

    if goal == "Healthy weight gain":
        meals = [
            ("Breakfast", "Eggs + roti/paratha + milk + banana"),
            ("Morning snack", "Yogurt + nuts/seeds"),
            ("Lunch", f"Rice/roti + dal + {('vegetarian protein' if vegetarian else 'chicken')} + vegetables"),
            ("Evening snack", "Milk + banana or fruit"),
            ("Dinner", f"Roti + {('beans/dal' if vegetarian else 'beans/meat')} + vegetables + yogurt"),
        ]
    elif goal == "Healthy weight management":
        meals = [
            ("Breakfast", "Eggs or yogurt + whole-grain roti + fruit"),
            ("Morning snack", "Fruit + unsweetened yogurt"),
            ("Lunch", f"Roti/rice + {('dal/beans' if vegetarian else 'chicken/fish')} + vegetables"),
            ("Evening snack", "Fruit + water/milk"),
            ("Dinner", f"Roti + {('dal/beans' if vegetarian else 'fish/chicken')} + vegetables"),
        ]
    elif goal == "Athletic nutrition":
        meals = [
            ("Breakfast", "Eggs + oats/roti + milk + fruit"),
            ("Pre/post activity", "Banana + yogurt or milk"),
            ("Lunch", f"Rice/roti + {('dal/beans' if vegetarian else 'chicken/fish')} + vegetables"),
            ("Snack", "Fruit + yogurt + nuts/seeds"),
            ("Dinner", f"Roti/rice + {('beans/dal' if vegetarian else 'chicken/fish')} + vegetables"),
        ]
    else:
        meals = [
            ("Breakfast", "Eggs/yogurt + roti + fruit"),
            ("Snack", "Fruit + yogurt"),
            ("Lunch", f"Rice/roti + {('dal/beans' if vegetarian else 'chicken/fish')} + vegetables"),
            ("Snack", "Milk + fruit"),
            ("Dinner", f"Roti + {('dal/beans' if vegetarian else 'protein source')} + vegetables"),
        ]

    # Style adjustment
    if style == "Budget-friendly":
        meals = [
            (name, text.replace("nuts/seeds", "roasted chickpeas")
                     .replace("chicken/fish", "dal/beans")
                     .replace("fish/chicken", "dal/beans"))
            for name, text in meals
        ]

    # Allergy warning
    warnings = []
    for name, text in meals:
        for allergy in allergy_text:
            if allergy and allergy in text.lower():
                warnings.append(f"{name}: check the suggested food for your listed allergy.")

    return meals, warnings


COACH_KB = {
    "protein": (
        "Protein supports growth, tissue maintenance and repair and many body functions. "
        "Common sources include eggs, dairy, pulses, fish, meat, nuts and seeds."
    ),
    "hydration": (
        "Water and other appropriate fluids support normal body functions. "
        "Fluid needs vary with age, activity, climate and health status."
    ),
    "iron": (
        "Iron is important for hemoglobin formation and oxygen transport. "
        "Sources include meat, pulses, leafy vegetables and fortified foods."
    ),
    "vitamin": (
        "Vitamins are micronutrients needed for many biological processes. "
        "Different vitamins have different roles and food sources."
    ),
    "calcium": (
        "Calcium supports bones and teeth and also has roles in muscle and nerve function. "
        "Dairy foods and some fortified foods are useful sources."
    ),
    "fiber": (
        "Dietary fiber supports digestive health and can contribute to satiety. "
        "Fruits, vegetables, whole grains, beans and pulses are common sources."
    ),
    "balanced": (
        "A balanced eating pattern includes a variety of foods and adequate energy, "
        "protein, vitamins, minerals and fluids."
    ),
    "malnutrition": (
        "Malnutrition is a broad term that includes undernutrition and other forms of "
        "nutrition imbalance. Assessment should consider the person's age, context and health."
    ),
    "bmi": (
        "BMI is calculated from weight and height. In adults it can be used as a screening "
        "measure, but it does not by itself diagnose health or nutrition status."
    ),
    "food safety": (
        "Food safety includes keeping food clean, separating raw and cooked foods, "
        "cooking foods adequately and storing them safely."
    ),
}


def coach_answer(question):
    q = question.lower()

    for keyword, answer in COACH_KB.items():
        if keyword in q:
            return answer

    return (
        "Nouriva Coach: I can provide general nutrition education about topics such as "
        "protein, hydration, iron, calcium, vitamins, fiber, balanced diets, BMI, "
        "malnutrition and food safety. For personal medical concerns, consult a qualified professional."
    )


EDUCATION = {
    "Balanced Diet": {
        "overview": "A balanced eating pattern provides a variety of foods and nutrients needed for health.",
        "points": [
            "Include a variety of food groups.",
            "Choose appropriate protein sources.",
            "Include fruits and vegetables regularly.",
            "Pay attention to hydration.",
            "Limit excessive intake of highly processed foods."
        ],
        "question": "Which approach best describes a balanced diet?",
        "options": [
            "Only eating one food group",
            "Eating a variety of foods that provide different nutrients",
            "Avoiding all carbohydrates",
            "Drinking water instead of eating"
        ],
        "answer": 1
    },
    "Protein": {
        "overview": "Protein is needed for tissue maintenance, repair and many body functions.",
        "points": [
            "Protein is made of amino acids.",
            "Sources include pulses, eggs, dairy, fish and meat.",
            "Protein needs vary between people.",
            "A varied diet can provide protein."
        ],
        "question": "Which nutrient is especially important for tissue growth and repair?",
        "options": ["Protein", "Water only", "Salt only", "None of these"],
        "answer": 0
    },
    "Micronutrients": {
        "overview": "Micronutrients include vitamins and minerals required in smaller amounts.",
        "points": [
            "Iron is important for hemoglobin.",
            "Calcium supports bones and teeth.",
            "Vitamin A has important roles in vision and immunity.",
            "Different micronutrients have different functions."
        ],
        "question": "Iron is particularly important for:",
        "options": [
            "Hemoglobin formation",
            "Making water",
            "Replacing all protein",
            "None of these"
        ],
        "answer": 0
    },
    "Hydration": {
        "overview": "Adequate fluid intake supports normal physiological functions.",
        "points": [
            "Water is essential for life.",
            "Fluid needs vary.",
            "Hot weather and physical activity can increase fluid losses.",
            "Some foods also contribute to fluid intake."
        ],
        "question": "Which substance is essential for normal hydration?",
        "options": ["Water", "Salt only", "Protein only", "None"],
        "answer": 0
    },
    "Food Safety": {
        "overview": "Food safety reduces the risk of foodborne illness.",
        "points": [
            "Wash hands and surfaces.",
            "Separate raw and cooked foods.",
            "Cook foods appropriately.",
            "Store food at safe temperatures."
        ],
        "question": "Which practice helps reduce food contamination?",
        "options": [
            "Separating raw and cooked foods",
            "Leaving cooked food uncovered for days",
            "Using dirty utensils",
            "None"
        ],
        "answer": 0
    },
    "Fiber": {
        "overview": "Dietary fiber is found mainly in plant foods and supports digestive health.",
        "points": [
            "Fruits and vegetables contain fiber.",
            "Pulses are useful sources.",
            "Whole grains can provide fiber.",
            "Adequate fluids support normal bowel function."
        ],
        "question": "Which is a common source of dietary fiber?",
        "options": ["Pulses", "Only table salt", "Only water", "None"],
        "answer": 0
    },
    "Food Security": {
        "overview": "Food security concerns reliable access to sufficient, safe and nutritious food.",
        "points": [
            "Availability matters.",
            "Access and affordability matter.",
            "Food utilization and safety matter.",
            "Stability over time matters."
        ],
        "question": "Food security is mainly concerned with:",
        "options": [
            "Reliable access to sufficient safe and nutritious food",
            "Only restaurant availability",
            "Only calorie counting",
            "None"
        ],
        "answer": 0
    },
    "Undernutrition": {
        "overview": "Undernutrition can occur when energy or nutrient intake is inadequate or needs are not met.",
        "points": [
            "Undernutrition can affect growth and health.",
            "Children require age-specific assessment.",
            "Causes can include illness, inadequate intake and food insecurity.",
            "Assessment should use appropriate clinical or public-health methods."
        ],
        "question": "Child growth assessment should consider:",
        "options": [
            "Age- and sex-specific references",
            "Adult BMI categories only",
            "Height alone",
            "None"
        ],
        "answer": 0
    },
    "Healthy Weight": {
        "overview": "Healthy weight is influenced by nutrition, activity, genetics, health and many other factors.",
        "points": [
            "Avoid judging health from weight alone.",
            "BMI is a screening measure in adults.",
            "Children require age- and sex-specific growth references.",
            "Individual needs vary."
        ],
        "question": "BMI in adults is best described as:",
        "options": [
            "A screening measure",
            "A complete diagnosis",
            "A blood test",
            "A food allergy test"
        ],
        "answer": 0
    },
    "Nutrition Across the Life Course": {
        "overview": "Nutrition needs and assessment approaches change across different stages of life.",
        "points": [
            "Children need growth-focused assessment.",
            "Adults have different screening considerations.",
            "Older adults may have changing nutritional needs.",
            "Pregnancy and other life stages require specialized guidance."
        ],
        "question": "Do nutritional needs remain exactly the same throughout life?",
        "options": ["No", "Yes, always", "Only for children", "Only for athletes"],
        "answer": 0
    },
}


GLOBAL_TOPICS = {
    "Undernutrition": {
        "description": "Undernutrition includes conditions associated with inadequate energy or nutrient intake and can affect growth, development and health.",
        "impact": "It can affect children and adults and is influenced by health, food access, diet quality and social conditions.",
        "sdgs": "SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being"
    },
    "Food Security": {
        "description": "Food security involves reliable access to sufficient, safe and nutritious food.",
        "impact": "Food insecurity can influence dietary quality, health and vulnerability to nutrition problems.",
        "sdgs": "SDG 2 • Zero Hunger | SDG 1 • No Poverty"
    },
    "Micronutrient Deficiencies": {
        "description": "Micronutrient deficiencies occur when the body does not receive or absorb enough essential vitamins or minerals.",
        "impact": "Deficiencies can affect processes such as blood formation, immunity, growth and development.",
        "sdgs": "SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being"
    },
    "Child Malnutrition": {
        "description": "Child nutrition assessment requires appropriate measures of growth, development and nutritional status.",
        "impact": "Early identification of growth concerns can support timely referral and intervention.",
        "sdgs": "SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being"
    },
    "Sustainable Nutrition": {
        "description": "Sustainable nutrition considers health, food systems, resources and environmental impacts.",
        "impact": "Food choices and food systems can influence both human health and environmental sustainability.",
        "sdgs": "SDG 2 • Zero Hunger | SDG 12 • Responsible Consumption and Production"
    },
}


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 🌿 Nouriva AI")
    st.caption("Nutrition • Education • Awareness")

    page = st.radio(
        "Navigation",
        [
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
        ],
    )

    st.divider()
    st.caption("Student Health-Technology Prototype")
    st.caption("Nouriva AI • 2026")


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>🌿 Nouriva AI</h1>
        <p>AI-Assisted Nutrition Screening & Education</p>
        <p>Nutrition awareness, preliminary screening, education,
        meal planning and global nutrition learning in one platform.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.subheader("Your Nutrition Hub")
    st.write("Choose a tool to explore Nouriva AI.")

    tools = [
        ("🔍", "Nutrition Scan", "BMI, diet and preliminary risk screening."),
        ("🍽️", "Diet Planner", "Generate practical example meal plans."),
        ("🤖", "Nutrition Coach", "Ask general nutrition education questions."),
        ("📚", "Education", "Lessons, key points and knowledge checks."),
        ("📊", "Nutrition Insights", "Indicators, charts and SDG connections."),
        ("🧒", "Growth Monitor", "Explore growth-assessment concepts."),
        ("📷", "Food Scanner", "Upload and analyze a food image workflow."),
        ("🌍", "Global Nutrition", "Explore major global nutrition challenges."),
        ("📄", "Health Report", "Generate a downloadable screening report."),
    ]

    cols = st.columns(3)

    for i, (icon, title, desc) in enumerate(tools):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{icon} {title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Core Tools", "9")

    with c2:
        st.metric("Education Areas", "10")

    with c3:
        st.metric("SDG Connections", "5+")

    with c4:
        st.metric("Status", "Working Prototype")

    st.success(
        "🌱 Nouriva AI demonstrates how accessible digital tools can support "
        "nutrition awareness, preliminary screening and education."
    )


# =========================================================
# NUTRITION SCAN
# =========================================================

elif page == "🔍 Nutrition Scan":

    st.header("🔍 Nutrition Scan")
    st.write(
        "Complete the screening form to calculate BMI and identify "
        "basic nutrition-related risk indicators."
    )

    with st.form("nutrition_form"):

        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age (years)", 1, 120, 20)
            sex = st.selectbox("Sex", ["Male", "Female"])

        with c2:
            height = st.number_input("Height (cm)", 30.0, 250.0, 170.0)
            weight = st.number_input("Weight (kg)", 1.0, 300.0, 55.0)

        meals = st.selectbox(
            "Typical meals per day",
            [1, 2, 3, 4, 5],
            index=2,
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

        fruit_veg = st.selectbox(
            "Fruit & vegetable intake",
            ["Rarely", "Sometimes", "Daily"],
        )

        food_access = st.selectbox(
            "Access to sufficient food",
            [
                "Usually sufficient",
                "Sometimes difficult",
                "Often difficult",
            ],
        )

        submitted = st.form_submit_button(
            "🔍 Analyze Nutrition",
            use_container_width=True,
        )

    if submitted:

        bmi = calculate_bmi(height, weight)

        score, factors = nutrition_risk(
            age,
            bmi,
            meals,
            protein,
            fruit_veg,
            food_access,
        )

        st.session_state.screening = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "meals": meals,
            "protein": protein,
            "fruit_veg": fruit_veg,
            "food_access": food_access,
            "risk_score": score,
            "risk_level": risk_level(score),
            "factors": factors,
        }

    if st.session_state.screening:

        data = st.session_state.screening

        st.divider()
        st.subheader("📊 Screening Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("BMI", data["bmi"])

        with c2:
            st.metric("Risk Score", data["risk_score"])

        with c3:
            st.metric("Risk Level", data["risk_level"])

        if data["age"] >= 18:
            category = adult_bmi_category(data["bmi"])

            if data["bmi"] < 18.5:
                st.warning(f"⚠️ {category}.")
            elif data["bmi"] < 25:
                st.success(f"✅ {category}.")
            elif data["bmi"] < 30:
                st.info(f"ℹ️ {category}.")
            else:
                st.warning(f"⚠️ {category}.")
        else:
            st.info(
                "For people under 18, BMI should be interpreted using "
                "age- and sex-specific growth references rather than adult BMI categories."
            )

        st.subheader("🌱 Identified Factors")

        if data["factors"]:
            for factor in data["factors"]:
                st.write("•", factor)
        else:
            st.success("No basic risk indicators were identified by this prototype.")

        st.subheader("💡 Educational Guidance")

        guidance = [
            "Aim for a varied and balanced eating pattern.",
            "Include suitable protein sources regularly.",
            "Include fruits and vegetables regularly.",
            "Maintain appropriate fluid intake.",
            "Seek professional assessment when you have health or nutrition concerns.",
        ]

        for item in guidance:
            st.write("•", item)

        st.caption(
            "This is a preliminary educational screening tool. "
            "It is not a diagnosis and does not replace professional assessment."
        )


# =========================================================
# DIET PLANNER
# =========================================================

elif page == "🍽️ Diet Planner":

    st.header("🍽️ Nouriva Diet Planner")

    st.write(
        "Build an example day around a general nutrition goal."
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

        style = st.selectbox(
            "Food style",
            [
                "Simple foods",
                "Budget-friendly",
            ],
        )

    with c2:
        vegetarian = st.checkbox("Vegetarian")

        allergies = st.multiselect(
            "Foods to flag for review",
            ["Milk", "Eggs", "Nuts", "Fish", "Chicken"],
        )

    if st.button("🍽️ Generate Meal Plan", use_container_width=True):

        meals, warnings = build_diet_plan(
            goal,
            style,
            vegetarian,
            allergies,
        )

        st.session_state.diet_plan = {
            "goal": goal,
            "style": style,
            "meals": meals,
            "warnings": warnings,
        }

    if st.session_state.diet_plan:

        plan = st.session_state.diet_plan

        st.success(
            f"Selected goal: {plan['goal']} • Style: {plan['style']}"
        )

        for meal_name, meal_text in plan["meals"]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{meal_name}</h3>
                    <p>{meal_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if plan["warnings"]:
            for warning in plan["warnings"]:
                st.warning(warning)

        st.info(
            "These are example educational meal ideas, not individualized medical diets. "
            "Personal dietary needs can vary."
        )


# =========================================================
# NUTRITION COACH
# =========================================================

elif page == "🤖 Nutrition Coach":

    st.header("🤖 Nouriva Nutrition Coach")

    st.write(
        "Ask a general nutrition education question."
    )

    question = st.text_input(
        "Your question",
        placeholder="Example: Why is protein important?",
    )

    if st.button("🤖 Ask Nouriva", use_container_width=True):

        if question.strip():

            answer = coach_answer(question)

            st.session_state.coach_history.append(
                {
                    "question": question,
                    "answer": answer,
                }
            )

    if st.session_state.coach_history:

        for item in reversed(st.session_state.coach_history[-5:]):

            st.markdown(
                f"""
                <div class="result">
                    <strong>Question</strong><br>
                    {item['question']}<br><br>
                    <strong>🌿 Nouriva Coach</strong><br>
                    {item['answer']}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "Prototype educational assistant. It does not provide diagnosis or individualized medical treatment."
    )


# =========================================================
# EDUCATION
# =========================================================

elif page == "📚 Education":

    st.header("📚 Nutrition Education")

    st.write(
        "Explore structured lessons, key points and knowledge checks."
    )

    topic = st.selectbox(
        "Choose a learning topic",
        list(EDUCATION.keys()),
    )

    lesson = EDUCATION[topic]

    st.subheader(topic)

    st.info(lesson["overview"])

    st.subheader("📌 Key Points")

    for point in lesson["points"]:
        st.write("•", point)

    st.divider()

    st.subheader("🧠 Knowledge Check")

    answer = st.radio(
        lesson["question"],
        lesson["options"],
        key=f"quiz_{topic}",
    )

    if st.button("Check Answer", use_container_width=True):

        selected_index = lesson["options"].index(answer)

        if selected_index == lesson["answer"]:
            st.success("✅ Correct! Good work.")
            st.session_state.education_score = 1
        else:
            correct = lesson["options"][lesson["answer"]]
            st.error(f"❌ Not quite. Correct answer: {correct}")
            st.session_state.education_score = 0

    if st.session_state.education_score is not None:
        st.metric(
            "Latest Quiz Result",
            "1 / 1" if st.session_state.education_score else "0 / 1",
        )


# =========================================================
# INSIGHTS
# =========================================================

elif page == "📊 Nutrition Insights":

    st.header("📊 Nutrition Insights")

    st.write(
        "Explore example nutrition indicators and their relationship to global goals."
    )

    indicator = st.selectbox(
        "Choose an indicator",
        [
            "BMI Screening Categories",
            "Nutrition Risk Factors",
            "SDG Connections",
        ],
    )

    if indicator == "BMI Screening Categories":

        df = pd.DataFrame(
            {
                "Category": [
                    "Below standard",
                    "Standard range",
                    "Above standard",
                    "High range",
                ],
                "Example": [18.5, 25, 30, 35],
            }
        )

        st.bar_chart(
            df.set_index("Category")
        )

        st.info(
            "Adult BMI categories are screening concepts and should not be interpreted as a complete health diagnosis."
        )

    elif indicator == "Nutrition Risk Factors":

        df = pd.DataFrame(
            {
                "Factor": [
                    "Low meals",
                    "No protein source",
                    "Rare fruit/vegetables",
                    "Food access difficulty",
                ],
                "Screening weight": [1, 1, 1, 2],
            }
        )

        st.bar_chart(
            df.set_index("Factor")
        )

        st.info(
            "The values shown are prototype screening weights, not validated clinical scores."
        )

    else:

        sdg_df = pd.DataFrame(
            {
                "SDG": [
                    "SDG 2",
                    "SDG 3",
                    "SDG 4",
                    "SDG 12",
                    "SDG 1",
                ],
                "Connection": [
                    5,
                    5,
                    4,
                    2,
                    2,
                ],
            }
        )

        st.bar_chart(
            sdg_df.set_index("SDG")
        )

        st.success(
            "Nouriva connects nutrition awareness primarily with Zero Hunger, "
            "Good Health and Well-Being, and Quality Education."
        )


# =========================================================
# GROWTH MONITOR
# =========================================================

elif page == "🧒 Growth Monitor":

    st.header("🧒 Growth Monitor")

    st.write(
        "Educational demonstration of how child growth assessment can begin with basic measurements."
    )

    c1, c2 = st.columns(2)

    with c1:
        child_age = st.number_input(
            "Age (years)",
            0.1,
            19.0,
            10.0,
        )

        child_sex = st.selectbox(
            "Sex",
            ["Male", "Female"],
            key="growth_sex",
        )

    with c2:
        child_height = st.number_input(
            "Height (cm)",
            30.0,
            220.0,
            140.0,
        )

        child_weight = st.number_input(
            "Weight (kg)",
            1.0,
            150.0,
            35.0,
        )

    if st.button("🧒 Assess Growth Information", use_container_width=True):

        child_bmi = calculate_bmi(
            child_height,
            child_weight,
        )

        st.subheader("Growth Information")

        c1, c2 = st.columns(2)

        with c1:
            st.metric("BMI", child_bmi)

        with c2:
            st.metric("Age", f"{child_age:g} years")

        st.info(
            "BMI alone cannot determine whether a child is growing normally. "
            "Clinical growth assessment requires validated age- and sex-specific "
            "growth references and appropriate professional interpretation."
        )

        if child_age < 5:
            st.warning(
                "For young children, specialized growth standards are especially important."
            )
        else:
            st.success(
                "The prototype has captured the basic measurements needed for a future growth-reference module."
            )


# =========================================================
# FOOD SCANNER
# =========================================================

elif page == "📷 Food Scanner":

    st.header("📷 Food Scanner")

    st.write(
        "Upload a food image to demonstrate Nouriva's prototype image-analysis workflow."
    )

    uploaded = st.file_uploader(
        "Upload a food image",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded:

        st.image(
            uploaded,
            caption="Uploaded food image",
            use_container_width=True,
        )

        image_bytes = uploaded.getvalue()

        st.subheader("🔬 Prototype Image Analysis")

        try:

            from PIL import Image

            image = Image.open(io.BytesIO(image_bytes))

            width, height = image.size

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Image Width", f"{width}px")

            with c2:
                st.metric("Image Height", f"{height}px")

            with c3:
                st.metric("File Size", f"{len(image_bytes) / 1024:.1f} KB")

            st.success(
                "Image successfully received and processed by the prototype."
            )

            st.info(
                "A production Nouriva AI food-recognition model could identify foods, "
                "estimate portions and connect recognized foods to a nutrition database. "
                "This prototype intentionally does not claim to identify food reliably without a trained model."
            )

        except Exception as e:
            st.error(f"Image processing error: {e}")


# =========================================================
# GLOBAL NUTRITION
# =========================================================

elif page == "🌍 Global Nutrition":

    st.header("🌍 Global Nutrition")

    st.write(
        "Explore major nutrition challenges and their connection to global development."
    )

    topic = st.selectbox(
        "Choose a global nutrition topic",
        list(GLOBAL_TOPICS.keys()),
    )

    data = GLOBAL_TOPICS[topic]

    st.subheader(topic)

    st.info(data["description"])

    st.subheader("🌎 Why This Matters")

    st.write(data["impact"])

    st.subheader("🎯 SDG Connection")

    st.success(data["sdgs"])

    st.subheader("🌱 Nouriva Perspective")

    st.write(
        "Nutrition challenges are influenced by health, food availability, "
        "economic conditions, education, environment and access to services. "
        "Digital education and early awareness can be part of a broader solution."
    )


# =========================================================
# HEALTH REPORT
# =========================================================

elif page == "📄 Health Report":

    st.header("📄 Health Report")

    if not st.session_state.screening:

        st.warning(
            "Complete the Nutrition Scan first so Nouriva can generate a report."
        )

    else:

        data = st.session_state.screening

        st.success(
            "Screening data found. Your educational report is ready."
        )

        report = f"""
NOURIVA AI
Nutrition Screening & Education Report
======================================

Generated: {data['date']}

PERSON INFORMATION
------------------
Age: {data['age']}
Sex: {data['sex']}
Height: {data['height']} cm
Weight: {data['weight']} kg

SCREENING
---------
BMI: {data['bmi']}
BMI interpretation: {adult_bmi_category(data['bmi']) if data['age'] >= 18 else 'Age-specific interpretation required'}

Reported meals per day: {data['meals']}
Protein sources: {', '.join(data['protein']) if data['protein'] else 'None listed'}
Fruit/vegetable intake: {data['fruit_veg']}
Food access: {data['food_access']}

PRELIMINARY RISK
----------------
Prototype score: {data['risk_score']}
Result: {data['risk_level']}

Factors:
{chr(10).join('- ' + x for x in data['factors']) if data['factors'] else '- No basic risk indicators identified'}

GENERAL EDUCATIONAL GUIDANCE
----------------------------
- Aim for a varied and balanced eating pattern.
- Include suitable protein sources.
- Include fruits and vegetables regularly.
- Maintain appropriate fluid intake.
- Seek professional advice for health or nutrition concerns.

IMPORTANT DISCLAIMER
--------------------
This report is generated by a student-built educational prototype.
It is not a medical diagnosis and should not replace assessment by
a qualified healthcare or nutrition professional.

Nouriva AI • Nutrition • Education • Awareness
"""

        st.text_area(
            "Report Preview",
            report,
            height=420,
        )

        st.download_button(
            "⬇️ Download Health Report",
            data=report,
            file_name="Nouriva_AI_Nutrition_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About Nouriva":

    st.header("ℹ️ About Nouriva AI")

    st.markdown(
        """
### 🌿 Nouriva AI

Nouriva AI is a student-built health-technology prototype focused on
nutrition awareness, preliminary screening and accessible digital education.

### 🎯 Problem

Nutrition challenges can involve inadequate intake, poor dietary quality,
food insecurity, micronutrient deficiencies and other interacting factors.

### 💡 Solution

Nouriva combines:

- Preliminary nutrition screening
- BMI calculation
- Nutrition-risk indicators
- Meal planning
- Nutrition education
- Educational nutrition coaching
- Growth-awareness concepts
- Food-image workflow
- Nutrition insights
- Global nutrition education
- Downloadable screening reports

### 🌍 Global Goals

The project connects particularly with:

- SDG 2 — Zero Hunger
- SDG 3 — Good Health and Well-Being
- SDG 4 — Quality Education
- SDG 12 — Responsible Consumption and Production
- SDG 1 — No Poverty

### 👨‍💻 Creator

**Muhammad Ahsan Shahzad**

BS Human Nutrition & Dietetics Student  
Pakistan

### 🚀 Hackathon Prototype

Nouriva AI demonstrates how accessible digital tools can support nutrition
awareness and education.

### ⚠️ Important

Nouriva AI is an educational prototype.

It does not diagnose disease, prescribe treatment or replace qualified
healthcare professionals.
"""
    )


# =========================================================
# FOOTER
# =========================================================

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
