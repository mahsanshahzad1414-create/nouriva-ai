import streamlit as st
from datetime import datetime
import html

st.set_page_config(
    page_title="Nouriva AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .main {padding-top: 1.5rem;}
    .hero {
        padding: 2rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #e8f5e9 0%, #f7fff8 55%, #e3f2fd 100%);
        border: 1px solid #d7ead9;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        color: #14532d;
        margin-bottom: .3rem;
    }
    .hero p {
        color: #365b46;
        font-size: 1.05rem;
    }
    .card {
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid #dfe9e1;
        background: white;
        min-height: 170px;
        box-shadow: 0 4px 14px rgba(20,83,45,.06);
        margin-bottom: 1rem;
    }
    .card h3 {
        color: #166534;
        margin-bottom: .45rem;
    }
    .metric-card {
        padding: 1rem;
        border-radius: 16px;
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        text-align: center;
    }
    .small-muted {
        color: #64748b;
        font-size: .9rem;
    }
    .section-title {
        color: #14532d;
        margin-top: .5rem;
    }
    .pill {
        display: inline-block;
        padding: .3rem .7rem;
        border-radius: 999px;
        background: #dcfce7;
        color: #166534;
        font-size: .82rem;
        margin-right: .3rem;
        margin-bottom: .3rem;
    }
    .footer {
        padding: 1rem;
        text-align: center;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------- Data ----------
EDUCATION = {
    "Balanced Diet": {
        "summary": "A balanced diet provides a variety of foods and nutrients needed for energy, growth, repair and normal body functions.",
        "key": [
            "Include a variety of food groups.",
            "Choose adequate protein sources.",
            "Include fruits and vegetables regularly.",
            "Maintain appropriate hydration.",
        ],
        "facts": [
            "No single food provides every nutrient in adequate amounts.",
            "Diet quality depends on variety, adequacy and balance.",
        ],
        "quiz": (
            "Which approach best supports a balanced diet?",
            ["Eating only one food group", "Eating a variety of nutritious foods", "Avoiding all carbohydrates", "Drinking water only"],
            "Eating a variety of nutritious foods",
        ),
    },
    "Protein": {
        "summary": "Protein provides amino acids needed for tissue growth, maintenance and repair and contributes to many body functions.",
        "key": [
            "Sources include eggs, dairy, pulses, fish, meat and nuts.",
            "Protein needs vary with age, body size and physiological state.",
            "Combining different foods can increase dietary variety.",
        ],
        "facts": [
            "Protein is made from amino acids.",
            "Protein supports maintenance and repair of body tissues.",
        ],
        "quiz": (
            "Which nutrient is especially important for tissue growth and repair?",
            ["Protein", "Water only", "Salt only", "None of these"],
            "Protein",
        ),
    },
    "Micronutrients": {
        "summary": "Vitamins and minerals are required in smaller amounts but are essential for normal growth, metabolism and body functions.",
        "key": [
            "Iron is important for oxygen transport.",
            "Calcium supports bones and teeth.",
            "Many micronutrients work together in metabolism.",
        ],
        "facts": [
            "Micronutrient deficiencies can occur even when energy intake is adequate.",
            "A varied diet helps improve micronutrient diversity.",
        ],
        "quiz": (
            "Which category includes vitamins and minerals?",
            ["Macronutrients", "Micronutrients", "Water only", "Fiber only"],
            "Micronutrients",
        ),
    },
    "Hydration": {
        "summary": "Water is essential for temperature regulation, circulation, digestion and many other physiological processes.",
        "key": [
            "Fluid needs vary between individuals.",
            "Heat and physical activity can increase fluid requirements.",
            "Water is a major source of hydration.",
        ],
        "facts": [
            "The body continually loses water through normal processes.",
            "Hydration needs depend on environment and activity.",
        ],
        "quiz": (
            "Which is a major function of water?",
            ["Supporting normal body functions", "Replacing all nutrients", "Providing all protein", "Eliminating the need for food"],
            "Supporting normal body functions",
        ),
    },
    "Food Security": {
        "summary": "Food security means people have reliable access to sufficient, safe and nutritious food that meets dietary needs and preferences.",
        "key": [
            "Availability is only one part of food security.",
            "Access and affordability also matter.",
            "Food safety and nutrition quality are important.",
        ],
        "facts": [
            "Food insecurity can affect diet quality and health.",
            "Economic and environmental factors can influence food access.",
        ],
        "quiz": (
            "Which is part of food security?",
            ["Reliable access to sufficient food", "Only food advertising", "Only food production", "Only restaurant access"],
            "Reliable access to sufficient food",
        ),
    },
    "Undernutrition": {
        "summary": "Undernutrition can occur when the body does not receive enough energy or nutrients, and it includes conditions such as wasting, stunting and micronutrient deficiencies.",
        "key": [
            "Undernutrition has multiple causes.",
            "Early identification can support appropriate referral.",
            "Children require age- and sex-specific growth assessment.",
        ],
        "facts": [
            "BMI alone is not sufficient for diagnosing malnutrition.",
            "Professional assessment may require clinical, dietary and growth information.",
        ],
        "quiz": (
            "Which statement is most appropriate?",
            ["BMI alone diagnoses every nutrition condition", "Undernutrition has multiple causes", "Children use adult BMI cutoffs", "Nutrition never affects growth"],
            "Undernutrition has multiple causes",
        ),
    },
    "Healthy Eating": {
        "summary": "Healthy eating emphasizes variety, adequacy, moderation and food choices appropriate to individual needs.",
        "key": [
            "Prioritize nutrient-dense foods.",
            "Use a variety of food groups.",
            "Consider cultural and economic realities.",
        ],
        "facts": [
            "Healthy diets can look different across cultures.",
            "Affordable foods can still contribute valuable nutrients.",
        ],
        "quiz": (
            "What is a useful principle of healthy eating?",
            ["Variety", "Eating one food repeatedly", "Avoiding all vegetables", "Skipping meals"],
            "Variety",
        ),
    },
    "Iron Nutrition": {
        "summary": "Iron is an essential mineral involved in hemoglobin formation and oxygen transport.",
        "key": [
            "Iron is found in animal and plant foods.",
            "Vitamin C can improve absorption of non-heme iron.",
            "Iron needs differ by age and physiological status.",
        ],
        "facts": [
            "Iron deficiency can impair normal physiological function.",
            "Dietary assessment should consider the overall eating pattern.",
        ],
        "quiz": (
            "Iron is especially important for which process?",
            ["Oxygen transport", "Vision only", "Hydration only", "Digestion only"],
            "Oxygen transport",
        ),
    },
    "Child Nutrition": {
        "summary": "Children have changing nutritional needs that support growth, development and healthy maturation.",
        "key": [
            "Growth should be assessed using age- and sex-specific references.",
            "Dietary variety is important.",
            "Persistent concerns should be discussed with a qualified professional.",
        ],
        "facts": [
            "Adult BMI categories should not simply be applied to children.",
            "Growth monitoring uses validated reference standards.",
        ],
        "quiz": (
            "How should child growth generally be interpreted?",
            ["Using age- and sex-specific references", "Using adult BMI alone", "Using weight alone", "Using height alone"],
            "Using age- and sex-specific references",
        ),
    },
    "Nutrition & SDGs": {
        "summary": "Nutrition is connected with global development, health, food security, poverty reduction and sustainable communities.",
        "key": [
            "SDG 2 focuses on Zero Hunger.",
            "SDG 3 focuses on Good Health and Well-being.",
            "Food systems influence nutrition outcomes.",
        ],
        "facts": [
            "Nutrition challenges are influenced by social, economic and environmental factors.",
            "Digital tools can support awareness and education.",
        ],
        "quiz": (
            "Which SDG is directly associated with Zero Hunger?",
            ["SDG 2", "SDG 7", "SDG 11", "SDG 16"],
            "SDG 2",
        ),
    },
}


def bmi_value(height_cm, weight_kg):
    if height_cm <= 0:
        return None
    return round(weight_kg / ((height_cm / 100) ** 2), 1)


def bmi_category(age, bmi):
    if age < 18:
        return "Needs age- and sex-specific interpretation"
    if bmi < 18.5:
        return "Below standard adult range"
    if bmi < 25:
        return "Standard adult range"
    if bmi < 30:
        return "Above standard adult range"
    return "High adult BMI range"


def nutrition_risk(age, bmi, meals, protein, fruit_veg, food_access):
    score = 0

    if age >= 18 and bmi < 18.5:
        score += 2

    if meals <= 2:
        score += 1

    if not protein:
        score += 1

    if fruit_veg == "Rarely":
        score += 1

    if food_access == "Often difficult":
        score += 2
    elif food_access == "Sometimes difficult":
        score += 1

    if score >= 4:
        level = "Higher potential risk factors"
    elif score >= 2:
        level = "Some potential risk factors"
    else:
        level = "Few risk factors identified"

    return score, level


def add_screening_to_session(result):
    st.session_state["last_screening"] = result


# ---------- Sidebar ----------
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
            "📚 Nutrition Education",
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


# ---------- Dashboard ----------
if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>🌿 Nouriva AI</h1>
        <p><b>AI-Assisted Nutrition Screening & Education Platform</b></p>
        <p>
        A student-built health-technology prototype designed to improve
        nutrition awareness through screening, education and accessible
        digital tools.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 Explore Nouriva")

    modules = [
        ("🔍 Nutrition Scan", "Preliminary BMI and nutrition-risk screening.", "Nutrition Scan"),
        ("🍽️ Diet Planner", "Build a simple example day around a general goal.", "Diet Planner"),
        ("🤖 Nutrition Coach", "Ask general nutrition education questions.", "Nutrition Coach"),
        ("📚 Education", "Explore structured nutrition lessons and quizzes.", "Nutrition Education"),
        ("📊 Insights", "Explore nutrition indicators and SDG connections.", "Nutrition Insights"),
        ("🧒 Growth Monitor", "Explore the concept of child growth monitoring.", "Growth Monitor"),
        ("📷 Food Scanner", "Upload a food image for prototype analysis workflow.", "Food Scanner"),
        ("🌍 Global Nutrition", "Explore global nutrition challenges and SDGs.", "Global Nutrition"),
        ("📄 Health Report", "Generate a downloadable educational screening report.", "Health Report"),
    ]

    cols = st.columns(3)

    for i, (title, desc, target) in enumerate(modules):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Open → {title.split(' ', 1)[1]}", key=f"dash_{i}", use_container_width=True):
                st.session_state["requested_page"] = target
                st.rerun()

    st.divider()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Core Modules", "9")

    with c2:
        st.metric("Education Topics", str(len(EDUCATION)))

    with c3:
        st.metric("Status", "Working Prototype")

    st.success(
        "🌱 Nouriva AI connects nutrition screening, education, planning "
        "and global nutrition awareness in one student-built prototype."
    )


# ---------- Nutrition Scan ----------
elif page == "🔍 Nutrition Scan":
    st.markdown("## 🔍 Nutrition Scan")
    st.write("Complete the form for a **preliminary educational screening**.")

    with st.form("nutrition_scan_form"):
        c1, c2 = st.columns(2)

        with c1:
            age = st.number_input("Age (years)", 1, 120, 20)
            sex = st.selectbox("Sex", ["Male", "Female"])
            height = st.number_input("Height (cm)", 30.0, 250.0, 170.0)

        with c2:
            weight = st.number_input("Weight (kg)", 1.0, 300.0, 55.0)
            meals = st.selectbox("Typical meals per day", [1, 2, 3, 4, 5], index=2)
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
        bmi = bmi_value(height, weight)
        score, level = nutrition_risk(
            age, bmi, meals, protein, fruit_veg, food_access
        )

        result = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "age": age,
            "sex": sex,
            "height": height,
            "weight": weight,
            "bmi": bmi,
            "category": bmi_category(age, bmi),
            "meals": meals,
            "protein": protein,
            "fruit_veg": fruit_veg,
            "food_access": food_access,
            "risk_score": score,
            "risk_level": level,
        }

        add_screening_to_session(result)

    if "last_screening" in st.session_state:
        r = st.session_state["last_screening"]

        st.divider()
        st.markdown("## 📊 Screening Result")

        a, b, c = st.columns(3)

        with a:
            st.metric("BMI", r["bmi"])

        with b:
            st.metric("Risk Score", r["risk_score"])

        with c:
            st.metric("Meals / Day", r["meals"])

        if r["age"] >= 18:
            if r["bmi"] < 18.5:
                st.warning(f"**BMI interpretation:** {r['category']}.")
            elif r["bmi"] < 25:
                st.success(f"**BMI interpretation:** {r['category']}.")
            elif r["bmi"] < 30:
                st.info(f"**BMI interpretation:** {r['category']}.")
            else:
                st.warning(f"**BMI interpretation:** {r['category']}.")
        else:
            st.info(
                "For people under 18, BMI should be interpreted using "
                "validated age- and sex-specific growth references."
            )

        if r["risk_score"] >= 4:
            st.warning(r["risk_level"])
        elif r["risk_score"] >= 2:
            st.info(r["risk_level"])
        else:
            st.success(r["risk_level"])

        st.markdown("### 💡 General Nutrition Guidance")

        guidance = [
            "Aim for a varied and balanced diet.",
            "Include suitable protein sources such as eggs, pulses, dairy, fish or other foods.",
            "Include fruits and vegetables regularly.",
            "Maintain adequate fluid intake.",
            "Seek advice from a qualified professional when nutrition or health concerns persist.",
        ]

        for item in guidance:
            st.write(f"• {item}")

        st.caption(
            "This is a basic educational screening and not a diagnosis."
        )


# ---------- Diet Planner ----------
elif page == "🍽️ Diet Planner":
    st.markdown("## 🍽️ Nouriva Diet Planner")
    st.write("Create a simple example day based on a general nutrition goal.")

    goal = st.selectbox(
        "Choose your general goal",
        [
            "Balanced nutrition",
            "Healthy weight gain",
            "Healthy weight management",
            "Athletic nutrition",
        ],
    )

    cultural = st.selectbox(
        "Food style",
        ["Flexible / mixed", "South Asian-inspired"],
    )

    plans = {
        "Balanced nutrition": [
            "🌅 Breakfast — Eggs + whole-grain roti/bread + fruit",
            "☀️ Snack — Yogurt + fruit",
            "🍛 Lunch — Lentils/chicken + rice/roti + vegetables",
            "🌇 Snack — Milk + nuts or fruit",
            "🌙 Dinner — Roti/rice + vegetables + a protein source",
        ],
        "Healthy weight gain": [
            "🌅 Breakfast — Eggs + milk + roti + banana",
            "☀️ Snack — Yogurt + nuts",
            "🍛 Lunch — Rice/roti + lentils + chicken + vegetables",
            "🌇 Snack — Milk + fruit",
            "🌙 Dinner — Roti + beans/meat + vegetables",
        ],
        "Healthy weight management": [
            "🌅 Breakfast — Eggs + whole-grain option + fruit",
            "☀️ Snack — Fruit or yogurt",
            "🍛 Lunch — Vegetables + lentils/chicken + moderate rice/roti",
            "🌇 Snack — Fruit + water",
            "🌙 Dinner — Vegetables + protein + suitable grain portion",
        ],
        "Athletic nutrition": [
            "🌅 Breakfast — Eggs + oats + milk + fruit",
            "☀️ Snack — Yogurt + nuts",
            "🍛 Lunch — Rice + chicken/fish + vegetables",
            "🌇 Snack — Banana + milk",
            "🌙 Dinner — Roti + lentils/meat + vegetables",
        ],
    }

    st.markdown("### 🥗 Example Day")

    for meal in plans[goal]:
        st.info(meal)

    if cultural == "South Asian-inspired":
        st.success(
            "Tip: common affordable options can include lentils, eggs, "
            "milk/yogurt, seasonal vegetables, fruit, rice and roti."
        )

    st.warning(
        "Meal plans shown here are examples for education. Individual "
        "medical, allergy, pregnancy, disease or therapeutic needs require "
        "professional dietary advice."
    )


# ---------- Nutrition Coach ----------
elif page == "🤖 Nutrition Coach":
    st.markdown("## 🤖 Nouriva Nutrition Coach")
    st.write(
        "Ask a general nutrition education question. This prototype "
        "uses a small educational knowledge base and does not claim "
        "to provide medical diagnosis."
    )

    question = st.text_input(
        "Ask Nouriva",
        placeholder="Example: Why is protein important?",
    )

    if question:
        q = question.lower()

        if "protein" in q:
            answer = EDUCATION["Protein"]["summary"]
        elif "hydration" in q or "water" in q:
            answer = EDUCATION["Hydration"]["summary"]
        elif "iron" in q:
            answer = EDUCATION["Iron Nutrition"]["summary"]
        elif "balanced" in q or "diet" in q:
            answer = EDUCATION["Balanced Diet"]["summary"]
        elif "food security" in q:
            answer = EDUCATION["Food Security"]["summary"]
        elif "undernutrition" in q or "malnutrition" in q:
            answer = EDUCATION["Undernutrition"]["summary"]
        elif "child" in q or "growth" in q:
            answer = EDUCATION["Child Nutrition"]["summary"]
        else:
            answer = (
                "I can currently explain topics such as balanced diets, "
                "protein, micronutrients, hydration, iron, food security, "
                "undernutrition, child nutrition and nutrition-related SDGs. "
                "Try asking about one of these."
            )

        st.success("🌿 Nouriva:")
        st.write(answer)

    st.divider()
    st.caption(
        "Prototype limitation: responses are educational and rule-based; "
        "a production AI assistant would require validated knowledge, "
        "safety controls and appropriate evaluation."
    )


# ---------- Education ----------
elif page == "📚 Nutrition Education":
    st.markdown("## 📚 Nouriva Nutrition Education Academy")
    st.write(
        "Explore structured lessons, practical takeaways and a knowledge "
        "check across core nutrition topics."
    )

    topic = st.selectbox(
        "Choose a topic",
        list(EDUCATION.keys()),
    )

    data = EDUCATION[topic]

    st.markdown(f"### 🌿 {topic}")
    st.info(data["summary"])

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### 🎯 Key Learning Points")
        for point in data["key"]:
            st.write(f"• {point}")

    with c2:
        st.markdown("#### 🧠 Quick Facts")
        for fact in data["facts"]:
            st.write(f"• {fact}")

    st.divider()

    st.markdown("### 🧠 Knowledge Check")

    q, options, correct = data["quiz"]

    answer = st.radio(
        q,
        options,
        key=f"quiz_{topic}",
    )

    if st.button("Check Answer", key=f"check_{topic}"):
        if answer == correct:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Not quite. The correct answer is: **{correct}**")

    st.divider()
    st.caption(
        "Educational content is simplified for a prototype and should "
        "not replace formal nutrition education or professional advice."
    )


# ---------- Insights ----------
elif page == "📊 Nutrition Insights":
    st.markdown("## 📊 Nutrition Insights")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Education Topics", len(EDUCATION))

    with c2:
        st.metric("Core Modules", 9)

    with c3:
        st.metric("Prototype Status", "Working")

    with c4:
        st.metric("Focus", "Nutrition + AI")

    st.divider()

    st.markdown("### 📈 What Nouriva Can Explore")

    insight_cols = st.columns(3)

    insights = [
        (
            "Undernutrition",
            "Awareness of inadequate energy or nutrient intake and the importance of early professional assessment.",
        ),
        (
            "Food Security",
            "Access, affordability, safety and nutritional quality all influence nutrition outcomes.",
        ),
        (
            "Prevention",
            "Education, dietary diversity and early awareness can support healthier decisions.",
        ),
    ]

    for i, (title, text) in enumerate(insights):
        with insight_cols[i]:
            st.markdown(
                f"""
                <div class="card">
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "Future versions can connect validated public datasets to create "
        "real interactive nutrition indicators and trend visualizations."
    )


# ---------- Growth Monitor ----------
elif page == "🧒 Growth Monitor":
    st.markdown("## 🧒 Growth Monitor")
    st.write(
        "Prototype demonstration of how a growth-monitoring interface "
        "could collect basic measurements."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        child_age = st.number_input(
            "Age (years)",
            0.0,
            19.0,
            5.0,
            step=0.1,
        )

    with c2:
        child_height = st.number_input(
            "Height (cm)",
            30.0,
            220.0,
            105.0,
        )

    with c3:
        child_weight = st.number_input(
            "Weight (kg)",
            1.0,
            150.0,
            20.0,
        )

    child_bmi = bmi_value(child_height, child_weight)

    st.metric("Calculated BMI", child_bmi)

    st.warning(
        "BMI alone cannot determine whether a child is growing normally. "
        "Clinical growth assessment requires age- and sex-specific validated "
        "growth references."
    )

    st.write(
        "A production version could plot height-for-age, weight-for-age "
        "and BMI-for-age against validated reference standards."
    )


# ---------- Food Scanner ----------
elif page == "📷 Food Scanner":
    st.markdown("## 📷 Nouriva Food Scanner")
    st.write(
        "Upload a food image to demonstrate the future computer-vision "
        "workflow."
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

        st.success(
            "Image received successfully. The current prototype does not "
            "claim to identify food or calculate nutrients automatically."
        )

        st.markdown("### 🔬 Future AI Pipeline")
        st.write("1. Image quality check")
        st.write("2. Food recognition")
        st.write("3. Portion estimation")
        st.write("4. Nutrient database matching")
        st.write("5. Uncertainty and safety checks")

    else:
        st.info("Upload a food image to test the interface.")


# ---------- Global Nutrition ----------
elif page == "🌍 Global Nutrition":
    st.markdown("## 🌍 Global Nutrition")
    st.write(
        "Nouriva connects nutrition awareness with major global development "
        "challenges."
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            """
            <div class="card">
                <h3>🎯 SDG 2 — Zero Hunger</h3>
                <p>
                Focuses on ending hunger, improving food security and
                promoting sustainable agriculture.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="card">
                <h3>❤️ SDG 3 — Good Health & Well-being</h3>
                <p>
                Nutrition is closely connected with health, growth,
                development and disease prevention.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🌱 Why It Matters")

    for item in [
        "Undernutrition can affect growth, development and health.",
        "Food insecurity can influence dietary quality and access.",
        "Nutrition education can improve awareness and informed choices.",
        "Digital tools may expand access to basic educational resources.",
    ]:
        st.write(f"• {item}")

    st.info(
        "Future versions can integrate trusted global datasets from "
        "organizations such as WHO, UNICEF and FAO."
    )


# ---------- Health Report ----------
elif page == "📄 Health Report":
    st.markdown("## 📄 Health Report")

    if "last_screening" not in st.session_state:
        st.info(
            "Complete a Nutrition Scan first. Your latest screening "
            "summary will appear here."
        )
    else:
        r = st.session_state["last_screening"]

        report = f"""
NOURIVA AI
Nutrition Screening & Education Prototype
-----------------------------------------

Screening date: {r['date']}

Basic information
Age: {r['age']} years
Sex: {r['sex']}
Height: {r['height']} cm
Weight: {r['weight']} kg

Preliminary screening
BMI: {r['bmi']}
BMI interpretation: {r['category']}
Risk score: {r['risk_score']}
Risk level: {r['risk_level']}

Diet and lifestyle
Meals per day: {r['meals']}
Protein sources: {", ".join(r['protein']) if r['protein'] else "None selected"}
Fruit/vegetable intake: {r['fruit_veg']}
Food access: {r['food_access']}

Important note
This report is an educational prototype output.
It does not diagnose disease and does not replace assessment
by a qualified healthcare professional.
"""

        st.text_area(
            "Report Preview",
            report,
            height=420,
        )

        st.download_button(
            "⬇️ Download Screening Report",
            data=report,
            file_name="Nouriva_AI_Screening_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ---------- About ----------
elif page == "ℹ️ About Nouriva":
    st.markdown("## ℹ️ About Nouriva AI")

    st.markdown(
        """
        ### 🌿 Nouriva AI

        Nouriva AI is a student-built health-technology prototype focused on:

        - Nutrition awareness
        - Preliminary nutrition screening
        - Nutrition education
        - Accessible digital health tools
        - Global nutrition awareness

        ### 💡 Vision

        To create an accessible AI-assisted nutrition companion that helps
        people better understand nutrition and potential nutrition-related
        risks.

        ### 👨‍💻 Creator

        **Muhammad Ahsan Shahzad**

        BS Human Nutrition & Dietetics Student  
        Pakistan

        ### 🚀 Hackathon Prototype

        Nouriva AI demonstrates how digital tools can combine nutrition
        screening, education, planning and global nutrition awareness in
        one accessible interface.

        ### ⚠️ Important

        Nouriva AI is an educational prototype.

        It does **not** diagnose disease, replace healthcare professionals,
        or provide definitive medical advice.
        """
    )


# ---------- Footer ----------
st.markdown(
    """
    <div class="footer">
        🌿 <b>Nouriva AI</b> • Student Health-Technology Prototype<br>
        Nutrition • Education • Awareness
    </div>
    """,
    unsafe_allow_html=True,
)
