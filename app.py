import streamlit as st
from datetime import datetime
from io import BytesIO

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
}
.subtitle {
    font-size: 19px;
    opacity: 0.8;
}
.card {
    padding: 22px;
    border-radius: 16px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 15px;
}
.small-note {
    font-size: 13px;
    opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown('<div class="main-title">🌿 Nouriva AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Assisted Nutrition Screening & Education Platform</div>',
    unsafe_allow_html=True
)

st.write(
    "A student-built health-technology prototype designed to improve "
    "nutrition awareness through screening, education and accessible "
    "digital tools."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🌿 Nouriva AI")
st.sidebar.caption("Nutrition • Education • Awareness")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🔍 Nutrition Scan",
        "🍽️ Diet Planner",
        "🤖 Nutrition Coach",
        "📚 Nutrition Education",
        "📊 Nutrition Insights",
        "🧒 Growth Monitor",
        "📷 Food Scanner",
        "🌍 Global Nutrition",
        "📄 Health Report",
        "ℹ️ About Nouriva"
    ]
)

# -----------------------------
# Dashboard
# -----------------------------
if page == "🏠 Dashboard":

    st.header("🏠 Nouriva AI Dashboard")

    st.success(
        "Welcome! Explore nutrition screening, meal planning, "
        "education and global nutrition awareness tools."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Core Tools", "10")

    with col2:
        st.metric("Focus", "Nutrition + AI")

    with col3:
        st.metric("Status", "Working Prototype")

    st.divider()

    st.subheader("🚀 Explore Nouriva")

    cards = [
        ("🔍 Nutrition Scan", "Preliminary BMI and nutrition-risk screening."),
        ("🍽️ Diet Planner", "Generate simple example meal plans."),
        ("🤖 Nutrition Coach", "Ask general nutrition education questions."),
        ("📚 Education", "Learn essential nutrition concepts."),
        ("📊 Insights", "Explore nutrition indicators."),
        ("🧒 Growth Monitor", "Explore age and growth monitoring concepts."),
        ("📷 Food Scanner", "Upload a food image for future analysis."),
        ("🌍 Global Nutrition", "Explore global nutrition challenges."),
        ("📄 Health Report", "Create a downloadable screening summary."),
    ]

    cols = st.columns(3)

    for i, (title, description) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="card">
                <h3>{title}</h3>
                <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.info(
        "🌱 Nouriva AI is designed as an educational prototype and "
        "does not diagnose medical conditions."
    )


# -----------------------------
# Nutrition Scan
# -----------------------------
elif page == "🔍 Nutrition Scan":

    st.header("🔍 Nutrition Scan")

    st.write(
        "Enter basic information for a preliminary nutrition screening."
    )

    col1, col2 = st.columns(2)

    with col1:
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

        weight = st.number_input(
            "Weight (kg)",
            min_value=1.0,
            max_value=300.0,
            value=55.0,
            step=0.1
        )

    with col2:
        meals = st.selectbox(
            "Typical meals per day",
            [1, 2, 3, 4, 5]
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

        fruit_veg = st.selectbox(
            "Fruit & vegetable intake",
            ["Rarely", "Sometimes", "Daily"]
        )

        food_access = st.selectbox(
            "Access to sufficient food",
            [
                "Usually sufficient",
                "Sometimes difficult",
                "Often difficult"
            ]
        )

    st.divider()

    analyze = st.button(
        "🔍 Analyze My Nutrition",
        type="primary",
        use_container_width=True
    )

    if analyze:

        height_m = height / 100

        bmi = round(
            weight / (height_m ** 2),
            1
        )

        risk_score = 0
        risk_factors = []

        if age >= 18:

            if bmi < 18.5:
                risk_score += 2
                risk_factors.append("BMI below standard adult range")

            elif bmi >= 30:
                risk_score += 1
                risk_factors.append("BMI in a high adult BMI range")

        if meals <= 2:
            risk_score += 1
            risk_factors.append("Low reported meal frequency")

        if len(protein) == 0:
            risk_score += 1
            risk_factors.append("No selected protein sources")

        if fruit_veg == "Rarely":
            risk_score += 1
            risk_factors.append("Low fruit and vegetable intake")

        if food_access == "Often difficult":
            risk_score += 2
            risk_factors.append("Food access difficulty")

        elif food_access == "Sometimes difficult":
            risk_score += 1
            risk_factors.append("Occasional food access difficulty")

        st.session_state["last_screening"] = {
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "risk_score": risk_score,
            "risk_factors": risk_factors
        }

        st.subheader("📊 Screening Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("BMI", bmi)

        with c2:
            st.metric("Risk Score", risk_score)

        with c3:
            if risk_score >= 4:
                level = "Higher"
            elif risk_score >= 2:
                level = "Moderate"
            else:
                level = "Lower"

            st.metric("Risk Level", level)

        if age < 18:
            st.info(
                "For people under 18, BMI should be interpreted using "
                "age- and sex-specific growth references rather than "
                "adult BMI cutoffs."
            )

        elif bmi < 18.5:
            st.warning(
                "BMI is below the standard adult range."
            )

        elif bmi < 25:
            st.success(
                "BMI is within the standard adult range."
            )

        elif bmi < 30:
            st.info(
                "BMI is above the standard adult range."
            )

        else:
            st.warning(
                "BMI is in a high adult BMI range."
            )

        st.subheader("🌱 Potential Nutrition Risk Factors")

        if risk_factors:
            for factor in risk_factors:
                st.write("• " + factor)
        else:
            st.success(
                "No major risk factors were identified by this basic screening."
            )

        st.subheader("💡 General Nutrition Guidance")

        guidance = [
            "Aim for a varied and balanced diet.",
            "Include suitable protein sources such as eggs, pulses, dairy, fish or meat.",
            "Include fruits and vegetables regularly.",
            "Maintain adequate fluid intake.",
            "Seek qualified professional advice for persistent nutrition or health concerns."
        ]

        for item in guidance:
            st.write("• " + item)

        st.caption(
            "This screening is educational and is not a medical diagnosis."
        )


# -----------------------------
# Diet Planner
# -----------------------------
elif page == "🍽️ Diet Planner":

    st.header("🍽️ Nouriva Diet Planner")

    goal = st.selectbox(
        "Choose a general nutrition goal",
        [
            "Balanced nutrition",
            "Healthy weight gain",
            "Healthy weight management",
            "Athletic nutrition"
        ]
    )

    dietary = st.selectbox(
        "Diet preference",
        [
            "No specific preference",
            "Vegetarian",
            "High-protein"
        ]
    )

    st.divider()

    if goal == "Healthy weight gain":

        meals_plan = [
            ("🌅 Breakfast", "Eggs + milk + roti + banana"),
            ("☀️ Snack", "Yogurt + nuts"),
            ("🍛 Lunch", "Rice/roti + lentils + chicken + vegetables"),
            ("🌇 Snack", "Milk + fruit"),
            ("🌙 Dinner", "Roti + beans/meat + vegetables")
        ]

    elif goal == "Athletic nutrition":

        meals_plan = [
            ("🌅 Breakfast", "Eggs + oats + milk + fruit"),
            ("☀️ Snack", "Yogurt + nuts"),
            ("🍛 Lunch", "Rice + chicken/fish + vegetables"),
            ("🌇 Snack", "Banana + milk"),
            ("🌙 Dinner", "Roti + lentils + vegetables")
        ]

    else:

        meals_plan = [
            ("🌅 Breakfast", "Eggs + roti + fruit"),
            ("☀️ Snack", "Fruit + yogurt"),
            ("🍛 Lunch", "Lentils + rice/roti + vegetables"),
            ("🌇 Snack", "Milk + fruit"),
            ("🌙 Dinner", "Roti + vegetables + protein source")
        ]

    if dietary == "Vegetarian":
        meals_plan = [
            (meal, food.replace("chicken", "lentils").replace(
                "chicken/fish", "lentils/beans"
            ).replace("meat", "beans"))
            for meal, food in meals_plan
        ]

    for meal, food in meals_plan:
        st.markdown(
            f"""
            <div class="card">
            <h3>{meal}</h3>
            <p>{food}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.caption(
        "Example educational meal plan. Individual dietary needs vary."
    )


# -----------------------------
# Nutrition Coach
# -----------------------------
elif page == "🤖 Nutrition Coach":

    st.header("🤖 Nouriva Nutrition Coach")

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
                "Protein supports growth, tissue maintenance and repair. "
                "Common sources include eggs, dairy, pulses, fish, meat, "
                "nuts and seeds."
            )

        elif "water" in q or "hydration" in q:
            answer = (
                "Adequate fluid intake supports normal body functions "
                "and helps maintain hydration."
            )

        elif "iron" in q:
            answer = (
                "Iron is an essential mineral involved in oxygen transport. "
                "Food sources include meat, lentils, beans and some "
                "fortified foods."
            )

        elif "vitamin" in q:
            answer = (
                "Vitamins are micronutrients required for many biological "
                "functions. A varied diet helps provide different vitamins."
            )

        elif "bmi" in q:
            answer = (
                "BMI is calculated from weight and height. It is a screening "
                "measure, not a diagnosis, and has limitations."
            )

        else:
            answer = (
                "Nouriva AI can provide general nutrition education about "
                "topics such as balanced diets, protein, hydration, "
                "micronutrients, food security and BMI."
            )

        st.info("🌿 Nouriva Coach")
        st.write(answer)

        st.caption(
            "Educational response only — not individualized medical advice."
        )


# -----------------------------
# Education
# -----------------------------
elif page == "📚 Nutrition Education":

    st.header("📚 Nutrition Education")

    topic = st.selectbox(
        "Choose a topic",
        [
            "Balanced Diet",
            "Protein",
            "Micronutrients",
            "Hydration",
            "Food Security",
            "Undernutrition",
            "BMI"
        ]
    )

    education = {

        "Balanced Diet":
            "A balanced diet includes a variety of foods that provide "
            "energy, protein, vitamins, minerals and other nutrients.",

        "Protein":
            "Protein supports growth, tissue maintenance and repair. "
            "Sources include eggs, dairy, pulses, fish, meat, nuts and seeds.",

        "Micronutrients":
            "Vitamins and minerals are needed in smaller quantities but "
            "are essential for normal biological functions.",

        "Hydration":
            "Adequate fluid intake supports normal body functions and "
            "helps maintain hydration.",

        "Food Security":
            "Food security means people have reliable access to sufficient, "
            "safe and nutritious food.",

        "Undernutrition":
            "Undernutrition can occur when the body does not receive enough "
            "energy or nutrients. It can include wasting, stunting and underweight.",

        "BMI":
            "BMI is a simple weight-for-height screening measure. It should "
            "not be used alone to diagnose a person's health or nutritional status."
    }

    st.info(education[topic])

    st.divider()

    st.subheader("🧠 Quick Knowledge Check")

    quiz = st.radio(
        "Which nutrient is especially important for tissue growth and repair?",
        [
            "Protein",
            "Water only",
            "Salt only",
            "None of these"
        ]
    )

    if st.button("Check Answer"):

        if quiz == "Protein":
            st.success("Correct! 🎉")
        else:
            st.warning(
                "The best answer is Protein."
            )


# -----------------------------
# Insights
# -----------------------------
elif page == "📊 Nutrition Insights":

    st.header("📊 Nutrition Insights")

    st.write(
        "Nouriva AI can be expanded to integrate validated public "
        "nutrition datasets and interactive indicators."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Nutrition", "Awareness")

    with c2:
        st.metric("Technology", "AI")

    with c3:
        st.metric("SDG Focus", "2 + 3")

    st.divider()

    st.subheader("Potential Data Areas")

    st.write("🌍 Food security")
    st.write("🧒 Child growth")
    st.write("🥗 Dietary diversity")
    st.write("🩺 Undernutrition")
    st.write("💧 Hydration")
    st.write("🌱 Sustainable nutrition")


# -----------------------------
# Growth Monitor
# -----------------------------
elif page == "🧒 Growth Monitor":

    st.header("🧒 Growth Monitor")

    st.info(
        "This prototype demonstrates the concept of growth monitoring. "
        "A production system should use validated age- and sex-specific "
        "growth references."
    )

    age = st.number_input(
        "Child age (years)",
        min_value=0.0,
        max_value=18.0,
        value=5.0,
        step=0.1
    )

    height = st.number_input(
        "Height (cm)",
        min_value=30.0,
        max_value=220.0,
        value=105.0
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        max_value=150.0,
        value=17.0
    )

    if st.button("Calculate Growth Indicators"):

        bmi = round(
            weight / ((height / 100) ** 2),
            1
        )

        st.metric("BMI", bmi)

        st.warning(
            "BMI alone cannot determine whether a child is growing normally. "
            "Clinical growth assessment requires age- and sex-specific references."
        )


# -----------------------------
# Food Scanner
# -----------------------------
elif page == "📷 Food Scanner":

    st.header("📷 Food Scanner")

    st.write(
        "Upload a food image to demonstrate the future image-analysis workflow."
    )

    uploaded = st.file_uploader(
        "Upload food image",
        type=["jpg", "jpeg", "png"]
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

        st.info(
            "🤖 Future AI vision capability: food recognition, "
            "portion estimation and nutrition estimation."
        )

        st.caption(
            "This prototype does not currently make nutritional claims "
            "from uploaded images."
        )


# -----------------------------
# Global Nutrition
# -----------------------------
elif page == "🌍 Global Nutrition":

    st.header("🌍 Global Nutrition")

    st.write(
        "Nutrition is closely connected with global development, "
        "food security and health."
    )

    st.subheader("🌱 Sustainable Development Goals")

    st.markdown("""
    **SDG 2 — Zero Hunger**

    Improve food security, nutrition and sustainable agriculture.

    **SDG 3 — Good Health and Well-being**

    Promote health and well-being across the life course.

    **SDG 12 — Responsible Consumption and Production**

    Encourage more sustainable food systems and consumption.
    """)

    st.divider()

    st.subheader("Global Nutrition Challenges")

    challenges = [
        "Undernutrition",
        "Micronutrient deficiencies",
        "Food insecurity",
        "Child growth problems",
        "Diet-related health risks",
        "Sustainable food systems"
    ]

    for item in challenges:
        st.write("🌍 " + item)


# -----------------------------
# Health Report
# -----------------------------
elif page == "📄 Health Report":

    st.header("📄 Health Report")

    data = st.session_state.get("last_screening")

    if not data:

        st.info(
            "Complete a Nutrition Scan first to generate a screening report."
        )

    else:

        st.subheader("🌿 Nouriva AI — Screening Summary")

        report = f"""
NOURIVA AI
Nutrition Screening & Education

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Age: {data["age"]}
Sex: {data["sex"]}
Height: {data["height"]:.1f} cm
Weight: {data["weight"]:.1f} kg

BMI: {data["bmi"]}
Preliminary Risk Score: {data["risk_score"]}

Potential Risk Factors:
"""

        if data["risk_factors"]:
            for factor in data["risk_factors"]:
                report += f"- {factor}\n"
        else:
            report += "- None identified by this basic screening.\n"

        report += """
    
IMPORTANT:
This is an educational screening prototype.
It does not diagnose disease and does not replace
professional healthcare assessment.
"""

        st.text(report)

        st.download_button(
            "⬇️ Download Screening Report",
            data=report,
            file_name="Nouriva_AI_Screening_Report.txt",
            mime="text/plain",
            use_container_width=True
        )


# -----------------------------
# About
# -----------------------------
elif page == "ℹ️ About Nouriva":

    st.header("ℹ️ About Nouriva AI")

    st.markdown("""
### 🌿 Nouriva AI

**Nouriva AI** is a student-built health-technology prototype focused on:

- Nutrition awareness
- Preliminary nutrition screening
- Nutrition education
- Accessible digital health tools
- Global nutrition awareness

### 💡 Vision

To create an accessible AI-powered nutrition companion that can help
people better understand nutrition and potential nutrition-related risks.

### 👨‍💻 Creator

**Muhammad Ahsan Shahzad**

BS Human Nutrition & Dietetics Student

Pakistan

### 🚀 Hackathon Prototype

This project demonstrates how AI-assisted digital tools could support
nutrition awareness and education.

### ⚠️ Important

Nouriva AI is an educational prototype.

It does **not** diagnose disease, replace healthcare professionals,
or provide definitive medical advice.
""")

st.divider()

st.caption(
    "🌿 Nouriva AI • Student Health-Technology Prototype"
  )
