
import streamlit as st

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="centered"
)

st.title("🌿 Nouriva AI")
st.subheader("AI-Assisted Nutrition Screening & Education")

st.write(
    "A student-built prototype for preliminary nutrition "
    "screening and nutrition education."
)

st.divider()

st.header("👤 Your Information")

age = st.number_input("Age (years)", 1, 120, 20)
sex = st.selectbox("Sex", ["Male", "Female"])
height = st.number_input("Height (cm)", 30.0, 250.0, 170.0)
weight = st.number_input("Weight (kg)", 1.0, 300.0, 55.0)

st.header("🍎 Diet & Lifestyle")

meals = st.selectbox("Typical meals per day", [1, 2, 3, 4, 5])

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

if st.button("🔍 Analyze My Nutrition", use_container_width=True):

    height_m = height / 100
    bmi = round(weight / (height_m ** 2), 1)

    st.header("📊 Preliminary Screening")
    st.metric("BMI", bmi)

    if age >= 18:
        if bmi < 18.5:
            st.warning("BMI is below the standard adult range.")
        elif bmi < 25:
            st.success("BMI is within the standard adult range.")
        elif bmi < 30:
            st.info("BMI is above the standard adult range.")
        else:
            st.warning("BMI is in a high adult BMI range.")
    else:
        st.info(
            "For people under 18, BMI should be interpreted "
            "using age- and sex-specific growth references."
        )

    risk_score = 0

    if age >= 18 and bmi < 18.5:
        risk_score += 2

    if meals <= 2:
        risk_score += 1

    if len(protein) == 0:
        risk_score += 1

    if fruit_veg == "Rarely":
        risk_score += 1

    if food_access == "Often difficult":
        risk_score += 2
    elif food_access == "Sometimes difficult":
        risk_score += 1

    st.subheader("🌱 Preliminary Nutrition Risk")

    if risk_score >= 4:
        st.warning("Higher potential nutrition-risk factors identified.")
    elif risk_score >= 2:
        st.info("Some potential nutrition-risk factors identified.")
    else:
        st.success("Few risk factors identified in this basic screening.")

    st.subheader("💡 General Nutrition Guidance")

    st.write("""
    • Aim for a varied and balanced diet.

    • Include affordable protein sources such as eggs,
      pulses, dairy, fish or other suitable foods.

    • Include fruits and vegetables regularly.

    • Maintain adequate fluid intake.

    • If you have concerns about weight, growth, food access
      or health, seek advice from a qualified professional.
    """)

    st.subheader("🤖 Ask Nouriva AI")

    question = st.text_input("Ask a nutrition education question")

    if question:
        st.info(
            "Nouriva AI: personalized AI assistance will be "
            "added in a future version."
        )

st.divider()

st.caption(
    "⚠️ Nouriva AI is a student prototype for nutrition "
    "education and preliminary screening. It does not "
    "diagnose disease or replace professional healthcare."
)
