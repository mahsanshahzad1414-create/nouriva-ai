import io
from datetime import datetime

import pandas as pd
import streamlit as st
from PIL import Image


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM DESIGN
# =========================================================

st.markdown(
    """
<style>

/* ---------- GLOBAL ---------- */

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(0,255,140,.08), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(255,40,60,.06), transparent 25%),
        #07100c;
    color: #f5f7f6;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050807 0%, #0a1711 55%, #07100c 100%);
    border-right: 1px solid #173a2a;
}

[data-testid="stSidebar"] * {
    color: #f4f7f5 !important;
}

[data-testid="stSidebar"] .stRadio label {
    border-radius: 10px;
}

/* ---------- TYPOGRAPHY ---------- */

h1, h2, h3, h4 {
    color: #f5f7f6 !important;
}

p, li, label, span, div {
    color: inherit;
}

/* ---------- HERO ---------- */

.hero {
    background:
        linear-gradient(135deg, rgba(13,83,52,.98), rgba(3,16,11,.98));
    border: 1px solid #1b6e48;
    border-radius: 28px;
    padding: 38px;
    margin-bottom: 25px;
    box-shadow: 0 20px 60px rgba(0,0,0,.35);
}

.hero h1 {
    font-size: clamp(34px, 5vw, 58px);
    margin: 0;
    font-weight: 800;
}

.hero .accent {
    color: #39e58b;
}

.hero p {
    color: #d8e9df !important;
    font-size: 17px;
}

/* ---------- CARDS ---------- */

.n-card {
    background: linear-gradient(145deg, #101914, #0a100d);
    border: 1px solid #1b392b;
    border-radius: 20px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,.25);
}

.n-card:hover {
    border-color: #2acb79;
}

.n-card h3 {
    color: #4bea97 !important;
    margin-top: 0;
}

.n-card p {
    color: #c9d7cf !important;
}

/* ---------- RESULT ---------- */

.result-card {
    background: #101713;
    border: 1px solid #28533d;
    border-left: 6px solid #32d681;
    border-radius: 18px;
    padding: 24px;
    margin: 18px 0;
    box-shadow: 0 12px 35px rgba(0,0,0,.30);
}

.result-card h3 {
    color: #52ee9e !important;
}

.result-card p,
.result-card li {
    color: #e3ebe6 !important;
}

/* ---------- WARNING ---------- */

.warning-card {
    background: #24100f;
    border: 1px solid #a93631;
    border-left: 6px solid #ff4d4d;
    border-radius: 18px;
    padding: 22px;
    margin: 18px 0;
}

.warning-card h3 {
    color: #ff7777 !important;
}

.warning-card p,
.warning-card li {
    color: #ffe2e2 !important;
}

/* ---------- RED ACCENT ---------- */

.red-accent {
    color: #ff5757 !important;
}

/* ---------- STAT ---------- */

.stat {
    background: #0e1612;
    border: 1px solid #244534;
    border-radius: 18px;
    padding: 22px;
    text-align: center;
}

.stat-number {
    font-size: 32px;
    font-weight: 800;
    color: #42e995 !important;
}

.stat-label {
    color: #aabbb1 !important;
}

/* ---------- BUTTONS ---------- */

.stButton > button,
.stDownloadButton > button {
    border-radius: 12px !important;
    min-height: 45px !important;
    font-weight: 700 !important;
}

.stButton > button[kind="primary"] {
    background: #19a866 !important;
    color: white !important;
    border: 1px solid #39e58b !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #42e995 !important;
}

/* ---------- INPUTS ---------- */

div[data-baseweb="input"],
div[data-baseweb="select"],
div[data-baseweb="textarea"] {
    background: #101713 !important;
}

input,
textarea {
    color: #f5f7f6 !important;
}

/* ---------- METRICS ---------- */

[data-testid="stMetric"] {
    background: #0e1612;
    border: 1px solid #244534;
    border-radius: 16px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #aebfb5 !important;
}

[data-testid="stMetricValue"] {
    color: #48e995 !important;
}

/* ---------- DIVIDER ---------- */

hr {
    border-color: #1b392b !important;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #8fa097 !important;
    border-top: 1px solid #193326;
    margin-top: 45px;
    padding: 28px;
}

.footer strong {
    color: #3de68f !important;
}

/* ---------- MOBILE ---------- */

@media (max-width: 800px) {
    .hero {
        padding: 25px;
    }

    .hero h1 {
        font-size: 36px;
    }

    .n-card {
        padding: 18px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "screening": None,
    "diet_plan": None,
    "coach_history": [],
    "quiz_results": {},
    "food_analysis": None,
    "growth_result": None,
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DATA
# =========================================================

EDUCATION = {
    "Balanced Diet": {
        "category": "Foundations",
        "overview": "A balanced eating pattern provides a variety of foods and nutrients needed to support normal body functions, growth and daily activity.",
        "points": [
            "Include a variety of food groups.",
            "Choose suitable protein sources.",
            "Include fruits and vegetables regularly.",
            "Choose appropriate sources of carbohydrates and fats.",
            "Maintain adequate fluid intake.",
        ],
        "practical": [
            "Build meals around a staple food, protein source and vegetables.",
            "Use seasonal and locally available foods when practical.",
            "Aim for variety across the week rather than relying on one food.",
        ],
        "question": "Which approach best describes a balanced diet?",
        "options": [
            "Eating only one food group",
            "Eating a variety of foods that provide different nutrients",
            "Avoiding all carbohydrates",
            "Replacing meals with water",
        ],
        "answer": 1,
    },
    "Protein": {
        "category": "Macronutrients",
        "overview": "Protein is made of amino acids and supports tissue maintenance, repair, growth and many physiological functions.",
        "points": [
            "Protein is found in both animal and plant foods.",
            "Eggs, dairy, pulses, fish and meat can provide protein.",
            "Protein requirements vary by age, body size and physiological state.",
            "A varied diet can provide protein.",
        ],
        "practical": [
            "Add pulses, eggs, dairy or another suitable protein source to meals.",
            "Combine different plant foods across the day for dietary variety.",
        ],
        "question": "Which nutrient is especially important for tissue growth and repair?",
        "options": ["Protein", "Water only", "Salt only", "None of these"],
        "answer": 0,
    },
    "Carbohydrates": {
        "category": "Macronutrients",
        "overview": "Carbohydrates are an important source of energy and are found in foods such as grains, fruits, vegetables and pulses.",
        "points": [
            "Carbohydrates provide energy.",
            "Whole grains and pulses can also provide fiber.",
            "Fruit and vegetables contain carbohydrate along with other nutrients.",
            "Food quality and overall dietary pattern matter.",
        ],
        "practical": [
            "Choose a variety of carbohydrate sources.",
            "Include whole grains or pulses where available.",
        ],
        "question": "What is a major role of carbohydrates?",
        "options": [
            "Providing energy",
            "Replacing all vitamins",
            "Being the only source of protein",
            "None",
        ],
        "answer": 0,
    },
    "Fats": {
        "category": "Macronutrients",
        "overview": "Dietary fats provide energy and support several important body functions. Different types of fat have different nutritional characteristics.",
        "points": [
            "Fat is energy dense.",
            "Some fats are essential in the diet.",
            "Nuts, seeds and many plant oils provide unsaturated fats.",
            "Overall dietary pattern matters more than one food alone.",
        ],
        "practical": [
            "Use fats in appropriate amounts.",
            "Include varied sources rather than relying on one type.",
        ],
        "question": "Which foods can provide unsaturated fats?",
        "options": [
            "Nuts and seeds",
            "Only table salt",
            "Only water",
            "None",
        ],
        "answer": 0,
    },
    "Micronutrients": {
        "category": "Vitamins & Minerals",
        "overview": "Micronutrients include vitamins and minerals required in smaller amounts but involved in many essential biological processes.",
        "points": [
            "Iron contributes to hemoglobin formation.",
            "Calcium supports bones and teeth.",
            "Vitamin A has roles in vision and immunity.",
            "Different micronutrients have different functions.",
        ],
        "practical": [
            "Eat a varied diet containing different food groups.",
            "Use fortified foods where appropriate and available.",
        ],
        "question": "Iron is particularly important for:",
        "options": [
            "Hemoglobin formation",
            "Making water",
            "Replacing all protein",
            "None",
        ],
        "answer": 0,
    },
    "Hydration": {
        "category": "Vitamins & Minerals",
        "overview": "Water is essential for normal physiological functions. Fluid requirements vary with climate, activity, age and health.",
        "points": [
            "Water supports many body processes.",
            "Hot weather can increase fluid losses.",
            "Physical activity can increase fluid needs.",
            "Some foods also contribute to fluid intake.",
        ],
        "practical": [
            "Drink fluids regularly according to thirst and circumstances.",
            "Pay attention to fluid needs during heat and physical activity.",
        ],
        "question": "Which substance is essential for normal hydration?",
        "options": ["Water", "Salt only", "Protein only", "None"],
        "answer": 0,
    },
    "Fiber": {
        "category": "Vitamins & Minerals",
        "overview": "Dietary fiber is found mainly in plant foods and supports digestive health and other aspects of a healthy dietary pattern.",
        "points": [
            "Pulses are useful sources of fiber.",
            "Fruits and vegetables provide fiber.",
            "Whole grains can provide fiber.",
            "Adequate fluids support normal bowel function.",
        ],
        "practical": [
            "Include pulses, vegetables, fruits and whole grains regularly.",
            "Increase dietary variety gradually.",
        ],
        "question": "Which is a common source of dietary fiber?",
        "options": ["Pulses", "Only table salt", "Only water", "None"],
        "answer": 0,
    },
    "Food Safety": {
        "category": "Food Safety",
        "overview": "Food safety practices reduce the risk of contamination and foodborne illness.",
        "points": [
            "Keep hands and surfaces clean.",
            "Separate raw and cooked foods.",
            "Cook food appropriately.",
            "Store food safely.",
        ],
        "practical": [
            "Wash hands before preparing food.",
            "Keep raw meat separate from ready-to-eat foods.",
            "Avoid consuming visibly spoiled food.",
        ],
        "question": "Which practice helps reduce food contamination?",
        "options": [
            "Separating raw and cooked foods",
            "Leaving cooked food uncovered for days",
            "Using dirty utensils",
            "None",
        ],
        "answer": 0,
    },
    "Food Security": {
        "category": "Public Health",
        "overview": "Food security concerns reliable access to sufficient, safe and nutritious food.",
        "points": [
            "Availability matters.",
            "Access and affordability matter.",
            "Food safety and utilization matter.",
            "Stability over time matters.",
        ],
        "practical": [
            "Consider affordability and availability when planning meals.",
            "Community and policy solutions are important alongside individual choices.",
        ],
        "question": "Food security is mainly concerned with:",
        "options": [
            "Reliable access to sufficient safe and nutritious food",
            "Only restaurant availability",
            "Only calorie counting",
            "None",
        ],
        "answer": 0,
    },
    "Undernutrition": {
        "category": "Public Health",
        "overview": "Undernutrition can occur when energy or nutrient needs are not adequately met and may affect growth, development and health.",
        "points": [
            "Undernutrition can affect children and adults.",
            "Causes can include inadequate intake and illness.",
            "Food insecurity can contribute.",
            "Assessment depends on age and context.",
        ],
        "practical": [
            "Persistent concerns about growth, weight or intake warrant professional assessment.",
            "Children should be assessed with appropriate growth references.",
        ],
        "question": "Child growth assessment should consider:",
        "options": [
            "Age- and sex-specific references",
            "Adult BMI categories only",
            "Height alone",
            "None",
        ],
        "answer": 0,
    },
    "Nutrition Across the Life Course": {
        "category": "Life Course",
        "overview": "Nutrition needs and assessment approaches change across stages of life.",
        "points": [
            "Children require growth-focused assessment.",
            "Adults have different screening considerations.",
            "Older adults may have changing nutritional needs.",
            "Pregnancy and other physiological states require specialized guidance.",
        ],
        "practical": [
            "Avoid assuming one nutrition plan is appropriate for everyone.",
            "Use age and life-stage appropriate guidance.",
        ],
        "question": "Do nutritional needs remain exactly the same throughout life?",
        "options": [
            "No",
            "Yes, always",
            "Only for children",
            "Only for athletes",
        ],
        "answer": 0,
    },
}


GLOBAL_TOPICS = {
    "Undernutrition": {
        "description": "Undernutrition includes conditions associated with inadequate energy or nutrient intake and can affect growth, development and health.",
        "impact": "It is influenced by diet, illness, food access, living conditions, education and health services.",
        "sdgs": ["SDG 2 — Zero Hunger", "SDG 3 — Good Health and Well-Being"],
        "actions": [
            "Improve access to nutritious foods.",
            "Strengthen nutrition education.",
            "Support early identification and referral.",
        ],
    },
    "Food Security": {
        "description": "Food security means people have reliable access to sufficient, safe and nutritious food.",
        "impact": "Food insecurity can affect dietary quality, health and vulnerability to nutrition problems.",
        "sdgs": ["SDG 2 — Zero Hunger", "SDG 1 — No Poverty"],
        "actions": [
            "Improve affordability and access.",
            "Support resilient food systems.",
            "Reduce food waste and loss.",
        ],
    },
    "Micronutrient Deficiencies": {
        "description": "Micronutrient deficiencies occur when the body does not receive or absorb enough essential vitamins or minerals.",
        "impact": "They can affect processes including blood formation, immunity, growth and development.",
        "sdgs": ["SDG 2 — Zero Hunger", "SDG 3 — Good Health and Well-Being"],
        "actions": [
            "Increase dietary diversity.",
            "Use appropriate fortification strategies.",
            "Improve access to nutrition services.",
        ],
    },
    "Child Malnutrition": {
        "description": "Child nutrition assessment requires appropriate measures of growth, development and nutritional status.",
        "impact": "Early identification of growth concerns can support timely professional assessment and intervention.",
        "sdgs": ["SDG 2 — Zero Hunger", "SDG 3 — Good Health and Well-Being"],
        "actions": [
            "Use validated growth references.",
            "Monitor growth over time.",
            "Refer concerns for professional assessment.",
        ],
    },
    "Sustainable Nutrition": {
        "description": "Sustainable nutrition considers health, food systems, resources and environmental impacts.",
        "impact": "Food choices and food systems can influence both human health and environmental sustainability.",
        "sdgs": [
            "SDG 2 — Zero Hunger",
            "SDG 12 — Responsible Consumption and Production",
        ],
        "actions": [
            "Reduce avoidable food waste.",
            "Support diverse and resilient food systems.",
            "Consider both nutrition and environmental context.",
        ],
    },
}


COACH_KB = {
    "protein": "Protein supports tissue maintenance, repair, growth and many body functions. Common sources include eggs, dairy, pulses, fish, meat, nuts and seeds.",
    "hydration": "Water and other appropriate fluids support normal body functions. Fluid needs vary with age, activity, climate and health.",
    "iron": "Iron contributes to hemoglobin formation and oxygen transport. Sources include meat, pulses, leafy vegetables and fortified foods.",
    "calcium": "Calcium supports bones and teeth and also has roles in muscle and nerve function. Dairy and fortified foods can provide calcium.",
    "fiber": "Dietary fiber is found mainly in plant foods. Fruits, vegetables, pulses and whole grains are common sources.",
    "balanced diet": "A balanced eating pattern includes a variety of foods and adequate energy, protein, vitamins, minerals and fluids.",
    "bmi": "BMI is calculated from weight and height. In adults it can be used as a screening measure, but it does not by itself diagnose health or nutrition status.",
    "food safety": "Food safety includes keeping food clean, separating raw and cooked foods, cooking food appropriately and storing it safely.",
    "malnutrition": "Malnutrition is a broad term that includes undernutrition and other forms of nutrition imbalance. Assessment should consider age, context and health.",
    "vitamin": "Vitamins are micronutrients needed for many biological processes. Different vitamins have different roles and food sources.",
}


# =========================================================
# HELPERS
# =========================================================

def calculate_bmi(height_cm, weight_kg):
    if height_cm <= 0:
        return 0
    meters = height_cm / 100
    return round(weight_kg / (meters * meters), 1)


def adult_bmi_category(bmi):
    if bmi < 18.5:
        return "Below standard adult BMI range"
    if bmi < 25:
        return "Standard adult BMI range"
    if bmi < 30:
        return "Above standard adult BMI range"
    return "High adult BMI range"


def nutrition_risk(age, bmi, meals, protein, fruit_veg, food_access):
    score = 0
    factors = []

    if age >= 18 and bmi < 18.5:
        score += 2
        factors.append("BMI below the standard adult range.")

    if age >= 18 and bmi >= 30:
        score += 1
        factors.append("BMI in a high adult BMI range.")

    if meals <= 2:
        score += 1
        factors.append("Low reported meal frequency.")

    if not protein:
        score += 1
        factors.append("No listed protein source.")

    if fruit_veg == "Rarely":
        score += 1
        factors.append("Low reported fruit and vegetable intake.")

    if food_access == "Often difficult":
        score += 2
        factors.append("Reported difficulty accessing sufficient food.")
    elif food_access == "Sometimes difficult":
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


def build_meal_plan(goal, style, vegetarian, allergies):
    allergies_lower = [x.lower() for x in allergies]

    if vegetarian:
        lunch_protein = "dal / chickpeas / beans"
        dinner_protein = "beans / dal / yogurt"
    else:
        lunch_protein = "chicken / fish / dal"
        dinner_protein = "chicken / fish / beans"

    if goal == "Healthy weight gain":
        meals = [
            ("Breakfast", "Eggs + roti/paratha + milk + banana"),
            ("Morning snack", "Yogurt + roasted chickpeas or nuts"),
            ("Lunch", f"Rice/roti + {lunch_protein} + vegetables"),
            ("Evening snack", "Milk + banana or another fruit"),
            ("Dinner", f"Roti + {dinner_protein} + vegetables + yogurt"),
        ]

    elif goal == "Healthy weight management":
        meals = [
            ("Breakfast", "Eggs or yogurt + roti + fruit"),
            ("Morning snack", "Fruit + plain yogurt"),
            ("Lunch", f"Roti/rice + {lunch_protein} + vegetables"),
            ("Evening snack", "Fruit or yogurt"),
            ("Dinner", f"Roti + {dinner_protein} + vegetables"),
        ]

    elif goal == "Athletic nutrition":
        meals = [
            ("Breakfast", "Eggs + oats/roti + milk + fruit"),
            ("Pre/post activity", "Banana + yogurt or milk"),
            ("Lunch", f"Rice/roti + {lunch_protein} + vegetables"),
            ("Snack", "Fruit + yogurt + nuts/seeds"),
            ("Dinner", f"Roti/rice + {dinner_protein} + vegetables"),
        ]

    else:
        meals = [
            ("Breakfast", "Eggs/yogurt + roti + fruit"),
            ("Morning snack", "Fruit + yogurt"),
            ("Lunch", f"Rice/roti + {lunch_protein} + vegetables"),
            ("Evening snack", "Milk + fruit"),
            ("Dinner", f"Roti + {dinner_protein} + vegetables"),
        ]

    if style == "Budget-friendly":
        meals = [
            (
                name,
                text.replace("nuts/seeds", "roasted chickpeas")
                .replace("chicken / fish", "dal / beans"),
            )
            for name, text in meals
        ]

    warnings = []

    for allergy in allergies_lower:
        for name, text in meals:
            if allergy and allergy in text.lower():
                warnings.append(
                    f"{name}: review the suggested food because '{allergy}' was flagged."
                )

    return meals, warnings


def coach_answer(question):
    q = question.lower().strip()

    for keyword, answer in COACH_KB.items():
        if keyword in q:
            return answer

    return (
        "I can explain general nutrition topics including protein, carbohydrates, "
        "fats, hydration, iron, calcium, vitamins, fiber, balanced diets, BMI, "
        "food safety, food security and malnutrition. "
        "For personal medical concerns, consult a qualified professional."
    )


def make_report(data):
    factors = (
        "\n".join(f"- {x}" for x in data["factors"])
        if data["factors"]
        else "- No basic prototype risk indicators identified."
    )

    return f"""
NOURIVA AI
NUTRITION SCREENING & EDUCATION REPORT
=======================================

Generated: {data["date"]}

PERSON INFORMATION
------------------
Age: {data["age"]}
Sex: {data["sex"]}
Height: {data["height"]} cm
Weight: {data["weight"]} kg

SCREENING
---------
BMI: {data["bmi"]}

BMI interpretation:
{adult_bmi_category(data["bmi"]) if data["age"] >= 18 else "Age-specific interpretation required"}

Reported meals per day: {data["meals"]}
Protein sources: {", ".join(data["protein"]) if data["protein"] else "None listed"}
Fruit & vegetable intake: {data["fruit_veg"]}
Food access: {data["food_access"]}

PROTOTYPE RISK SCREEN
---------------------
Score: {data["risk_score"]}
Level: {data["risk_level"]}

Identified factors:
{factors}

GENERAL EDUCATIONAL GUIDANCE
----------------------------
- Aim for a varied and balanced eating pattern.
- Include suitable protein sources regularly.
- Include fruits and vegetables regularly.
- Maintain appropriate fluid intake.
- Seek professional nutrition or healthcare advice for persistent concerns.

IMPORTANT
---------
This report is generated by a student-built educational prototype.
The BMI interpretation and risk score are screening/educational tools,
not diagnoses or validated clinical risk scores.

Nouriva AI • Nutrition • Education • Awareness
Student Health-Technology Prototype • 2026
"""


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            padding:14px;
            border:1px solid #23583c;
            border-radius:16px;
            background:#0b1510;
            margin-bottom:18px;">
            <h2 style="color:#45e994;margin:0;">🌿 Nouriva AI</h2>
            <small style="color:#a8b9af;">Nutrition • Education • Awareness</small>
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

    page = st.radio(
        "Navigation",
        pages,
        key="main_navigation",
    )

    st.divider()

    st.markdown(
        """
        **NOURIVA**
        
        Student Health-Technology Prototype
        
        **2026**
        """
    )


# =========================================================
# TOP HERO
# =========================================================

st.markdown(
    """
<div class="hero">
    <h1>🌿 Nouriva <span class="accent">AI</span></h1>
    <p><b>AI-Assisted Nutrition Screening & Education</b></p>
    <p>
        Nutrition awareness, preliminary screening, education,
        meal planning and global nutrition learning — brought together
        in one student-built platform.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.subheader("Your Nutrition Hub")
    st.write("Choose a module to start.")

    tools = [
        ("🔍", "Nutrition Scan", "BMI + preliminary nutrition indicators.", "🔍 Nutrition Scan"),
        ("🍽️", "Diet Planner", "Build practical example meal plans.", "🍽️ Diet Planner"),
        ("🤖", "Nutrition Coach", "Ask general nutrition questions.", "🤖 Nutrition Coach"),
        ("📚", "Education", "Lessons, practical points and quizzes.", "📚 Education"),
        ("📊", "Insights", "Charts, indicators and SDG connections.", "📊 Nutrition Insights"),
        ("🧒", "Growth Monitor", "Explore growth assessment concepts.", "🧒 Growth Monitor"),
        ("📷", "Food Scanner", "Upload a food image.", "📷 Food Scanner"),
        ("🌍", "Global Nutrition", "Explore global nutrition challenges.", "🌍 Global Nutrition"),
        ("📄", "Health Report", "Generate and download your report.", "📄 Health Report"),
    ]

    cols = st.columns(3)

    for i, (icon, title, desc, target) in enumerate(tools):

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="n-card">
                    <h3>{icon} {title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Open {title}",
                key=f"dashboard_{i}",
                width="stretch",
                type="primary",
            ):
                st.session_state.main_navigation = target
                st.rerun()

    st.divider()

    stats = st.columns(4)

    stat_data = [
        ("09", "Core Modules"),
        ("11+", "Education Topics"),
        ("05", "SDG Connections"),
        ("24/7", "Prototype Access"),
    ]

    for col, (number, label) in zip(stats, stat_data):
        with col:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="stat-number">{number}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="result-card">
            <h3>🌱 Nouriva Purpose</h3>
            <p>
            Nouriva AI demonstrates how accessible digital tools can support
            nutrition awareness, preliminary screening, education and global
            nutrition learning.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# NUTRITION SCAN
# =========================================================

elif page == "🔍 Nutrition Scan":

    st.header("🔍 Nutrition Scan")

    st.write(
        "Enter basic information to calculate BMI and explore "
        "prototype nutrition-related indicators."
    )

    with st.form("nutrition_scan_form"):

        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age (years)", 1, 120, 20)
            sex = st.selectbox("Sex", ["Male", "Female"])

        with c2:
            height = st.number_input("Height (cm)", 30.0, 250.0, 170.0, step=0.5)
            weight = st.number_input("Weight (kg)", 1.0, 300.0, 55.0, step=0.5)

        st.subheader("Diet & Lifestyle")

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
            type="primary",
            width="stretch",
        )

    if submitted:

        bmi = calculate_bmi(height, weight)

        score, level, factors = nutrition_risk(
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
            "risk_level": level,
            "factors": factors,
        }

    if st.session_state.screening:

        data = st.session_state.screening

        st.divider()
        st.header("📊 Screening Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("BMI", data["bmi"])

        with c2:
            st.metric("Prototype Risk Score", data["risk_score"])

        with c3:
            st.metric("Screening Level", data["risk_level"])

        if data["age"] >= 18:

            category = adult_bmi_category(data["bmi"])

            if data["bmi"] < 18.5:
                st.markdown(
                    f"""
                    <div class="warning-card">
                        <h3>⚠️ {category}</h3>
                        <p>The BMI value is below the standard adult BMI range.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            elif data["bmi"] < 25:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <h3>✅ {category}</h3>
                        <p>The BMI value falls within the standard adult BMI range.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            elif data["bmi"] < 30:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <h3>ℹ️ {category}</h3>
                        <p>The BMI value is above the standard adult BMI range.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:
                st.markdown(
                    f"""
                    <div class="warning-card">
                        <h3>⚠️ {category}</h3>
                        <p>The BMI value is in a high adult BMI range.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.markdown(
                """
                <div class="warning-card">
                    <h3>🧒 Age-specific interpretation required</h3>
                    <p>
                    Adult BMI categories should not be used for children and adolescents.
                    Appropriate age- and sex-specific growth references are required.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("🌱 Identified Factors")

        if data["factors"]:

            for factor in data["factors"]:
                st.markdown(
                    f"""
                    <div class="n-card">
                        <p>• {factor}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.markdown(
                """
                <div class="result-card">
                    <h3>✓ No basic indicators identified</h3>
                    <p>
                    This does not mean that no nutrition concerns exist.
                    The prototype only evaluates the factors included in this screen.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("💡 General Educational Guidance")

        guidance = [
            "Aim for a varied and balanced eating pattern.",
            "Include suitable protein sources regularly.",
            "Include fruits and vegetables regularly.",
            "Maintain appropriate fluid intake.",
            "Seek professional nutrition or healthcare advice for persistent concerns.",
        ]

        for item in guidance:
            st.write("•", item)

        st.markdown(
            """
            <div class="warning-card">
                <h3>⚠️ Important</h3>
                <p>
                BMI and the prototype risk score are screening/educational
                tools. They are not diagnoses or validated clinical risk scores.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# DIET PLANNER
# =========================================================

elif page == "🍽️ Diet Planner":

    st.header("🍽️ Diet Planner")

    st.write(
        "Generate a practical example day around a general nutrition goal."
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

    if st.button(
        "🍽️ Generate Meal Plan",
        type="primary",
        width="stretch",
    ):

        meals, warnings = build_meal_plan(
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

        st.markdown(
            f"""
            <div class="result-card">
                <h3>✓ Plan Generated</h3>
                <p><b>Goal:</b> {plan["goal"]}</p>
                <p><b>Style:</b> {plan["style"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for meal_name, meal_text in plan["meals"]:

            st.markdown(
                f"""
                <div class="n-card">
                    <h3>🍴 {meal_name}</h3>
                    <p>{meal_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if plan["warnings"]:

            for warning in plan["warnings"]:

                st.markdown(
                    f"""
                    <div class="warning-card">
                        <h3>⚠️ Review</h3>
                        <p>{warning}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown(
            """
            <div class="warning-card">
                <h3>Important</h3>
                <p>
                These are example educational meal ideas, not individualized
                medical diets. Personal needs vary according to age, health,
                activity, allergies and other factors.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# COACH
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

    if st.button(
        "🤖 Ask Nouriva",
        type="primary",
        width="stretch",
    ):

        if question.strip():

            answer = coach_answer(question)

            st.session_state.coach_history.append(
                {
                    "question": question,
                    "answer": answer,
                    "time": datetime.now().strftime("%H:%M"),
                }
            )

    if st.session_state.coach_history:

        st.subheader("Conversation")

        for item in reversed(st.session_state.coach_history[-8:]):

            st.markdown(
                f"""
                <div class="n-card">
                    <p style="color:#8fa097 !important;">
                        {item["time"]}
                    </p>
                    <h3>Q: {item["question"]}</h3>
                    <p><b>🌿 Nouriva:</b> {item["answer"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="warning-card">
            <h3>Educational assistant</h3>
            <p>
            This prototype provides general nutrition education. It does not
            diagnose disease, prescribe treatment or replace professional care.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# EDUCATION
# =========================================================

elif page == "📚 Education":

    st.header("📚 Nutrition Education")

    st.write(
        "Learn the fundamentals through structured lessons, practical guidance and knowledge checks."
    )

    categories = sorted(
        list(set(v["category"] for v in EDUCATION.values()))
    )

    selected_category = st.selectbox(
        "Filter by category",
        ["All"] + categories,
    )

    available_topics = [
        topic
        for topic, data in EDUCATION.items()
        if selected_category == "All"
        or data["category"] == selected_category
    ]

    topic = st.selectbox(
        "Choose a lesson",
        available_topics,
    )

    lesson = EDUCATION[topic]

    st.markdown(
        f"""
        <div class="result-card">
            <h3>📖 {topic}</h3>
            <p><b>Area:</b> {lesson["category"]}</p>
            <p>{lesson["overview"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📌 Key Concepts")

    cols = st.columns(2)

    for i, point in enumerate(lesson["points"]):

        with cols[i % 2]:

            st.markdown(
                f"""
                <div class="n-card">
                    <p>✓ {point}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("🛠️ Practical Takeaways")

    for point in lesson["practical"]:
        st.write("•", point)

    st.divider()

    st.subheader("🧠 Knowledge Check")

    quiz_key = f"answer_{topic}"

    selected = st.radio(
        lesson["question"],
        lesson["options"],
        key=quiz_key,
    )

    if st.button(
        "Check Answer",
        key=f"check_{topic}",
        type="primary",
        width="stretch",
    ):

        selected_index = lesson["options"].index(selected)

        if selected_index == lesson["answer"]:

            st.session_state.quiz_results[topic] = True

            st.markdown(
                """
                <div class="result-card">
                    <h3>✅ Correct</h3>
                    <p>Excellent. You selected the correct answer.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.session_state.quiz_results[topic] = False

            correct = lesson["options"][lesson["answer"]]

            st.markdown(
                f"""
                <div class="warning-card">
                    <h3>❌ Not quite</h3>
                    <p><b>Correct answer:</b> {correct}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if topic in st.session_state.quiz_results:

        score = st.session_state.quiz_results[topic]

        st.metric(
            "Latest Result",
            "1 / 1" if score else "0 / 1",
        )


# =========================================================
# INSIGHTS
# =========================================================

elif page == "📊 Nutrition Insights":

    st.header("📊 Nutrition Insights")

    st.write(
        "Explore screening concepts, prototype indicators and global-goal connections."
    )

    insight = st.selectbox(
        "Choose an insight",
        [
            "Adult BMI Screening",
            "Prototype Risk Factors",
            "Nutrition & SDGs",
            "Your Latest Screening",
        ],
    )

    if insight == "Adult BMI Screening":

        df = pd.DataFrame(
            {
                "Category": [
                    "Below standard",
                    "Standard",
                    "Above standard",
                    "High",
                ],
                "Reference": [18.5, 25, 30, 35],
            }
        )

        st.bar_chart(
            df.set_index("Category")
        )

        st.markdown(
            """
            <div class="result-card">
                <h3>Adult BMI screening</h3>
                <p>
                These are commonly used adult BMI screening thresholds.
                BMI should be interpreted in context and does not by itself
                establish a diagnosis.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif insight == "Prototype Risk Factors":

        df = pd.DataFrame(
            {
                "Factor": [
                    "Low meal frequency",
                    "No listed protein source",
                    "Rare fruit/vegetable intake",
                    "Sometimes difficult food access",
                    "Often difficult food access",
                ],
                "Prototype weight": [1, 1, 1, 1, 2],
            }
        )

        st.bar_chart(
            df.set_index("Factor")
        )

        st.markdown(
            """
            <div class="warning-card">
                <h3>Prototype methodology</h3>
                <p>
                These values are demonstration weights created for the
                Nouriva prototype. They are not a validated clinical score.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif insight == "Nutrition & SDGs":

        sdg_df = pd.DataFrame(
            {
                "SDG": ["SDG 1", "SDG 2", "SDG 3", "SDG 4", "SDG 12"],
                "Nouriva relevance": [2, 5, 5, 4, 3],
            }
        )

        st.bar_chart(
            sdg_df.set_index("SDG")
        )

        for row in sdg_df.itertuples():

            st.markdown(
                f"""
                <div class="n-card">
                    <h3>{row.SDG}</h3>
                    <p>Illustrative Nouriva connection level: {row._2}/5</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        if not st.session_state.screening:

            st.info(
                "Complete Nutrition Scan to see your latest screening summary here."
            )

        else:

            data = st.session_state.screening

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("BMI", data["bmi"])

            with c2:
                st.metric("Risk Score", data["risk_score"])

            with c3:
                st.metric("Risk Level", data["risk_level"])

            st.success(
                "Your latest screening data is available for educational review."
            )


# =========================================================
# GROWTH MONITOR
# =========================================================

elif page == "🧒 Growth Monitor":

    st.header("🧒 Growth Monitor")

    st.write(
        "Educational demonstration of basic growth-monitoring inputs."
    )

    c1, c2 = st.columns(2)

    with c1:

        child_age = st.number_input(
            "Age (years)",
            0.1,
            19.0,
            10.0,
            step=0.1,
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
            step=0.5,
        )

        child_weight = st.number_input(
            "Weight (kg)",
            1.0,
            150.0,
            35.0,
            step=0.5,
        )

    if st.button(
        "🧒 Assess Growth Information",
        type="primary",
        width="stretch",
    ):

        bmi = calculate_bmi(
            child_height,
            child_weight,
        )

        st.session_state.growth_result = {
            "age": child_age,
            "sex": child_sex,
            "height": child_height,
            "weight": child_weight,
            "bmi": bmi,
        }

    if st.session_state.growth_result:

        data = st.session_state.growth_result

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("BMI", data["bmi"])

        with c2:
            st.metric("Age", f'{data["age"]:.1f} years')

        with c3:
            st.metric("Sex", data["sex"])

        st.markdown(
            """
            <div class="warning-card">
                <h3>⚠️ Important growth limitation</h3>
                <p>
                BMI alone cannot determine whether a child or adolescent is
                growing normally. Proper assessment requires validated
                age- and sex-specific growth references and professional
                interpretation.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if data["age"] < 5:

            st.info(
                "For young children, specialized growth standards are particularly important."
            )

        else:

            st.success(
                "Basic growth measurements captured successfully."
            )


# =========================================================
# FOOD SCANNER
# =========================================================

elif page == "📷 Food Scanner":

    st.header("📷 Food Scanner")

    st.write(
        "Upload a food image to demonstrate Nouriva's image-analysis workflow."
    )

    uploaded = st.file_uploader(
        "Choose a food image",
        type=["jpg", "jpeg", "png", "webp"],
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
                width="stretch",
            )

            st.subheader("🔬 Image Analysis")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Width",
                    f"{image.width}px",
                )

            with c2:
                st.metric(
                    "Height",
                    f"{image.height}px",
                )

            with c3:
                st.metric(
                    "File size",
                    f"{len(image_bytes) / 1024:.1f} KB",
                )

            st.markdown(
                """
                <div class="result-card">
                    <h3>✓ Image received successfully</h3>
                    <p>
                    The prototype can receive and inspect an uploaded image.
                    A production food-recognition system would require a trained
                    computer-vision model and validated nutrition database.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as error:

            st.error(
                f"Unable to process this image: {error}"
            )


# =========================================================
# GLOBAL NUTRITION
# =========================================================

elif page == "🌍 Global Nutrition":

    st.header("🌍 Global Nutrition")

    st.write(
        "Explore major nutrition challenges and their relationship to global development."
    )

    topic = st.selectbox(
        "Choose a global topic",
        list(GLOBAL_TOPICS.keys()),
    )

    data = GLOBAL_TOPICS[topic]

    st.markdown(
        f"""
        <div class="result-card">
            <h3>🌎 {topic}</h3>
            <p>{data["description"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Why it matters")

    st.write(data["impact"])

    st.subheader("🎯 SDG Connections")

    cols = st.columns(len(data["sdgs"]))

    for col, sdg in zip(cols, data["sdgs"]):

        with col:

            st.markdown(
                f"""
                <div class="n-card">
                    <h3>{sdg.split(" — ")[0]}</h3>
                    <p>{sdg.split(" — ")[1]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.subheader("🌱 Possible Areas of Action")

    for action in data["actions"]:
        st.write("•", action)

    st.markdown(
        """
        <div class="warning-card">
            <h3>Global perspective</h3>
            <p>
            Nutrition outcomes are shaped by health, food availability,
            economic conditions, education, environment and access to services.
            There is rarely a single solution.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# HEALTH REPORT
# =========================================================

elif page == "📄 Health Report":

    st.header("📄 Health Report")

    if not st.session_state.screening:

        st.markdown(
            """
            <div class="warning-card">
                <h3>⚠️ No screening available</h3>
                <p>
                Complete the Nutrition Scan first. Your screening data will
                automatically become available here.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        data = st.session_state.screening

        report = make_report(data)

        st.markdown(
            """
            <div class="result-card">
                <h3>✓ Report Ready</h3>
                <p>
                Your educational screening summary has been generated.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            "Report Preview",
            report,
            height=500,
        )

        st.download_button(
            "⬇️ Download TXT Report",
            data=report.encode("utf-8"),
            file_name="Nouriva_AI_Report.txt",
            mime="text/plain",
            type="primary",
            width="stretch",
            key="download_txt",
        )

        csv_df = pd.DataFrame(
            {
                "Field": [
                    "Generated",
                    "Age",
                    "Sex",
                    "Height_cm",
                    "Weight_kg",
                    "BMI",
                    "Risk_Score",
                    "Risk_Level",
                    "Meals_Per_Day",
                    "Fruit_Vegetable_Intake",
                    "Food_Access",
                ],
                "Value": [
                    data["date"],
                    data["age"],
                    data["sex"],
                    data["height"],
                    data["weight"],
                    data["bmi"],
                    data["risk_score"],
                    data["risk_level"],
                    data["meals"],
                    data["fruit_veg"],
                    data["food_access"],
                ],
            }
        )

        csv_data = csv_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV Data",
            data=csv_data,
            file_name="Nouriva_AI_Screening_Data.csv",
            mime="text/csv",
            width="stretch",
            key="download_csv",
        )

        st.markdown(
            """
            <div class="warning-card">
                <h3>⚠️ Report disclaimer</h3>
                <p>
                This report is generated by a student-built educational
                prototype. It is not a medical diagnosis and does not replace
                professional nutrition or healthcare assessment.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About Nouriva":

    st.header("ℹ️ About Nouriva AI")

    st.markdown(
        """
        <div class="result-card">
            <h3>🌿 Nouriva AI</h3>
            <p>
            Nouriva AI is a student-built health-technology prototype focused
            on nutrition awareness, preliminary screening, education and
            accessible digital tools.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sections = [
        (
            "🎯 Problem",
            "Nutrition challenges can involve inadequate intake, poor dietary quality, food insecurity, micronutrient deficiencies and other interacting factors.",
        ),
        (
            "💡 Solution",
            "Nouriva combines preliminary screening, nutrition education, meal planning, educational coaching, growth-awareness concepts, image workflow, insights, global nutrition learning and downloadable reports.",
        ),
        (
            "🌍 Global Goals",
            "The prototype connects with SDG 1, SDG 2, SDG 3, SDG 4 and SDG 12.",
        ),
        (
            "👨‍💻 Creator",
            "Muhammad Ahsan Shahzad — BS Human Nutrition & Dietetics Student — Pakistan.",
        ),
    ]

    for title, text in sections:

        st.markdown(
            f"""
            <div class="n-card">
                <h3>{title}</h3>
                <p>{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="warning-card">
            <h3>⚠️ Important</h3>
            <p>
            Nouriva AI is an educational prototype. It does not diagnose
            disease, prescribe treatment or replace qualified healthcare
            professionals.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🌿 <strong>Nouriva AI</strong> • Nutrition • Education • Awareness<br>
        Student Health-Technology Prototype • 2026<br><br>
        Educational prototype — not a diagnostic medical system.
    </div>
    """,
    unsafe_allow_html=True,
)
