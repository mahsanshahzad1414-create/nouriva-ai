import streamlit as st
import pandas as pd
import io
from datetime import datetime
from html import escape

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
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(39,174,96,.10), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(52,152,219,.10), transparent 28%),
            #f5f8f7;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #073b2a 0%, #0b6045 100%);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .hero {
        padding: 36px;
        border-radius: 28px;
        color: white;
        background: linear-gradient(135deg, #073b2a 0%, #087f5b 55%, #12a66f 100%);
        box-shadow: 0 16px 40px rgba(0,0,0,.12);
        margin-bottom: 28px;
    }

    .hero h1 {
        font-size: 46px;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        font-size: 18px;
        margin-top: 8px;
        opacity: .94;
    }

    .section-title {
        font-size: 28px;
        font-weight: 800;
        color: #073b2a;
        margin: 10px 0 18px;
    }

    .tool-card {
        background: white;
        border: 1px solid #dce9e4;
        border-radius: 22px;
        padding: 24px;
        min-height: 190px;
        box-shadow: 0 8px 24px rgba(20,50,40,.07);
        margin-bottom: 18px;
    }

    .tool-icon {
        font-size: 34px;
    }

    .tool-card h3 {
        color: #086044;
        margin: 8px 0;
    }

    .tool-card p {
        color: #667085;
        min-height: 45px;
    }

    .info-card {
        background: white;
        border: 1px solid #dce9e4;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 6px 20px rgba(20,50,40,.06);
        margin: 12px 0;
    }

    .info-card h3 {
        color: #086044;
    }

    .metric-card {
        background: white;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        border: 1px solid #dce9e4;
        box-shadow: 0 6px 18px rgba(20,50,40,.06);
    }

    .metric-number {
        font-size: 30px;
        font-weight: 800;
        color: #087f5b;
    }

    .metric-label {
        color: #667085;
        font-size: 14px;
    }

    .result-card {
        background: white;
        border-radius: 22px;
        padding: 26px;
        border-left: 7px solid #0b8f66;
        box-shadow: 0 8px 25px rgba(20,50,40,.08);
        margin: 18px 0;
    }

    .warning-card {
        background: #fff8e6;
        border: 1px solid #f4d58d;
        border-radius: 18px;
        padding: 18px;
    }

    .footer {
        text-align: center;
        color: #667085;
        padding: 35px 10px 20px;
        margin-top: 40px;
    }

    .stButton > button {
        border-radius: 13px;
        font-weight: 700;
        min-height: 44px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 15px;
        border-radius: 16px;
        border: 1px solid #dce9e4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "🏠 Dashboard",
    "screening": None,
    "diet_plan": None,
    "coach_history": [],
    "quiz_results": {},
    "growth_result": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DATA
# =========================================================

NAVIGATION = [
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

TOOLS = [
    ("🔍", "Nutrition Scan", "BMI, diet information and preliminary nutrition-risk indicators."),
    ("🍽️", "Diet Planner", "Generate practical example meal ideas around a general goal."),
    ("🤖", "Nutrition Coach", "Ask general nutrition education questions."),
    ("📚", "Education", "Explore structured lessons, key points and knowledge checks."),
    ("📊", "Nutrition Insights", "Explore screening concepts, indicators and SDG connections."),
    ("🧒", "Growth Monitor", "Explore age- and sex-specific growth assessment concepts."),
    ("📷", "Food Scanner", "Upload a food image and inspect the prototype workflow."),
    ("🌍", "Global Nutrition", "Explore major nutrition challenges and global development."),
    ("📄", "Health Report", "Generate and download an educational screening summary."),
]

EDUCATION = {
    "Balanced Diet": {
        "overview": "A balanced eating pattern includes a variety of foods that provide energy, protein, vitamins, minerals and other nutrients.",
        "points": [
            "Include a variety of food groups.",
            "Include appropriate protein sources.",
            "Eat fruits and vegetables regularly.",
            "Maintain appropriate fluid intake.",
            "Limit excessive intake of highly processed foods."
        ],
        "question": "Which statement best describes a balanced diet?",
        "options": [
            "Eating only one food group",
            "Eating a variety of foods that provide different nutrients",
            "Avoiding all carbohydrates",
            "Drinking water instead of eating"
        ],
        "answer": 1,
    },
    "Protein": {
        "overview": "Protein is required for tissue maintenance, growth, repair and many biological functions.",
        "points": [
            "Protein is made from amino acids.",
            "Sources include eggs, dairy, pulses, fish and meat.",
            "Nutritional needs vary between individuals.",
            "A varied diet can provide protein."
        ],
        "question": "Which nutrient is especially important for tissue growth and repair?",
        "options": ["Protein", "Water only", "Salt only", "None of these"],
        "answer": 0,
    },
    "Carbohydrates": {
        "overview": "Carbohydrates are an important source of energy and are found in foods such as grains, fruits, vegetables and pulses.",
        "points": [
            "Carbohydrates provide energy.",
            "Whole grains can provide fiber.",
            "Fruits and vegetables contain carbohydrates along with other nutrients.",
            "Food quality and overall dietary pattern matter."
        ],
        "question": "What is one major role of carbohydrates?",
        "options": [
            "Providing energy",
            "Replacing all vitamins",
            "Making bones directly",
            "None"
        ],
        "answer": 0,
    },
    "Fats": {
        "overview": "Dietary fats provide energy and have important structural and physiological roles.",
        "points": [
            "Fats provide concentrated energy.",
            "Some fats are essential nutrients.",
            "Unsaturated fats are found in foods such as nuts, seeds and some oils.",
            "Overall dietary pattern matters more than one food alone."
        ],
        "question": "Which nutrient provides concentrated dietary energy?",
        "options": ["Fat", "Water", "Vitamin C only", "Fiber only"],
        "answer": 0,
    },
    "Micronutrients": {
        "overview": "Micronutrients include vitamins and minerals required in smaller quantities but essential for many body processes.",
        "points": [
            "Iron contributes to hemoglobin formation.",
            "Calcium supports bones and teeth.",
            "Vitamin A has important roles including vision.",
            "Different micronutrients have different functions."
        ],
        "question": "Iron is particularly important for:",
        "options": [
            "Hemoglobin formation",
            "Making water",
            "Replacing all protein",
            "None"
        ],
        "answer": 0,
    },
    "Iron": {
        "overview": "Iron is an essential mineral involved in hemoglobin formation and oxygen transport.",
        "points": [
            "Iron is needed for hemoglobin.",
            "Sources include meat and pulses.",
            "Some plant foods contain iron.",
            "Iron deficiency can require professional assessment."
        ],
        "question": "Iron has an important role in:",
        "options": [
            "Hemoglobin formation",
            "Water production",
            "Replacing carbohydrates",
            "None"
        ],
        "answer": 0,
    },
    "Calcium": {
        "overview": "Calcium supports bones and teeth and also participates in muscle and nerve function.",
        "points": [
            "Dairy foods can provide calcium.",
            "Some fortified foods provide calcium.",
            "Adequate calcium is important throughout life.",
            "Vitamin D also has an important role in calcium metabolism."
        ],
        "question": "Calcium is especially associated with:",
        "options": [
            "Bones and teeth",
            "Only hydration",
            "Only digestion",
            "None"
        ],
        "answer": 0,
    },
    "Hydration": {
        "overview": "Fluids are essential for normal physiological processes. Fluid needs vary according to age, activity, climate and health.",
        "points": [
            "Water is essential for life.",
            "Physical activity can increase fluid losses.",
            "Hot environments can increase fluid requirements.",
            "Some foods also contain water."
        ],
        "question": "Which substance is essential for normal hydration?",
        "options": ["Water", "Salt only", "Protein only", "None"],
        "answer": 0,
    },
    "Fiber": {
        "overview": "Dietary fiber is mainly found in plant foods and contributes to digestive health.",
        "points": [
            "Pulses are useful sources.",
            "Fruits and vegetables provide fiber.",
            "Whole grains can provide fiber.",
            "Adequate fluid intake supports normal bowel function."
        ],
        "question": "Which is a common source of dietary fiber?",
        "options": ["Pulses", "Only salt", "Only water", "None"],
        "answer": 0,
    },
    "Food Safety": {
        "overview": "Food safety practices help reduce contamination and foodborne illness.",
        "points": [
            "Keep hands and surfaces clean.",
            "Separate raw and cooked foods.",
            "Cook food appropriately.",
            "Store food safely."
        ],
        "question": "Which practice helps reduce food contamination?",
        "options": [
            "Separating raw and cooked foods",
            "Leaving cooked food uncovered for days",
            "Using dirty utensils",
            "None"
        ],
        "answer": 0,
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
        "answer": 0,
    },
    "Undernutrition": {
        "overview": "Undernutrition can occur when energy or nutrient intake is inadequate or nutritional needs are not met.",
        "points": [
            "It can affect growth and health.",
            "Children require age-specific assessment.",
            "Causes can include illness and inadequate intake.",
            "Food insecurity can contribute to nutrition problems."
        ],
        "question": "Child growth assessment should consider:",
        "options": [
            "Age- and sex-specific references",
            "Adult BMI categories only",
            "Height alone",
            "None"
        ],
        "answer": 0,
    },
    "Healthy Weight": {
        "overview": "Healthy weight is influenced by nutrition, physical activity, genetics, health and many other factors.",
        "points": [
            "Weight alone does not define health.",
            "BMI can be a screening measure in adults.",
            "Children require age- and sex-specific growth assessment.",
            "Individual needs differ."
        ],
        "question": "BMI in adults is best described as:",
        "options": [
            "A screening measure",
            "A complete diagnosis",
            "A blood test",
            "A food allergy test"
        ],
        "answer": 0,
    },
    "Life Course Nutrition": {
        "overview": "Nutrition needs and assessment approaches change across different stages of life.",
        "points": [
            "Children require growth-focused assessment.",
            "Adults have different nutritional considerations.",
            "Older adults may have changing nutritional needs.",
            "Pregnancy and some health conditions require specialized guidance."
        ],
        "question": "Do nutritional needs remain exactly the same throughout life?",
        "options": ["No", "Yes, always", "Only for children", "Only for athletes"],
        "answer": 0,
    },
}

GLOBAL_TOPICS = {
    "Undernutrition": {
        "description": "Undernutrition includes conditions associated with inadequate energy or nutrient intake.",
        "impact": "It can affect growth, development and health and may be influenced by illness, food access, diet and social conditions.",
        "sdgs": "SDG 2 — Zero Hunger • SDG 3 — Good Health and Well-Being",
    },
    "Food Security": {
        "description": "Food security involves reliable access to sufficient, safe and nutritious food.",
        "impact": "Food insecurity can influence dietary quality, health and vulnerability to nutrition problems.",
        "sdgs": "SDG 2 — Zero Hunger • SDG 1 — No Poverty",
    },
    "Micronutrient Deficiencies": {
        "description": "Micronutrient deficiencies occur when the body does not receive or absorb enough essential vitamins or minerals.",
        "impact": "Deficiencies can affect blood formation, immunity, growth and other biological processes.",
        "sdgs": "SDG 2 — Zero Hunger • SDG 3 — Good Health and Well-Being",
    },
    "Child Malnutrition": {
        "description": "Child nutrition assessment requires appropriate measures of growth and nutritional status.",
        "impact": "Appropriate growth assessment can support early recognition of potential concerns.",
        "sdgs": "SDG 2 — Zero Hunger • SDG 3 — Good Health and Well-Being",
    },
    "Sustainable Nutrition": {
        "description": "Sustainable nutrition considers human health alongside food systems, resources and environmental impacts.",
        "impact": "Food systems influence both human health and environmental sustainability.",
        "sdgs": "SDG 2 — Zero Hunger • SDG 12 — Responsible Consumption and Production",
    },
    "Maternal & Infant Nutrition": {
        "description": "Nutrition during pregnancy and infancy has important implications for growth and development.",
        "impact": "These life stages require appropriate professional guidance and evidence-based assessment.",
        "sdgs": "SDG 2 — Zero Hunger • SDG 3 — Good Health and Well-Being",
    },
}

COACH_KB = {
    "protein": "Protein supports tissue growth, maintenance and repair. Common sources include eggs, dairy, pulses, fish, meat, nuts and seeds.",
    "hydration": "Water and appropriate fluids support normal body functions. Fluid needs vary with age, activity, climate and health.",
    "iron": "Iron contributes to hemoglobin formation and oxygen transport. Sources include meat, pulses and fortified foods.",
    "calcium": "Calcium supports bones and teeth and also has roles in muscle and nerve function.",
    "fiber": "Dietary fiber supports digestive health. Fruits, vegetables, pulses and whole grains are common sources.",
    "vitamin": "Vitamins are micronutrients needed for many biological processes. Different vitamins have different roles.",
    "balanced": "A balanced eating pattern includes a variety of foods and appropriate energy, protein, vitamins, minerals and fluids.",
    "malnutrition": "Malnutrition is a broad term that includes undernutrition and other forms of nutrition imbalance. Assessment requires appropriate context.",
    "bmi": "BMI uses height and weight. In adults it can be a screening measure, but it does not by itself diagnose health or nutritional status.",
    "food safety": "Food safety includes cleaning, separating raw and cooked foods, appropriate cooking and safe storage.",
    "carbohydrate": "Carbohydrates are an important energy source and occur in grains, fruits, vegetables and pulses.",
    "fat": "Dietary fats provide energy and have important structural and physiological functions.",
}


# =========================================================
# HELPERS
# =========================================================

def go_to(page):
    st.session_state.page = page


def calculate_bmi(height_cm, weight_kg):
    if height_cm <= 0:
        return 0.0

    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 1)


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
        factors.append("No protein source listed.")

    if fruit_veg == "Rarely":
        score += 1
        factors.append("Low reported fruit and vegetable intake.")

    if food_access == "Often difficult":
        score += 2
        factors.append("Reported frequent difficulty accessing sufficient food.")
    elif food_access == "Sometimes difficult":
        score += 1
        factors.append("Reported occasional difficulty accessing sufficient food.")

    if score >= 5:
        level = "Higher potential nutrition-risk factors"
    elif score >= 3:
        level = "Several potential nutrition-risk factors"
    elif score >= 1:
        level = "Some potential nutrition-risk factors"
    else:
        level = "Few identified risk factors"

    return score, level, factors


def build_diet_plan(goal, style, vegetarian, allergies):
    allergies_lower = [x.lower() for x in allergies]

    if vegetarian:
        lunch_protein = "dal / beans / chickpeas"
        dinner_protein = "beans / dal"
    else:
        lunch_protein = "chicken / fish"
        dinner_protein = "beans / meat"

    if goal == "Healthy weight gain":
        meals = [
            ("Breakfast", "Eggs + roti/paratha + milk + banana"),
            ("Morning Snack", "Yogurt + roasted chickpeas or nuts/seeds"),
            ("Lunch", f"Rice/roti + dal + {lunch_protein} + vegetables"),
            ("Evening Snack", "Milk + banana or seasonal fruit"),
            ("Dinner", f"Roti + {dinner_protein} + vegetables + yogurt"),
        ]

    elif goal == "Healthy weight management":
        meals = [
            ("Breakfast", "Eggs or yogurt + whole-grain roti + fruit"),
            ("Morning Snack", "Fruit + unsweetened yogurt"),
            ("Lunch", f"Roti/rice + {lunch_protein} + vegetables"),
            ("Evening Snack", "Fruit + water or milk"),
            ("Dinner", f"Roti + {dinner_protein} + vegetables"),
        ]

    elif goal == "Athletic nutrition":
        meals = [
            ("Breakfast", "Eggs + oats/roti + milk + fruit"),
            ("Pre/Post Activity", "Banana + yogurt or milk"),
            ("Lunch", f"Rice/roti + {lunch_protein} + vegetables"),
            ("Snack", "Fruit + yogurt + nuts/seeds"),
            ("Dinner", f"Roti/rice + {dinner_protein} + vegetables"),
        ]

    else:
        meals = [
            ("Breakfast", "Eggs/yogurt + roti + fruit"),
            ("Snack", "Fruit + yogurt"),
            ("Lunch", f"Rice/roti + {lunch_protein} + vegetables"),
            ("Snack", "Milk + fruit"),
            ("Dinner", f"Roti + {dinner_protein} + vegetables"),
        ]

    if style == "Budget-friendly":
        meals = [
            (
                name,
                text.replace("nuts/seeds", "roasted chickpeas")
                .replace("chicken / fish", "dal / beans")
                .replace("fish / chicken", "dal / beans"),
            )
            for name, text in meals
        ]

    warnings = []

    for name, text in meals:
        text_lower = text.lower()

        for allergy in allergies_lower:
            if allergy and allergy in text_lower:
                warnings.append(
                    f"{name}: the example contains or may contain your selected food. Review it before use."
                )

    return meals, list(dict.fromkeys(warnings))


def coach_answer(question):
    q = question.lower().strip()

    for keyword, answer in COACH_KB.items():
        if keyword in q:
            return answer

    return (
        "I can provide general nutrition education about protein, carbohydrates, "
        "fats, hydration, iron, calcium, vitamins, fiber, balanced diets, BMI, "
        "malnutrition and food safety. For personal medical concerns, consult a "
        "qualified healthcare or nutrition professional."
    )


def create_report(data):
    factors = (
        "\n".join(f"- {x}" for x in data["factors"])
        if data["factors"]
        else "- No basic risk indicators identified by this prototype."
    )

    protein = ", ".join(data["protein"]) if data["protein"] else "None listed"

    bmi_interpretation = (
        adult_bmi_category(data["bmi"])
        if data["age"] >= 18
        else "Age-specific interpretation required"
    )

    return f"""
NOURIVA AI
Nutrition Screening & Education Report
========================================

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
BMI interpretation: {bmi_interpretation}

Reported meals per day: {data["meals"]}
Protein sources: {protein}
Fruit & vegetable intake: {data["fruit_veg"]}
Food access: {data["food_access"]}

PRELIMINARY SCREENING
---------------------
Prototype score: {data["risk_score"]}
Result: {data["risk_level"]}

Identified factors:
{factors}

GENERAL EDUCATIONAL GUIDANCE
----------------------------
- Aim for a varied and balanced eating pattern.
- Include suitable protein sources regularly.
- Include fruits and vegetables regularly.
- Maintain appropriate fluid intake.
- Seek professional assessment for health or nutrition concerns.

IMPORTANT
---------
Nouriva AI is a student-built educational prototype.
This report is not a medical diagnosis and does not replace
professional healthcare or nutrition assessment.

Nouriva AI • Nutrition • Education • Awareness
Student Health-Technology Prototype • 2026
"""


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("## 🌿 Nouriva AI")
    st.caption("Nutrition • Education • Awareness")

    st.divider()

    selected = st.radio(
        "Navigation",
        NAVIGATION,
        index=NAVIGATION.index(st.session_state.page),
    )

    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

    st.divider()

    st.markdown("### Nouriva")
    st.caption("Student Health-Technology Prototype")
    st.caption("2026")


page = st.session_state.page


# =========================================================
# GLOBAL HEADER
# =========================================================

st.markdown(
    """
    <div class="hero">
        <h1>🌿 Nouriva AI</h1>
        <p><b>AI-Assisted Nutrition Screening & Education</b></p>
        <p>
        Nutrition awareness, preliminary screening, education,
        meal planning and global nutrition learning in one platform.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown('<div class="section-title">Your Nutrition Hub</div>', unsafe_allow_html=True)

    st.write(
        "Choose a tool below. Each module opens directly and provides an interactive workflow."
    )

    for start in range(0, len(TOOLS), 3):
        row = TOOLS[start:start + 3]
        cols = st.columns(3)

        for col, (icon, title, description) in zip(cols, row):
            with col:
                st.markdown(
                    f"""
                    <div class="tool-card">
                        <div class="tool-icon">{icon}</div>
                        <h3>{title}</h3>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Open {title}",
                    key=f"open_{title}",
                    use_container_width=True,
                ):
                    mapping = {
                        "Nutrition Scan": "🔍 Nutrition Scan",
                        "Diet Planner": "🍽️ Diet Planner",
                        "Nutrition Coach": "🤖 Nutrition Coach",
                        "Education": "📚 Education",
                        "Nutrition Insights": "📊 Nutrition Insights",
                        "Growth Monitor": "🧒 Growth Monitor",
                        "Food Scanner": "📷 Food Scanner",
                        "Global Nutrition": "🌍 Global Nutrition",
                        "Health Report": "📄 Health Report",
                    }

                    st.session_state.page = mapping[title]
                    st.rerun()

    st.divider()

    st.markdown("### Nouriva at a Glance")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Core Tools", "9")

    with c2:
        st.metric("Education Areas", f"{len(EDUCATION)}+")

    with c3:
        st.metric("Global Topics", len(GLOBAL_TOPICS))

    with c4:
        st.metric("Status", "Working Prototype")

    st.markdown(
        """
        <div class="info-card">
            <h3>🌱 Our Purpose</h3>
            <p>
            Nouriva AI demonstrates how accessible digital tools can support
            nutrition awareness, preliminary screening and nutrition education.
            It is a student-built prototype rather than a diagnostic medical system.
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
        "Enter basic information to calculate BMI and explore preliminary "
        "nutrition-related indicators."
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

        with c2:
            height = st.number_input(
                "Height (cm)",
                min_value=30.0,
                max_value=250.0,
                value=170.0,
                step=0.1,
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=1.0,
                max_value=300.0,
                value=55.0,
                step=0.1,
            )

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
            "🔍 Analyze My Nutrition",
            use_container_width=True,
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
        st.subheader("📊 Screening Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("BMI", data["bmi"])

        with c2:
            st.metric("Risk Score", data["risk_score"])

        with c3:
            st.metric("Screening Result", data["risk_level"])

        if data["age"] >= 18:

            category = adult_bmi_category(data["bmi"])

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
                "For people under 18, adult BMI categories should not be used. "
                "Age- and sex-specific growth references are required."
            )

        st.subheader("🌱 Identified Factors")

        if data["factors"]:
            for factor in data["factors"]:
                st.write(f"• {factor}")
        else:
            st.success(
                "No basic risk indicators were identified by this prototype."
            )

        st.subheader("💡 General Educational Guidance")

        guidance = [
            "Aim for a varied and balanced eating pattern.",
            "Include appropriate protein sources regularly.",
            "Include fruits and vegetables regularly.",
            "Maintain appropriate fluid intake.",
            "Seek professional advice for persistent health or nutrition concerns.",
        ]

        for item in guidance:
            st.write(f"• {item}")

        st.caption(
            "BMI and the prototype risk score are screening/educational tools, "
            "not diagnoses or validated clinical risk scores."
        )


# =========================================================
# DIET PLANNER
# =========================================================

elif page == "🍽️ Diet Planner":

    st.header("🍽️ Diet Planner")

    st.write(
        "Generate an example day of meals around a general nutrition goal."
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

        vegetarian = st.checkbox(
            "Vegetarian"
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
            f"Plan generated • Goal: {plan['goal']} • Style: {plan['style']}"
        )

        for meal_name, meal_text in plan["meals"]:

            st.markdown(
                f"""
                <div class="info-card">
                    <h3>🍽️ {escape(meal_name)}</h3>
                    <p>{escape(meal_text)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if plan["warnings"]:

            st.subheader("⚠️ Review Flags")

            for warning in plan["warnings"]:
                st.warning(warning)

        st.info(
            "These are example educational meal ideas, not individualized medical diets. "
            "Personal dietary needs, allergies, health conditions and energy requirements vary."
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

    if st.button(
        "🤖 Ask Nouriva",
        use_container_width=True,
    ):

        if question.strip():

            answer = coach_answer(question)

            st.session_state.coach_history.append(
                {
                    "question": question.strip(),
                    "answer": answer,
                }
            )

        else:
            st.warning("Please enter a nutrition question first.")

    if st.session_state.coach_history:

        st.subheader("Conversation")

        for item in reversed(st.session_state.coach_history[-8:]):

            st.markdown(
                f"""
                <div class="result-card">
                    <b>Question</b>
                    <p>{escape(item["question"])}</p>
                    <b>🌿 Nouriva Coach</b>
                    <p>{escape(item["answer"])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption(
        "Nouriva Coach is an educational prototype and does not provide diagnosis, "
        "prescriptions or individualized medical treatment."
    )


# =========================================================
# EDUCATION
# =========================================================

elif page == "📚 Education":

    st.header("📚 Nutrition Education")

    st.write(
        "Learn through structured lessons, key points and knowledge checks."
    )

    topic = st.selectbox(
        "Choose a learning topic",
        list(EDUCATION.keys()),
    )

    lesson = EDUCATION[topic]

    st.markdown(
        f"""
        <div class="info-card">
            <h3>📖 {escape(topic)}</h3>
            <p>{escape(lesson["overview"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📌 Key Learning Points")

    for point in lesson["points"]:
        st.write(f"• {point}")

    st.divider()

    st.subheader("🧠 Knowledge Check")

    answer = st.radio(
        lesson["question"],
        lesson["options"],
        key=f"answer_{topic}",
    )

    if st.button(
        "Check Answer",
        use_container_width=True,
        key=f"check_{topic}",
    ):

        selected_index = lesson["options"].index(answer)

        if selected_index == lesson["answer"]:
            st.session_state.quiz_results[topic] = True
            st.success("✅ Correct! Excellent.")

        else:
            st.session_state.quiz_results[topic] = False

            correct = lesson["options"][lesson["answer"]]

            st.error(
                f"❌ Not quite. Correct answer: {correct}"
            )

    if topic in st.session_state.quiz_results:

        result = st.session_state.quiz_results[topic]

        st.metric(
            "Latest Result",
            "1 / 1" if result else "0 / 1",
        )


# =========================================================
# INSIGHTS
# =========================================================

elif page == "📊 Nutrition Insights":

    st.header("📊 Nutrition Insights")

    st.write(
        "Explore example indicators used by Nouriva's educational prototype."
    )

    indicator = st.selectbox(
        "Choose an insight",
        [
            "Adult BMI Screening Concepts",
            "Prototype Risk Factors",
            "Nouriva SDG Connections",
            "Nutrition Education Coverage",
        ],
    )

    if indicator == "Adult BMI Screening Concepts":

        df = pd.DataFrame(
            {
                "Category": [
                    "Below standard",
                    "Standard",
                    "Above standard",
                    "High",
                ],
                "Reference": [
                    18.5,
                    25,
                    30,
                    35,
                ],
            }
        )

        st.bar_chart(
            df.set_index("Category")
        )

        st.info(
            "These are adult BMI screening thresholds. BMI should not be interpreted "
            "as a complete diagnosis of health or nutritional status."
        )

    elif indicator == "Prototype Risk Factors":

        df = pd.DataFrame(
            {
                "Factor": [
                    "Low meals",
                    "No protein listed",
                    "Rare fruit/vegetables",
                    "Food access difficulty",
                    "BMI screening flag",
                ],
                "Prototype Weight": [
                    1,
                    1,
                    1,
                    2,
                    2,
                ],
            }
        )

        st.bar_chart(
            df.set_index("Factor")
        )

        st.warning(
            "These are Nouriva prototype weights created for demonstration. "
            "They are not a validated clinical scoring system."
        )

    elif indicator == "Nouriva SDG Connections":

        df = pd.DataFrame(
            {
                "SDG": [
                    "SDG 1",
                    "SDG 2",
                    "SDG 3",
                    "SDG 4",
                    "SDG 12",
                ],
                "Project Connection": [
                    2,
                    5,
                    5,
                    5,
                    3,
                ],
            }
        )

        st.bar_chart(
            df.set_index("SDG")
        )

        st.success(
            "Nouriva primarily connects nutrition awareness with Zero Hunger, "
            "Good Health and Well-Being and Quality Education."
        )

    else:

        education_counts = pd.DataFrame(
            {
                "Area": list(EDUCATION.keys()),
                "Lesson": [1] * len(EDUCATION),
            }
        )

        st.bar_chart(
            education_counts.set_index("Area")
        )

        st.success(
            f"Nouriva currently contains {len(EDUCATION)} structured education topics."
        )


# =========================================================
# GROWTH MONITOR
# =========================================================

elif page == "🧒 Growth Monitor":

    st.header("🧒 Growth Monitor")

    st.write(
        "Educational demonstration of basic growth measurements."
    )

    st.warning(
        "Child and adolescent growth must be interpreted using validated "
        "age- and sex-specific growth references. BMI alone is not sufficient."
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
            key="growth_sex_final",
        )

    with c2:

        child_height = st.number_input(
            "Height (cm)",
            min_value=30.0,
            max_value=220.0,
            value=140.0,
            step=0.1,
        )

        child_weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=150.0,
            value=35.0,
            step=0.1,
        )

    if st.button(
        "🧒 Assess Growth Information",
        use_container_width=True,
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

        result = st.session_state.growth_result

        st.divider()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("BMI", result["bmi"])

        with c2:
            st.metric("Age", f'{result["age"]:g} years')

        with c3:
            st.metric("Height", f'{result["height"]:g} cm')

        st.info(
            "The measurements have been captured successfully. "
            "A production system would compare these values with validated "
            "age- and sex-specific growth references."
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
        "Upload food image",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded:

        st.image(
            uploaded,
            caption="Uploaded food image",
            use_container_width=True,
        )

        try:

            from PIL import Image

            image_bytes = uploaded.getvalue()
            image = Image.open(io.BytesIO(image_bytes))

            width, height = image.size

            st.subheader("🔬 Image Analysis")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Width", f"{width}px")

            with c2:
                st.metric("Height", f"{height}px")

            with c3:
                st.metric(
                    "File Size",
                    f"{len(image_bytes) / 1024:.1f} KB",
                )

            st.success(
                "✅ Image successfully received and processed."
            )

            st.info(
                "This version demonstrates the image-processing workflow. "
                "A real food-recognition model would be required before claiming "
                "automatic food identification, portion estimation or nutrient calculation."
            )

        except Exception as error:
            st.error(
                f"Could not process this image: {error}"
            )

    else:

        st.info(
            "Upload a JPG, JPEG, PNG or WEBP image to begin."
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
        "Choose a global nutrition topic",
        list(GLOBAL_TOPICS.keys()),
    )

    data = GLOBAL_TOPICS[topic]

    st.markdown(
        f"""
        <div class="info-card">
            <h3>🌎 {escape(topic)}</h3>
            <p>{escape(data["description"])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Why This Matters")

    st.write(data["impact"])

    st.subheader("🎯 SDG Connection")

    st.success(data["sdgs"])

    st.subheader("🌱 Nouriva Perspective")

    st.write(
        "Nutrition outcomes are influenced by health, food availability, "
        "affordability, education, environment, food systems and access to services. "
        "Digital education is one possible supporting tool within broader solutions."
    )


# =========================================================
# HEALTH REPORT
# =========================================================

elif page == "📄 Health Report":

    st.header("📄 Health Report")

    if not st.session_state.screening:

        st.warning(
            "Complete the Nutrition Scan first."
        )

        if st.button(
            "🔍 Go to Nutrition Scan",
            use_container_width=True,
        ):
            st.session_state.page = "🔍 Nutrition Scan"
            st.rerun()

    else:

        data = st.session_state.screening

        st.success(
            "✅ Screening data found. Your educational report is ready."
        )

        report = create_report(data)

        st.text_area(
            "Report Preview",
            report,
            height=480,
        )

        st.download_button(
            "⬇️ Download Nouriva Health Report",
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
        <div class="info-card">
            <h3>🌿 What is Nouriva AI?</h3>
            <p>
            Nouriva AI is a student-built health-technology prototype focused
            on nutrition awareness, preliminary screening, education and
            accessible digital tools.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🎯 Project Focus")

    st.write(
        "Nouriva brings together nutrition screening concepts, meal planning, "
        "education, nutrition coaching, growth-awareness concepts, food-image "
        "workflow and global nutrition information."
    )

    st.subheader("💡 Why Nouriva?")

    st.write(
        "Nutrition challenges are influenced by diet, health, food access, "
        "education, economic conditions, environment and many other factors. "
        "Nouriva demonstrates how a digital platform could make nutrition "
        "information more accessible."
    )

    st.subheader("🌍 Sustainable Development Goals")

    sdgs = [
        "SDG 1 — No Poverty",
        "SDG 2 — Zero Hunger",
        "SDG 3 — Good Health and Well-Being",
        "SDG 4 — Quality Education",
        "SDG 12 — Responsible Consumption and Production",
    ]

    for sdg in sdgs:
        st.write(f"• {sdg}")

    st.subheader("👨‍💻 Creator")

    st.write(
        "**Muhammad Ahsan Shahzad**  \n"
        "BS Human Nutrition & Dietetics Student  \n"
        "Pakistan"
    )

    st.subheader("⚠️ Important Limitation")

    st.warning(
        "Nouriva AI is an educational student prototype. "
        "It does not diagnose disease, prescribe treatment or replace "
        "qualified healthcare or nutrition professionals."
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
