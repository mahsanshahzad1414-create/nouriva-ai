import streamlit as st

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Nouriva AI")
st.subheader("AI-Assisted Nutrition & Health Education Platform")

st.write(
    "Welcome to Nouriva AI — an intelligent platform for "
    "nutrition screening, education and health awareness."
)

st.divider()

st.sidebar.title("🌿 Nouriva AI")

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
        "📄 Health Report"
    ]
)

if page == "🏠 Dashboard":

    st.header("🏠 Your Nutrition Dashboard")

    st.success(
        "Welcome to Nouriva AI. Choose a tool from the menu "
        "to explore nutrition screening, education and planning."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🔍 Nutrition Scan\n\nBasic nutrition screening.")

    with col2:
        st.info("🍽️ Diet Planner\n\nExplore balanced meal ideas.")

    with col3:
        st.info("🤖 Nutrition Coach\n\nNutrition education assistant.")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.info("📚 Education\n\nLearn nutrition concepts.")

    with col5:
        st.info("📊 Insights\n\nExplore nutrition information.")

    with col6:
        st.info("🌍 Global Nutrition\n\nExplore global nutrition challenges.")

    st.divider()

    st.subheader("🚀 Nouriva AI")

    st.write(
        "Student-built health-technology prototype focused on "
        "nutrition awareness and education."
    )


elif page == "🔍 Nutrition Scan":

    st.header("🔍 Nutrition Scan")

    st.write(
        "Enter basic information for a preliminary nutrition screening."
    )

    age = st.number_input(
        "Age (years)", 1, 120, 20
    )

    sex = st.selectbox(
        "Sex", ["Male", "Female"]
    )

    height = st.number_input(
        "Height (cm)", 30.0, 250.0, 170.0
    )

    weight = st.number_input(
        "Weight (kg)", 1.0, 300.0, 55.0
    )

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

    if st.button(
        "🔍 Analyze Nutrition",
        use_container_width=True
    ):

        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)

        st.divider()

        st.header("📊 Screening Result")

        st.metric("BMI", bmi)

        if age >= 18:

            if bmi < 18.5:
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

        else:

            st.info(
                "For people under 18, BMI should be interpreted "
                "using age- and sex-specific growth references."
            )

        risk = 0

        if age >= 18 and bmi < 18.5:
            risk += 2

        if meals <= 2:
            risk += 1

        if len(protein) == 0:
            risk += 1

        if fruit_veg == "Rarely":
            risk += 1

        if food_access == "Often difficult":
            risk += 2

        elif food_access == "Sometimes difficult":
            risk += 1

        st.subheader("🌱 Preliminary Nutrition Risk")

        if risk >= 4:

            st.warning(
                "Higher potential nutrition-risk factors identified."
            )

        elif risk >= 2:

            st.info(
                "Some potential nutrition-risk factors identified."
            )

        else:

            st.success(
                "Few risk factors identified in this basic screening."
            )

        st.subheader("💡 General Guidance")

        st.write(
            """
• Aim for a varied and balanced diet.

• Include protein-rich foods such as eggs, pulses,
  dairy, fish or other suitable sources.

• Eat fruits and vegetables regularly.

• Maintain adequate fluid intake.

• Seek professional advice if you have concerns
  about nutrition, growth, weight or health.
"""
        )


elif page == "🍽️ Diet Planner":

    st.header("🍽️ Nouriva Diet Planner")

    goal = st.selectbox(
        "Choose your general goal",
        [
            "Balanced nutrition",
            "Healthy weight gain",
            "Healthy weight management",
            "Athletic nutrition"
        ]
    )

    st.subheader("🥗 Example Day")

    if goal == "Healthy weight gain":

        meals_plan = [
            "🌅 Breakfast: Eggs + milk + roti + banana",
            "☀️ Snack: Yogurt + nuts",
            "🍛 Lunch: Rice/roti + lentils + chicken + vegetables",
            "🌇 Snack: Milk + fruit",
            "🌙 Dinner: Roti + beans/meat + vegetables"
        ]

    elif goal == "Athletic nutrition":

        meals_plan = [
            "🌅 Breakfast: Eggs + oats + milk + fruit",
            "☀️ Snack: Yogurt + nuts",
            "🍛 Lunch: Rice + chicken/fish + vegetables",
            "🌇 Snack: Banana + milk",
            "🌙 Dinner: Roti + lentils + vegetables"
        ]

    else:

        meals_plan = [
            "🌅 Breakfast: Eggs + roti + fruit",
            "☀️ Snack: Fruit + yogurt",
            "🍛 Lunch: Lentils + rice/roti + vegetables",
            "🌇 Snack: Milk + fruit",
            "🌙 Dinner: Roti + vegetables + protein source"
        ]

    for meal in meals_plan:
        st.write(meal)


elif page == "🤖 Nutrition Coach":

    st.header("🤖 Nouriva Nutrition Coach")

    question = st.text_input(
        "Ask a general nutrition education question"
    )

    if question:

        st.info(
            "Nouriva Coach: This prototype currently provides "
            "general nutrition education. AI-powered responses "
            "will be added in a future version."
        )


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
            "Undernutrition"
        ]
    )

    education = {
        "Balanced Diet":
            "A balanced diet includes a variety of foods providing energy, protein, vitamins and minerals.",

        "Protein":
            "Protein supports growth, tissue repair and many important body functions.",

        "Micronutrients":
            "Vitamins and minerals are required in smaller amounts but are essential for health.",

        "Hydration":
            "Adequate fluids help maintain normal body functions and support hydration.",

        "Food Security":
            "Food security means people have reliable access to sufficient, safe and nutritious food.",

        "Undernutrition":
            "Undernutrition can occur when the body does not receive enough energy or nutrients."
    }

    st.info(education[topic])


elif page == "📊 Nutrition Insights":

    st.header("📊 Nutrition Insights")

    st.metric("Core MVP Modules", "4")
    st.metric("Innovation Focus", "Nutrition + AI")
    st.metric("Project Status", "Prototype")

    st.info(
        "Future versions can integrate public nutrition datasets "
        "and interactive visualizations."
    )


elif page == "🧒 Growth Monitor":

    st.header("🧒 Growth Monitor")

    st.info(
        "Future module: age- and sex-specific growth monitoring "
        "using validated growth references."
    )


elif page == "📷 Food Scanner":

    st.header("📷 Food Scanner")

    st.info(
        "Future module: image-based food recognition and "
        "nutrition estimation."
    )


elif page == "🌍 Global Nutrition":

    st.header("🌍 Global Nutrition")

    st.info(
        "Future module: global malnutrition, food-security "
        "and nutrition indicators."
    )


elif page == "📄 Health Report":

    st.header("📄 Health Report")

    st.info(
        "Future module: downloadable screening summary "
        "for educational purposes."
    )


st.divider()

st.caption(
    "⚠️ Nouriva AI is a student prototype for nutrition "
    "education and preliminary screening. It does not "
    "diagnose medical conditions or replace professional "
    "healthcare advice."
)
