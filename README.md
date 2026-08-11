🌿 Nouriva AI

Nutrition • Education • Awareness

AI-Assisted Nutrition Screening & Education Platform

Nouriva AI is a student-built health-technology prototype designed to bring nutrition screening, nutrition education, meal planning, growth-awareness tools, food-image workflows and global nutrition learning together in one accessible digital platform.

«Nouriva AI is an educational prototype. It does not diagnose disease, prescribe treatment, or replace qualified healthcare professionals.»

---

🚀 Overview

Nutrition problems can be influenced by dietary intake, food access, health conditions, socioeconomic factors, education and the wider food environment.

Nouriva AI explores how a digital platform could support early nutrition awareness and education through interactive tools.

The project combines practical nutrition concepts with a modern Streamlit-based interface.

---

✨ Core Features

🔍 Nutrition Scan

Provides a preliminary nutrition screening workflow using:

- Age
- Sex
- Height
- Weight
- BMI calculation
- Meal frequency
- Protein-source selection
- Fruit and vegetable intake
- Food-access indicators
- Prototype nutrition-risk scoring
- Educational guidance

The tool distinguishes adult BMI screening from the need for age- and sex-specific assessment in children.

---

🍽️ Diet Planner

Generates example daily meal plans according to a general goal.

Available goals include:

- Balanced nutrition
- Healthy weight gain
- Healthy weight management
- Athletic nutrition

Additional options include:

- Simple foods
- Budget-friendly choices
- Vegetarian planning
- Foods to flag for allergy review

The planner is intended for education and demonstration, not individualized medical diet prescription.

---

🤖 Nutrition Coach

Nouriva Coach provides basic nutrition education around topics such as:

- Protein
- Hydration
- Iron
- Calcium
- Vitamins
- Fiber
- Balanced diets
- BMI
- Malnutrition
- Food safety

The current implementation uses an educational knowledge base rather than claiming to be a clinical AI system.

---

📚 Nutrition Education

A structured learning section covering multiple nutrition topics.

Current areas include:

- Balanced Diet
- Protein
- Micronutrients
- Hydration
- Food Safety
- Fiber
- Food Security
- Undernutrition
- Healthy Weight
- Nutrition Across the Life Course

Each lesson includes:

- Topic overview
- Key learning points
- Knowledge-check question
- Multiple-choice answers
- Instant feedback
- Quiz result

---

📊 Nutrition Insights

Provides interactive educational visualizations covering:

- Adult BMI screening categories
- Prototype nutrition-risk factors
- Sustainable Development Goal connections

The charts are intended to demonstrate how nutrition information can be represented digitally.

«Prototype screening weights and charts are not validated clinical tools.»

---

🧒 Growth Monitor

Demonstrates the basic concept of child growth monitoring using:

- Age
- Sex
- Height
- Weight
- BMI calculation

The application explicitly explains that child growth cannot be interpreted using adult BMI categories alone.

A production system would require validated age- and sex-specific growth references and appropriate professional interpretation.

---

📷 Food Scanner

Allows users to upload:

- JPG
- JPEG
- PNG
- WEBP

The current prototype:

1. Receives the image.
2. Displays the uploaded image.
3. Processes the image file.
4. Reports image dimensions and file size.
5. Demonstrates the workflow for future food-recognition capabilities.

The current version does not falsely claim reliable food identification.

Future possibilities

A production version could integrate:

- Food recognition
- Portion estimation
- Nutrient estimation
- Food databases
- Meal analysis
- Dietary pattern analysis

---

🌍 Global Nutrition

Provides educational information about major global nutrition challenges, including:

- Undernutrition
- Food security
- Micronutrient deficiencies
- Child malnutrition
- Sustainable nutrition

The section connects nutrition challenges with relevant United Nations Sustainable Development Goals (SDGs).

Examples include:

- SDG 1 — No Poverty
- SDG 2 — Zero Hunger
- SDG 3 — Good Health and Well-Being
- SDG 4 — Quality Education
- SDG 12 — Responsible Consumption and Production

---

📄 Health Report

After completing a Nutrition Scan, Nouriva can generate an educational screening report containing:

- Date and time
- Basic measurements
- BMI
- BMI screening interpretation
- Dietary information
- Food-access information
- Prototype risk score
- Identified screening factors
- General educational guidance
- Disclaimer

The report can be downloaded as a ".txt" file.

---

🏠 Dashboard

The dashboard provides access to Nouriva's major tools from a central navigation system.

Core modules

Module| Purpose
🔍 Nutrition Scan| Preliminary screening
🍽️ Diet Planner| Example meal planning
🤖 Nutrition Coach| Nutrition education
📚 Education| Structured learning
📊 Insights| Nutrition indicators
🧒 Growth Monitor| Growth-awareness concepts
📷 Food Scanner| Image workflow
🌍 Global Nutrition| Global nutrition education
📄 Health Report| Downloadable report

---

🧠 Technology

Nouriva AI is currently built using Python and Streamlit.

Main technologies

- Python
- Streamlit
- Pandas
- Matplotlib
- Pillow

Streamlit provides the interactive web-app framework used by the project.

---

📁 Project Structure

nouriva-ai/
│
├── app.py
├── requirements.txt
├── README.md
└── .devcontainer/
    └── devcontainer.json

The main application is contained in:

app.py

---

⚙️ Installation

Clone the repository:

git clone https://github.com/mahsanshahzad1414-create/nouriva-ai.git

Enter the project directory:

cd nouriva-ai

Install the dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

The application will then open in the browser through Streamlit.

---

📦 Requirements

The current application uses:

streamlit
pandas
matplotlib
pillow

---

🔬 Project Status

Current status: Working Student Prototype

Nouriva AI currently demonstrates functional interactive workflows rather than a production clinical system.

Working components

- ✅ Dashboard
- ✅ Navigation
- ✅ BMI calculation
- ✅ Preliminary nutrition-risk screening
- ✅ Dietary assessment
- ✅ Example meal planning
- ✅ Nutrition education
- ✅ Knowledge checks
- ✅ Nutrition Coach knowledge base
- ✅ Nutrition insights
- ✅ Charts
- ✅ Growth-monitoring demonstration
- ✅ Food-image upload workflow
- ✅ Global nutrition education
- ✅ SDG connections
- ✅ Educational report generation
- ✅ Downloadable report
- ✅ Responsive Streamlit interface

---

🚧 Current Limitations

Nouriva AI is not a clinical nutrition application.

The current prototype does not provide:

- Clinical diagnosis
- Medical treatment
- Prescription diets
- Validated disease prediction
- Laboratory interpretation
- Clinical decision-making
- Reliable automated food recognition
- Clinical child-growth classification
- Professional medical recommendations

The nutrition-risk score is a prototype educational scoring mechanism, not a validated clinical assessment.

---

🔮 Future Development

Nouriva AI could eventually evolve into a more advanced nutrition platform with:

🤖 AI Nutrition Assistant

A production AI assistant could provide evidence-based nutrition education using a curated knowledge base and appropriate safety controls.

📷 Computer Vision Food Analysis

Potential future capabilities:

- Food recognition
- Portion estimation
- Nutrient estimation
- Meal composition analysis

📈 Advanced Nutrition Analytics

Future versions could include:

- Longitudinal nutrition tracking
- Dietary pattern analysis
- Interactive dashboards
- Personalized educational insights

🧒 Growth Assessment

A future growth module could integrate validated:

- Height-for-age references
- Weight-for-age references
- BMI-for-age references
- Growth trajectories

with appropriate age- and sex-specific interpretation.

🌍 Global Nutrition Data

Future versions could connect to reliable public datasets to provide:

- Global nutrition indicators
- Country comparisons
- Food-security information
- Malnutrition trends
- SDG-related indicators

🌐 Multilingual Nutrition Education

Potential languages include:

- English
- Urdu
- Punjabi
- Arabic
- Chinese

---

🎯 Vision

The long-term vision of Nouriva AI is to explore how accessible technology, nutrition science and artificial intelligence can work together to improve nutrition awareness.

The goal is not to replace nutrition professionals.

The goal is to make reliable nutrition education and early awareness more accessible, understandable and engaging.

---

🌱 Why Nouriva AI?

Nouriva AI brings several nutrition-related concepts together instead of focusing on only one feature.

Nutrition Screening
        ↓
Nutrition Education
        ↓
Diet Planning
        ↓
Nutrition Awareness
        ↓
Growth Awareness
        ↓
Food Analysis Workflow
        ↓
Global Nutrition Learning

This creates a foundation for a future nutrition-focused digital health platform.

---

👨‍💻 Creator

Muhammad Ahsan Shahzad

BS Human Nutrition & Dietetics Student
Pakistan

Nouriva AI is developed as a student health-technology project combining nutrition education, digital technology and artificial intelligence concepts.

---

🏆 Project Context

Nouriva AI • 2026

Student Health-Technology Prototype

Focus

Nutrition • Education • Awareness

---

⚠️ Disclaimer

Nouriva AI is a student-built educational and technology prototype.

Information generated or displayed by the application is intended for general educational purposes.

It does not:

- Diagnose medical conditions
- Prescribe treatment
- Replace a registered dietitian
- Replace a doctor
- Replace professional nutritional assessment

Users with medical, nutritional, growth, eating, or food-access concerns should seek appropriate professional support.

---

🌿 Nouriva AI

Nutrition • Education • Awareness

Building technology for a more nutrition-aware future.
