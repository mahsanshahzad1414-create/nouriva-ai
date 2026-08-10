import streamlit as st
import math
from datetime import datetime

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(16,185,129,0.10), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(59,130,246,0.08), transparent 25%),
        #f7faf9;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #073b32 0%, #0b594b 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-brand {
    text-align: center;
    padding: 12px 5px 25px 5px;
}

.sidebar-logo {
    font-size: 42px;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 800;
}

.sidebar-sub {
    font-size: 12px;
    opacity: 0.75;
}

/* Main */

.main-title {
    font-size: 44px;
    font-weight: 800;
    line-height: 1.1;
    color: #073b32;
}

.hero {
    padding: 35px;
    border-radius: 28px;
    background: linear-gradient(135deg, #073b32, #087f5b);
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 15px 40px rgba(7,59,50,0.16);
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    color: rgba(255,255,255,0.88);
    font-size: 17px;
}

/* Cards */

.tool-card {
    background: white;
    border-radius: 22px;
    padding: 25px;
    min-height: 190px;
    border: 1px solid #e5ece9;
    box-shadow: 0 8px 25px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.tool-icon {
    font-size: 34px;
}

.tool-title {
    font-size: 20px;
    font-weight: 800;
    color: #073b32;
    margin-top: 8px;
}

.tool-text {
    color: #5c6b66;
    font-size: 14px;
    min-height: 45px;
}

/* Section */

.section-title {
    color: #073b32;
    font-size: 28px;
    font-weight: 800;
    margin-top: 25px;
}

.section-subtitle {
    color: #66756f;
}

/* Metrics */

.metric-card {
    background: white;
    border-radius: 18px;
    padding: 22px;
    border: 1px solid #e4ebe8;
    text-align: center;
}

.metric-number {
    font-size: 30px;
    font-weight: 800;
    color: #087f5b;
}

.metric-label {
    color: #697873;
    font-size: 13px;
}

/* Information */

.info-box {
    background: #eef9f5;
    border-left: 5px solid #087f5b;
    border-radius: 12px;
    padding: 18px;
    margin: 15px 0;
}

.warning-box {
    background: #fff8e6;
    border-left: 5px solid #e9a23b;
    border-radius: 12px;
    padding: 18px;
    margin: 15px 0;
}

/* Footer */

.footer {
    text-align: center;
    padding: 35px 10px 15px 10px;
    color: #71817b;
    font-size: 13px;
}

button[kind="secondary"] {
    border-radius: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def go(page):
    st.session_state.page = page


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🌿</div>
        <div class="sidebar-title">Nouriva AI</div>
        <div class="sidebar-sub">
            Nutrition • Education • Awareness
        </div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠 Dashboard": "Dashboard",
        "🔍 Nutrition Scan": "Nutrition Scan",
        "🍽️ Diet Planner": "Diet Planner",
        "🤖 Nutrition Coach": "Nutrition Coach",
        "📚 Education": "Education",
        "📊 Insights": "Insights",
        "🧒 Growth Monitor": "Growth Monitor",
        "📷 Food Scanner": "Food Scanner",
        "🌍 Global Nutrition": "Global Nutrition",
        "📄 Health Report": "Health Report",
        "ℹ️ About": "About"
    }

    for label, page_name in pages.items():
        if st.button(
            label,
            key="nav_" + page_name,
            use_container_width=True
        ):
            go(page_name)
            st.rerun()

    st.divider()

    st.caption("Student Health-Technology Prototype")
    st.caption("Nouriva AI • 2026")


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <h1>🌿 Nouriva AI</h1>
    <p>
        AI-Assisted Nutrition Screening & Education Platform
    </p>
    <p>
        Explore nutrition screening, food education, meal planning,
        growth awareness and global nutrition information in one place.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# DASHBOARD
# ============================================================

if st.session_state.page == "Dashboard":

    st.markdown(
        '<div class="section-title">Your Nutrition Hub</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose a tool below to explore Nouriva AI."
    )

    tools = [
        (
            "🔍",
            "Nutrition Scan",
            "Calculate BMI and explore preliminary nutrition-risk indicators.",
            "Nutrition Scan"
        ),
        (
            "🍽️",
            "Diet Planner",
            "Build an example day of balanced meals around a general goal.",
            "Diet Planner"
        ),
        (
            "🤖",
            "Nutrition Coach",
            "Explore general nutrition questions using Nouriva's educational assistant.",
            "Nutrition Coach"
        ),
        (
            "📚",
            "Education",
            "Learn about macronutrients, micronutrients, hydration, food safety and more.",
            "Education"
        ),
        (
            "📊",
            "Nutrition Insights",
            "Explore nutrition indicators, screening concepts and SDG connections.",
            "Insights"
        ),
        (
            "🧒",
            "Growth Monitor",
            "Explore the principles of age- and sex-specific growth assessment.",
            "Growth Monitor"
        ),
        (
            "📷",
            "Food Scanner",
            "Upload a food image and explore a prototype food-analysis workflow.",
            "Food Scanner"
        ),
        (
            "🌍",
            "Global Nutrition",
            "Learn about undernutrition, food security and global nutrition challenges.",
            "Global Nutrition"
        ),
        (
            "📄",
            "Health Report",
            "Generate an educational screening summary for download.",
            "Health Report"
        )
    ]

    for row in range(0, len(tools), 3):

        cols = st.columns(3)

        for col, tool in zip(cols, tools[row:row + 3]):

            icon, title, description, destination = tool

            with col:

                st.markdown(
                    f"""
                    <div class="tool-card">
                        <div class="tool-icon">{icon}</div>
                        <div class="tool-title">{title}</div>
                        <div class="tool-text">{description}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Open {title}",
                    key="open_" + destination,
                    use_container_width=True
                ):
                    go(destination)
                    st.rerun()

    st.markdown(
        '<div class="section-title">Nouriva at a Glance</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            '<div class="metric-card"><div class="metric-number">9</div>'
            '<div class="metric-label">Core Tools</div></div>',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            '<div class="metric-card"><div class="metric-number">10+</div>'
            '<div class="metric-label">Education Areas</div></div>',
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            '<div class="metric-card"><div class="metric-number">5</div>'
            '<div class="metric-label">SDG Connections</div></div>',
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            '<div class="metric-card"><div class="metric-number">MVP+</div>'
            '<div class="metric-label">Working Prototype</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="info-box"><b>🌱 Our purpose</b><br>'
        'Nouriva AI demonstrates how accessible digital tools can support '
        'nutrition awareness, preliminary screening and education. '
        'It is designed as a student-built prototype, not a diagnostic system.'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# NUTRITION SCAN
# ============================================================

elif st.session_state.page == "Nutrition Scan":

    st.markdown(
        '<div class="section-title">🔍 Nutrition Scan</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Enter basic information to calculate BMI and review "
        "simple nutrition-risk indicators."
    )

    st.markdown(
        '<div class="warning-box"><b>Important:</b> BMI is a screening '
        'measure, not a diagnosis. Adult BMI categories are not appropriate '
        'for interpreting children and adolescents.</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        age = st.number_input(
            "Age (years)",
            min_value=1,
            max_value=120,
            value=20
        )

        sex = st.selectbox(
            "Sex",
            ["Male", "Female"]
        )

        height = st.number_input(
            "Height (cm)",
            min_value=30.0,
            max_value=250.0,
            value=170.0,
            step=0.1
        )

    with c2:

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=55.0,
            step=0.1
        )

        meals = st.selectbox(
            "Typical meals per day",
            [1, 2, 3, 4, 5]
        )

        fruit_veg = st.selectbox(
            "Fruit & vegetable intake",
            ["Rarely", "Sometimes", "Daily"]
        )

    protein = st.multiselect(
        "Common protein sources",
        [
            "Eggs",
            "Milk / Dairy",
            "Pulses / Lentils",
            "Fish",
            "Chicken / Meat",
            "Nuts / Seeds"
        ]
    )

    food_access = st.selectbox(
        "Access to sufficient food",
        [
            "Usually sufficient",
            "Sometimes difficult",
            "Often difficult"
        ]
    )

    if st.button(
        "🔍 Analyze Nutrition",
        type="primary",
        use_container_width=True
    ):

        height_m = height / 100
        bmi = weight / (height_m ** 2)
        bmi = round(bmi, 1)

        st.divider()

        st.markdown(
            '<div class="section-title">Screening Results</div>',
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)

        with a:
            st.metric("BMI", bmi)

        with b:
            st.metric("Meals / day", meals)

        with c:
            st.metric("Protein sources", len(protein))

        if age >= 18:

            if bmi < 18.5:
                st.warning(
                    "BMI is below the standard adult reference range."
                )

            elif bmi < 25:
                st.success(
                    "BMI falls within the standard adult reference range."
                )

            elif bmi < 30:
                st.info(
                    "BMI is above the standard adult reference range."
                )

            else:
                st.warning(
                    "BMI is in a high adult BMI range."
                )

        else:

            st.info(
                "For people under 18, BMI must be interpreted using "
                "age- and sex-specific growth references. This prototype "
                "does not diagnose pediatric nutritional status."
            )

        risk = 0
        factors = []

        if age >= 18 and bmi < 18.5:
            risk += 2
            factors.append("BMI below adult reference range")

        if meals <= 2:
            risk += 1
            factors.append("Low reported meal frequency")

        if len(protein) == 0:
            risk += 1
            factors.append("No listed protein source")

        if fruit_veg == "Rarely":
            risk += 1
            factors.append("Low reported fruit/vegetable intake")

        if food_access == "Often difficult":
            risk += 2
            factors.append("Food access reported as often difficult")

        elif food_access == "Sometimes difficult":
            risk += 1
            factors.append("Food access sometimes difficult")

        st.subheader("🌱 Preliminary Risk Indicators")

        if risk >= 4:
            st.warning(
                "Several potential nutrition-risk factors were identified."
            )

        elif risk >= 2:
            st.info(
                "Some potential nutrition-risk factors were identified."
            )

        else:
            st.success(
                "Few risk indicators were identified in this basic screen."
            )

        if factors:

            st.write("Factors contributing to this screening result:")

            for factor in factors:
                st.write("•", factor)

        st.subheader("💡 General Guidance")

        guidance = [
            "Aim for variety across major food groups.",
            "Include appropriate protein sources regularly.",
            "Include fruits and vegetables as part of a varied diet.",
            "Maintain adequate fluid intake.",
            "Seek professional assessment when persistent nutrition or health concerns exist."
        ]

        for item in guidance:
            st.write("•", item)


# ============================================================
# DIET PLANNER
# ============================================================

elif st.session_state.page == "Diet Planner":

    st.markdown(
        '<div class="section-title">🍽️ Diet Planner</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Create a simple educational example meal pattern."
    )

    goal = st.selectbox(
        "General goal",
        [
            "Balanced Nutrition",
            "Healthy Weight Gain",
            "Healthy Weight Management",
            "Active Lifestyle"
        ]
    )

    style = st.selectbox(
        "Food style",
        [
            "Flexible",
            "South Asian-inspired",
            "Vegetarian"
        ]
    )

    if goal == "Healthy Weight Gain":

        meals_plan = [
            ("Breakfast", "Eggs + whole-grain roti/oats + milk + fruit"),
            ("Morning Snack", "Yogurt + nuts/seeds"),
            ("Lunch", "Rice/roti + lentils or chicken + vegetables"),
            ("Afternoon Snack", "Milk/yogurt + banana"),
            ("Dinner", "Roti/rice + beans/meat + vegetables")
        ]

    elif goal == "Active Lifestyle":

        meals_plan = [
            ("Breakfast", "Eggs + oats/roti + milk + fruit"),
            ("Snack", "Yogurt + fruit"),
            ("Lunch", "Rice/roti + protein source + vegetables"),
            ("Pre/Post Activity", "Fruit + suitable carbohydrate/protein food"),
            ("Dinner", "Balanced meal with protein + vegetables + grains")
        ]

    elif goal == "Healthy Weight Management":

        meals_plan = [
            ("Breakfast", "Eggs + whole grain + fruit"),
            ("Snack", "Fruit or unsweetened yogurt"),
            ("Lunch", "Vegetables + lentils/chicken + moderate grain portion"),
            ("Snack", "Fruit + small serving of nuts"),
            ("Dinner", "Vegetables + protein + whole grain")
        ]

    else:

        meals_plan = [
            ("Breakfast", "Eggs + roti/oats + fruit"),
            ("Snack", "Fruit + yogurt"),
            ("Lunch", "Lentils/chicken + rice/roti + vegetables"),
            ("Snack", "Milk + fruit"),
            ("Dinner", "Protein source + vegetables + grain")
        ]

    st.subheader("Example Day")

    for meal, food in meals_plan:

        st.markdown(
            f"""
            <div class="tool-card" style="min-height:auto;">
                <b>{meal}</b><br>
                {food}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Meal examples are educational and are not individualized medical diets."
    )


# ============================================================
# NUTRITION COACH
# ============================================================

elif st.session_state.page == "Nutrition Coach":

    st.markdown(
        '<div class="section-title">🤖 Nouriva Nutrition Coach</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask a general nutrition education question."
    )

    question = st.text_input(
        "Your question",
        placeholder="Example: Why is protein important?"
    )

    if question:

        q = question.lower()

        if "protein" in q:

            answer = (
                "Protein is needed for growth, tissue maintenance and repair, "
                "and many biological processes. Common sources include eggs, "
                "dairy, pulses, fish, meat, nuts and seeds."
            )

        elif "water" in q or "hydration" in q:

            answer = (
                "Water is essential for normal body functions including "
                "temperature regulation, circulation and many chemical "
                "processes. Fluid needs vary with age, activity, climate "
                "and health status."
            )

        elif "iron" in q:

            answer = (
                "Iron is an essential mineral involved in oxygen transport "
                "and other physiological functions. Food sources include "
                "meat, legumes and some fortified foods. Iron concerns "
                "should be assessed by a qualified healthcare professional."
            )

        elif "vitamin" in q:

            answer = (
                "Vitamins are micronutrients required for many body functions. "
                "Different vitamins have different roles, and a varied diet "
                "helps provide many essential micronutrients."
            )

        elif "bmi" in q:

            answer = (
                "BMI is calculated from weight and height. It is a screening "
                "measure and should be interpreted alongside other information. "
                "It is not a diagnosis and adult BMI categories should not be "
                "used for children."
            )

        elif "breakfast" in q:

            answer = (
                "A balanced breakfast can combine a protein source, a "
                "carbohydrate-rich food and fruit or another nutrient-rich food."
            )

        else:

            answer = (
                "Nouriva's current prototype provides general nutrition "
                "education rather than medical diagnosis. Try asking about "
                "protein, hydration, iron, vitamins, BMI or balanced meals."
            )

        st.success(answer)

    st.subheader("Popular Questions")

    questions = [
        "Why is protein important?",
        "What is BMI?",
        "Why is hydration important?",
        "What are good sources of iron?",
        "What makes a balanced meal?"
    ]

    for item in questions:
        st.write("•", item)


# ============================================================
# EDUCATION
# ============================================================

elif st.session_state.page == "Education":

    st.markdown(
        '<div class="section-title">📚 Nutrition Education Centre</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore structured nutrition learning topics."
    )

    topics = {
        "Balanced Diet": {
            "overview":
                "A balanced diet provides a variety of foods and nutrients "
                "in amounts appropriate for individual needs.",
            "key": [
                "Include a variety of foods.",
                "Include protein-rich foods.",
                "Include fruits and vegetables.",
                "Choose suitable sources of carbohydrates and fats.",
                "Maintain adequate hydration."
            ]
        },

        "Protein": {
            "overview":
                "Protein contributes to tissue growth, maintenance and repair "
                "and supports many biological functions.",
            "key": [
                "Protein is made of amino acids.",
                "Sources include animal and plant foods.",
                "Needs vary by age, body size and activity.",
                "Variety can help provide different nutrients."
            ]
        },

        "Carbohydrates": {
            "overview":
                "Carbohydrates are an important source of energy and occur "
                "in foods such as grains, fruits, vegetables and legumes.",
            "key": [
                "Whole grains provide carbohydrates and other nutrients.",
                "Fruits and vegetables contain carbohydrates plus micronutrients.",
                "Energy needs vary between individuals."
            ]
        },

        "Fats": {
            "overview":
                "Dietary fats provide energy and support cell structure and "
                "the absorption of fat-soluble vitamins.",
            "key": [
                "Fats are energy dense.",
                "Different fats have different physiological effects.",
                "Nuts, seeds, fish and plant oils provide useful sources."
            ]
        },

        "Vitamins": {
            "overview":
                "Vitamins are organic micronutrients required for many "
                "physiological processes.",
            "key": [
                "Different vitamins perform different functions.",
                "Some are water-soluble and others fat-soluble.",
                "A varied diet helps provide many vitamins."
            ]
        },

        "Minerals": {
            "overview":
                "Minerals are essential elements needed for functions such "
                "as bone health, oxygen transport and nerve activity.",
            "key": [
                "Iron is involved in oxygen transport.",
                "Calcium contributes to bone health.",
                "Zinc supports many biological processes."
            ]
        },

        "Hydration": {
            "overview":
                "Fluids support circulation, temperature regulation and "
                "many normal physiological processes.",
            "key": [
                "Fluid needs vary.",
                "Hot environments can increase fluid needs.",
                "Physical activity can increase fluid loss."
            ]
        },

        "Food Safety": {
            "overview":
                "Food safety reduces the risk of foodborne illness.",
            "key": [
                "Wash hands before food preparation.",
                "Separate raw and ready-to-eat foods.",
                "Cook foods appropriately.",
                "Store foods safely."
            ]
        },

        "Food Security": {
            "overview":
                "Food security concerns reliable access to sufficient, safe "
                "and nutritious food.",
            "key": [
                "Availability matters.",
                "Access matters.",
                "Utilization and nutrition quality matter.",
                "Stability over time matters."
            ]
        },

        "Undernutrition": {
            "overview":
                "Undernutrition occurs when nutritional requirements are not "
                "adequately met and can include wasting, stunting and underweight.",
            "key": [
                "Causes can be complex.",
                "Food insecurity can contribute.",
                "Disease and infection can contribute.",
                "Assessment should use appropriate clinical and nutritional methods."
            ]
        }
    }

    topic = st.selectbox(
        "Choose a learning topic",
        list(topics.keys())
    )

    data = topics[topic]

    st.subheader(topic)

    st.info(data["overview"])

    st.subheader("Key Learning Points")

    for point in data["key"]:
        st.write("•", point)

    st.divider()

    st.subheader("🧠 Knowledge Check")

    quiz = {
        "Balanced Diet": (
            "Which approach best describes a balanced diet?",
            [
                "Eating only one food group",
                "Eating a variety of foods and nutrients",
                "Avoiding all carbohydrates",
                "Drinking water only"
            ],
            "Eating a variety of foods and nutrients"
        ),

        "Protein": (
            "Which nutrient is especially important for tissue growth and repair?",
            [
                "Protein",
                "Water only",
                "Salt only",
                "None of these"
            ],
            "Protein"
        ),

        "Carbohydrates": (
            "Which nutrient is an important source of dietary energy?",
            [
                "Carbohydrates",
                "Water",
                "Minerals only",
                "None"
            ],
            "Carbohydrates"
        ),

        "Fats": (
            "Which is a role of dietary fat?",
            [
                "It supports absorption of some vitamins",
                "It has no biological role",
                "It replaces all micronutrients",
                "It is only found in meat"
            ],
            "It supports absorption of some vitamins"
        ),

        "Vitamins": (
            "Vitamins are generally classified as:",
            [
                "Micronutrients",
                "Macronutrients only",
                "Proteins",
                "Water"
            ],
            "Micronutrients"
        ),

        "Minerals": (
            "Which is an essential mineral?",
            [
                "Iron",
                "Glucose",
                "Protein",
                "Water"
            ],
            "Iron"
        ),

        "Hydration": (
            "Why is hydration important?",
            [
                "Water supports many normal body functions",
                "Water provides all nutrients",
                "Water replaces protein",
                "Hydration has no role"
            ],
            "Water supports many normal body functions"
        ),

        "Food Safety": (
            "Which practice helps reduce foodborne illness?",
            [
                "Separating raw and ready-to-eat foods",
                "Leaving food uncovered",
                "Ignoring storage temperatures",
                "Using dirty utensils"
            ],
            "Separating raw and ready-to-eat foods"
        ),

        "Food Security": (
            "Food security includes reliable access to:",
            [
                "Sufficient, safe and nutritious food",
                "Water only",
                "Supplements only",
                "One food every day"
            ],
            "Sufficient, safe and nutritious food"
        ),

        "Undernutrition": (
            "Which can contribute to undernutrition?",
            [
                "Inadequate nutrient intake",
                "Only exercise",
                "Only drinking water",
                "None"
            ],
            "Inadequate nutrient intake"
        )
    }

    q, options, correct = quiz[topic]

    answer = st.radio(
        q,
        options,
        key="quiz_" + topic
    )

    if st.button("Check Answer", key="check_" + topic):

        if answer == correct:
            st.success("Correct! 🌱")

        else:
            st.error("Not quite. Review the learning points above.")


# ============================================================
# INSIGHTS
# ============================================================

elif st.session_state.page == "Insights":

    st.markdown(
        '<div class="section-title">📊 Nutrition Insights</div>',
        unsafe_allow_html=True
    )

    st.write(
        "A simple educational view of important nutrition indicators."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Core Nutrition Areas", "10+")

    with c2:
        st.metric("Prototype Modules", "9")

    with c3:
        st.metric("Primary Focus", "Nutrition Awareness")

    st.subheader("Nutrition Assessment Is Multi-Dimensional")

    st.write(
        "BMI alone cannot describe complete nutritional status. "
        "Real nutrition assessment can consider dietary intake, growth, "
        "clinical information, anthropometric measurements, social factors "
        "and other relevant evidence."
    )

    st.subheader("SDG Connections")

    sdgs = {
        "SDG 2 — Zero Hunger":
            "Nouriva addresses nutrition awareness, food security and undernutrition.",

        "SDG 3 — Good Health and Well-Being":
            "Nutrition education supports awareness related to health and well-being.",

        "SDG 4 — Quality Education":
            "The Education Centre provides accessible nutrition learning.",

        "SDG 10 — Reduced Inequalities":
            "Accessible digital education can help broaden access to basic nutrition information.",

        "SDG 17 — Partnerships":
            "Nutrition challenges require collaboration across health, education, communities and technology."
    }

    for name, description in sdgs.items():

        st.markdown(
            f"""
            <div class="tool-card" style="min-height:auto;">
                <b>{name}</b><br>
                {description}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# GROWTH MONITOR
# ============================================================

elif st.session_state.page == "Growth Monitor":

    st.markdown(
        '<div class="section-title">🧒 Growth Monitor</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Explore the concept of child and adolescent growth monitoring."
    )

    st.markdown(
        '<div class="warning-box"><b>Important:</b> Pediatric growth '
        'cannot be classified using adult BMI categories alone. '
        'Validated age- and sex-specific growth references are required.'
        '</div>',
        unsafe_allow_html=True
    )

    age = st.number_input(
        "Child/adolescent age (years)",
        min_value=0.0,
        max_value=19.0,
        value=10.0,
        step=0.1
    )

    sex = st.selectbox(
        "Sex",
        ["Male", "Female"],
        key="growth_sex"
    )

    height = st.number_input(
        "Height (cm)",
        min_value=30.0,
        max_value=220.0,
        value=140.0,
        step=0.1,
        key="growth_height"
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=200.0,
        value=35.0,
        step=0.1,
        key="growth_weight"
    )

    if st.button(
        "Calculate BMI for Reference",
        type="primary",
        use_container_width=True
    ):

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)

        st.metric("BMI", bmi)

        st.info(
            "This BMI value is shown for reference only. "
            "For children and adolescents, interpretation requires "
            "age- and sex-specific BMI-for-age references and appropriate "
            "clinical assessment."
        )


# ============================================================
# FOOD SCANNER
# ============================================================

elif st.session_state.page == "Food Scanner":

    st.markdown(
        '<div class="section-title">📷 Food Scanner</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload a food image to demonstrate Nouriva's future "
        "image-analysis workflow."
    )

    uploaded = st.file_uploader(
        "Upload a food image",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded:

        st.image(
            uploaded,
            caption="Uploaded food image",
            use_container_width=True
        )

        st.success(
            "Image received successfully."
        )

        st.subheader("Prototype Analysis Workflow")

        st.write("1. Image uploaded")
        st.write("2. Food object detection — future AI module")
        st.write("3. Food identification — future AI module")
        st.write("4. Portion estimation — future AI module")
        st.write("5. Nutrition estimation — future AI module")

        st.info(
            "The current prototype does not pretend to identify food "
            "or calories without a validated computer-vision model."
        )

    else:

        st.info(
            "Upload an image to test the prototype workflow."
        )


# ============================================================
# GLOBAL NUTRITION
# ============================================================

elif st.session_state.page == "Global Nutrition":

    st.markdown(
        '<div class="section-title">🌍 Global Nutrition</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Nutrition is a global challenge involving health, food systems, "
        "poverty, education and access."
    )

    areas = [
        (
            "Undernutrition",
            "Includes conditions such as wasting, stunting and underweight."
        ),
        (
            "Micronutrient Deficiencies",
            "Inadequate intake or absorption of essential vitamins and minerals."
        ),
        (
            "Food Security",
            "Reliable access to sufficient, safe and nutritious food."
        ),
        (
            "Maternal & Child Nutrition",
            "Nutrition during early life has important implications for growth and development."
        ),
        (
            "Double Burden of Malnutrition",
            "Undernutrition can coexist with overweight, obesity and diet-related disease."
        )
    ]

    for title, description in areas:

        st.markdown(
            f"""
            <div class="tool-card" style="min-height:auto;">
                <div class="tool-title">{title}</div>
                <div class="tool-text">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.subheader("🌱 Why Technology Matters")

    st.write(
        "Digital tools can help make educational information easier to access, "
        "support preliminary screening workflows and visualize nutrition "
        "challenges. However, technology should complement rather than replace "
        "qualified healthcare and nutrition professionals."
    )


# ============================================================
# HEALTH REPORT
# ============================================================

elif st.session_state.page == "Health Report":

    st.markdown(
        '<div class="section-title">📄 Educational Health Report</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Generate a simple educational screening summary."
    )

    name = st.text_input(
        "Name (optional)"
    )

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=20
    )

    height = st.number_input(
        "Height (cm)",
        min_value=30.0,
        max_value=250.0,
        value=170.0
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=300.0,
        value=55.0
    )

    if st.button(
        "Generate Report",
        type="primary",
        use_container_width=True
    ):

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)

        if age >= 18:

            if bmi < 18.5:
                interpretation = "Below standard adult BMI reference range."

            elif bmi < 25:
                interpretation = "Within standard adult BMI reference range."

            elif bmi < 30:
                interpretation = "Above standard adult BMI reference range."

            else:
                interpretation = "High adult BMI range."

        else:

            interpretation = (
                "Pediatric BMI requires age- and sex-specific interpretation."
            )

        report = f"""
NOURIVA AI
Educational Nutrition Screening Report
--------------------------------------

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Name: {name if name else "Not provided"}
Age: {age} years
Height: {height} cm
Weight: {weight} kg
BMI: {bmi}

Interpretation:
{interpretation}

Important:
This report is generated by a student-built educational prototype.
It is not a diagnosis and should not replace professional assessment.

For children and adolescents, BMI must be interpreted using
appropriate age- and sex-specific references.

Nouriva AI
Nutrition • Education • Awareness
"""

        st.success("Report generated.")

        st.download_button(
            "⬇️ Download Educational Report",
            data=report,
            file_name="nouriva_ai_screening_report.txt",
            mime="text/plain",
            use_container_width=True
        )

        st.text(report)


# ============================================================
# ABOUT
# ============================================================

elif st.session_state.page == "About":

    st.markdown(
        '<div class="section-title">ℹ️ About Nouriva AI</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    ### 🌿 Nouriva AI

    Nouriva AI is a student-built health-technology prototype focused on
    nutrition awareness, education and preliminary screening.

    ### 🎯 What Nouriva explores

    - Preliminary nutrition screening
    - BMI calculation
    - Nutrition-risk indicators
    - Nutrition education
    - Meal-planning concepts
    - Growth-monitoring concepts
    - Food-image analysis workflow
    - Global nutrition awareness
    - Sustainable Development Goal connections

    ### 💡 Vision

    To explore how accessible digital technology and responsible AI-assisted
    tools could help people understand nutrition and make nutrition education
    easier to access.

    ### 👨‍💻 Creator

    **Muhammad Ahsan Shahzad**

    BS Human Nutrition & Dietetics Student  
    Pakistan

    ### 🚀 Hackathon Prototype

    Nouriva AI was developed as a student health-technology prototype for
    social-impact innovation.

    ### ⚠️ Responsible Use

    Nouriva AI does **not** diagnose disease, replace healthcare professionals,
    or provide definitive medical advice.

    Some modules intentionally demonstrate future workflows rather than
    pretending that an unvalidated AI model already exists.
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    🌿 <b>Nouriva AI</b> • Nutrition • Education • Awareness<br>
    Student Health-Technology Prototype • 2026<br><br>
    Educational prototype — not a diagnostic medical system.
</div>
""", unsafe_allow_html=True)
