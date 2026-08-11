import streamlit as st
import pandas as pd
import io
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Nouriva AI", page_icon="🌿", layout="wide")

# ---------- PREMIUM THEME ----------
st.markdown("""
<style>
.stApp{
 background:radial-gradient(circle at 90% 0%,rgba(19,190,112,.16),transparent 28%),
 linear-gradient(135deg,#050706,#0b100d 55%,#13090c);color:#f6faf8;
}
.block-container{max-width:1400px;padding-top:2rem;padding-bottom:4rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#050706,#0c1912);border-right:1px solid #24342c}
[data-testid="stSidebar"] *{color:#f6faf8!important}
h1,h2,h3,h4,p,span,label,li{color:inherit}
.hero{padding:44px;border-radius:30px;background:linear-gradient(135deg,#092c1b,#07100c 65%,#25090e);border:1px solid rgba(24,210,123,.28);box-shadow:0 25px 80px #0008;margin-bottom:28px}
.eyebrow{color:#5ff0a8!important;font-size:12px;font-weight:900;letter-spacing:.18em}
.hero h1{font-size:clamp(40px,6vw,72px);margin:10px 0;font-weight:900}
.hero p{color:#c6d2cb!important;max-width:850px;font-size:18px;line-height:1.65}
.pill{display:inline-block;padding:7px 12px;border-radius:99px;background:#18c77a16;border:1px solid #18c77a44;color:#7af0b5!important;margin:5px;font-size:12px;font-weight:800}
.card,.metric,.panel{background:linear-gradient(145deg,#121916,#0c110f);border:1px solid #ffffff14;border-radius:22px;box-shadow:0 15px 45px #0005}
.card{padding:24px;min-height:150px}
.card:hover{border-color:#18c77a55;transform:translateY(-2px)}
.card p{color:#aebbb4!important;line-height:1.55}
.metric{padding:20px}.metric small{color:#8f9c96}.metric strong{display:block;font-size:30px;margin-top:5px}
.panel{padding:26px;margin:18px 0}
.good{background:linear-gradient(135deg,#0d2d1d,#0b1711);border:1px solid #18c77a66;border-left:5px solid #18c77a;border-radius:20px;padding:22px;margin:15px 0}
.warn{background:linear-gradient(135deg,#351017,#170b0e);border:1px solid #ff4d5f66;border-left:5px solid #ff4d5f;border-radius:20px;padding:22px;margin:15px 0}
.neutral{background:#101613;border:1px solid #ffffff16;border-left:5px solid #77837d;border-radius:20px;padding:22px;margin:15px 0}
.module{padding:28px;border-radius:25px;background:linear-gradient(135deg,#0e1713,#0b0f0d);border:1px solid #ffffff12;margin-bottom:22px}
.stButton>button,.stDownloadButton>button{background:linear-gradient(135deg,#15ad69,#087044)!important;color:#fff!important;border:1px solid #36e79a55!important;border-radius:13px!important;font-weight:800!important;min-height:46px}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:#62f0ae!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input,div[data-baseweb="select"]>div{background:#0e1411!important;color:#fff!important;border-color:#ffffff1f!important}
.stRadio label,.stCheckbox label,.stSelectbox label,.stMultiSelect label,.stNumberInput label,.stTextInput label,.stFileUploader label{color:#d8e2dc!important}
[data-testid="stMetricValue"],[data-testid="stMetricLabel"]{color:#fff!important}
.footer{text-align:center;color:#718078!important;padding:30px;border-top:1px solid #ffffff10;margin-top:50px}
</style>
""", unsafe_allow_html=True)

# ---------- STATE / NAVIGATION ----------
PAGES=["🏠 Dashboard","🔍 Nutrition Scan","🍽️ Diet Planner","🤖 Nutrition Coach","📚 Education",
       "📊 Nutrition Insights","🧒 Growth Monitor","📷 Food Scanner","🌍 Global Nutrition",
       "📄 Health Report","ℹ️ About Nouriva"]

for k,v in {"page":PAGES[0],"screening":None,"plan":None,"coach":[],"growth":None,"quiz":{}}.items():
    st.session_state.setdefault(k,v)

def nav(page):
    st.session_state.page=page

with st.sidebar:
    st.markdown("## 🌿 Nouriva AI")
    st.caption("Nutrition • Education • Awareness")
    st.divider()
    for i,p in enumerate(PAGES):
        st.button(p,key=f"nav_{i}",use_container_width=True,on_click=nav,args=(p,))
    st.divider()
    st.markdown("**NOURIVA**")
    st.caption("Student Health-Technology Prototype • 2026")

# ---------- HELPERS ----------
def calc_bmi(h,w):
    return round(w/((h/100)**2),1) if h else 0

def adult_cat(b):
    if b<18.5:return "Below standard adult BMI range"
    if b<25:return "Standard adult BMI range"
    if b<30:return "Above standard adult BMI range"
    return "High adult BMI range"

def risk(age,b,meals,protein,fruit,access):
    score=0; factors=[]
    if age>=18 and b<18.5: score+=2; factors.append("BMI is below the standard adult screening range.")
    if age>=18 and b>=30: score+=1; factors.append("BMI is in a high adult screening range.")
    if meals<=2: score+=1; factors.append("Reported meal frequency is low.")
    if not protein: score+=1; factors.append("No protein source was selected.")
    if fruit=="Rarely": score+=1; factors.append("Fruit and vegetable intake was reported as rare.")
    if access=="Often difficult": score+=2; factors.append("Food access was reported as often difficult.")
    elif access=="Sometimes difficult": score+=1; factors.append("Food access was reported as sometimes difficult.")
    level="Higher potential risk factors" if score>=5 else "Several potential risk factors" if score>=3 else "Some potential nutrition-risk factors" if score else "Few identified risk factors"
    return score,level,factors

EDU={
"Balanced Diet":("A balanced eating pattern provides a variety of foods and nutrients.",["Include different food groups.","Include suitable protein sources.","Eat fruits and vegetables regularly.","Include appropriate fluids."],"Which approach best describes a balanced diet?",["Only one food group","A variety of foods providing different nutrients","No carbohydrates","Water instead of food"],1),
"Protein":("Protein provides amino acids used for tissue maintenance, repair and many body functions.",["Sources include pulses, eggs, dairy, fish, meat, nuts and seeds.","Needs vary by person.","Protein is one part of an overall balanced diet."],"Which nutrient is especially important for tissue growth and repair?",["Protein","Water only","Salt only","None"],0),
"Carbohydrates":("Carbohydrates are a major source of energy and occur in grains, fruits and legumes.",["Whole grains can provide fiber.","Carbohydrates can be part of a balanced diet.","Food quality and overall dietary pattern matter."],"Which food commonly provides carbohydrate?",["Rice","Plain salt","Water only","None"],0),
"Fats":("Dietary fats provide energy and support absorption of fat-soluble vitamins.",["Different fats have different effects.","Nuts, seeds and plant oils contain unsaturated fats.","Overall dietary pattern matters."],"Which is a food source of dietary fat?",["Nuts","Water","Salt only","None"],0),
"Micronutrients":("Vitamins and minerals are required in smaller amounts but support essential functions.",["Iron contributes to hemoglobin formation.","Calcium supports bones and teeth.","Different micronutrients have different roles."],"Iron is particularly important for:",["Hemoglobin formation","Making water","Replacing protein","None"],0),
"Hydration":("Fluids support normal physiological functions and needs vary with context.",["Water is essential.","Activity and hot environments can increase fluid losses.","Foods can contribute to total fluid intake."],"Which substance is essential for normal hydration?",["Water","Salt only","Protein only","None"],0),
"Fiber":("Dietary fiber is mainly found in plant foods and supports digestive health.",["Pulses are useful sources.","Fruits and vegetables contain fiber.","Whole grains can provide fiber."],"Which is a common source of dietary fiber?",["Pulses","Only salt","Only water","None"],0),
"Food Safety":("Food safety practices help reduce exposure to foodborne hazards.",["Wash hands and surfaces.","Separate raw and cooked foods.","Cook appropriately.","Store food safely."],"Which practice helps reduce contamination?",["Separating raw and cooked foods","Using dirty utensils","Leaving cooked food out for days","None"],0),
"Food Security":("Food security concerns reliable access to sufficient, safe and nutritious food.",["Availability matters.","Access and affordability matter.","Utilization and safety matter.","Stability over time matters."],"Food security is mainly concerned with:",["Reliable access to sufficient safe and nutritious food","Only restaurants","Only calories","None"],0),
"Undernutrition":("Undernutrition can occur when energy or nutrient needs are not adequately met.",["It can affect growth and health.","Children require age-specific assessment.","Illness and food insecurity can contribute.","Assessment should use appropriate methods."],"Child growth assessment should consider:",["Age- and sex-specific references","Adult BMI only","Height alone","None"],0),
"Healthy Weight":("Weight-related health is influenced by nutrition, activity, genetics, health and context.",["Weight alone does not define health.","Adult BMI is a screening measure.","Children require growth references."],"BMI in adults is best described as:",["A screening measure","A complete diagnosis","A blood test","An allergy test"],0),
"Life-Course Nutrition":("Nutrition needs and assessment approaches change across life stages.",["Children need growth-focused assessment.","Adults have different screening considerations.","Older adults may have changing needs.","Some life stages require specialized guidance."],"Do nutrition needs remain exactly the same throughout life?",["No","Yes, always","Only children","Only athletes"],0)
}
GLOBAL={
"Undernutrition":("Undernutrition includes conditions associated with inadequate energy or nutrient intake.","It can affect growth, development and health and is influenced by diet, illness and social conditions.","SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being"),
"Food Security":("Food security involves reliable access to sufficient, safe and nutritious food.","Affordability, availability, utilization and stability can influence food security.","SDG 2 • Zero Hunger | SDG 1 • No Poverty"),
"Micronutrient Deficiencies":("Micronutrient deficiencies occur when essential vitamins or minerals are not adequately available or absorbed.","They can affect blood formation, immunity, growth and development.","SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being"),
"Child Malnutrition":("Child nutrition assessment requires appropriate measures of growth and nutritional status.","Early identification of concerns can support appropriate referral and intervention.","SDG 2 • Zero Hunger | SDG 3 • Good Health and Well-Being"),
"Sustainable Nutrition":("Sustainable nutrition considers health, food systems, resources and environmental effects.","Food choices and food systems influence human health and sustainability.","SDG 2 • Zero Hunger | SDG 12 • Responsible Consumption and Production")
}
COACH={
"protein":"Protein provides amino acids used for tissue maintenance, repair and many body functions.",
"hydration":"Water and other suitable fluids support normal body functions. Needs vary with age, activity, climate and health.",
"iron":"Iron is important for hemoglobin formation and oxygen transport.",
"calcium":"Calcium supports bones and teeth and participates in muscle and nerve function.",
"fiber":"Dietary fiber is mainly found in plant foods and supports digestive health.",
"bmi":"BMI is calculated from height and weight. In adults it can be a screening measure, but it does not diagnose health.",
"food safety":"Food safety includes clean hands and surfaces, separation of raw/cooked foods, appropriate cooking and safe storage.",
"balanced":"A balanced eating pattern includes variety, appropriate energy, protein, micronutrients, fiber and fluids.",
"malnutrition":"Malnutrition is a broad term including undernutrition and other forms of nutrition imbalance."
}
def coach_answer(q):
    q=q.lower()
    for k,v in COACH.items():
        if k in q:return v
    return "I can explain protein, hydration, iron, calcium, fiber, BMI, food safety, balanced diets and malnutrition. Personal medical concerns should be discussed with a qualified professional."

def meal_plan(goal,veg,budget):
    p="dal / beans / chickpeas / eggs / yogurt" if veg else "dal / eggs / chicken / fish / yogurt"
    if goal=="Healthy weight gain":
        x=[("Breakfast","Eggs + roti/paratha + milk + banana"),("Snack","Yogurt + fruit + nuts/seeds"),("Lunch",f"Rice/roti + {p} + vegetables"),("Snack","Milk + banana or fruit"),("Dinner",f"Roti/rice + {p} + vegetables + yogurt")]
    elif goal=="Athletic nutrition":
        x=[("Breakfast","Eggs + oats/roti + milk + fruit"),("Pre/Post activity","Banana + yogurt or milk"),("Lunch",f"Rice/roti + {p} + vegetables"),("Snack","Fruit + yogurt + nuts/seeds"),("Dinner",f"Rice/roti + {p} + vegetables")]
    else:
        x=[("Breakfast","Eggs/yogurt + roti + fruit"),("Snack","Fruit + yogurt"),("Lunch",f"Rice/roti + {p} + vegetables"),("Snack","Milk + fruit"),("Dinner",f"Roti/rice + {p} + vegetables")]
    if budget:x=[(a,b.replace("nuts/seeds","roasted chickpeas")) for a,b in x]
    return x

# ---------- TOP ----------
a,b=st.columns([5,1])
with a: st.markdown('<div class="eyebrow">NOURIVA • 2026</div>',unsafe_allow_html=True)
with b: st.button("⌂ Home",key="home",use_container_width=True,on_click=nav,args=(PAGES[0],))

# ---------- DASHBOARD ----------
if st.session_state.page==PAGES[0]:
    st.markdown("""<div class="hero"><div class="eyebrow">STUDENT HEALTH-TECHNOLOGY PROTOTYPE</div><h1>🌿 Nouriva AI</h1><p><b>AI-Assisted Nutrition Screening & Education</b></p><p>Nutrition awareness, preliminary screening, education, meal planning and global nutrition learning — brought together in one premium student-built platform.</p><span class="pill">9 CORE MODULES</span><span class="pill">12+ EDUCATION TOPICS</span><span class="pill">INTERACTIVE</span><span class="pill">SDG-AWARE</span></div>""",unsafe_allow_html=True)
    st.markdown("## Your Nutrition Hub")
    st.caption("Choose a module to start. Cards open directly.")
    mods=[("🔍","Nutrition Scan","BMI + preliminary nutrition indicators.",1),("🍽️","Diet Planner","Example meal plans around a general goal.",2),("🤖","Nutrition Coach","General nutrition education assistant.",3),("📚","Education","Lessons, key points and quizzes.",4),("📊","Insights","Charts, indicators and SDG connections.",5),("🧒","Growth Monitor","Growth-assessment concepts.",6),("📷","Food Scanner","Image upload and workflow.",7),("🌍","Global Nutrition","Major global nutrition challenges.",8),("📄","Health Report","Downloadable educational summary.",9)]
    cols=st.columns(3)
    for i,(ic,title,desc,n) in enumerate(mods):
        with cols[i%3]:
            st.markdown(f'<div class="card"><div style="font-size:32px">{ic}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
            st.button(f"Open {title}",key=f"open_{n}",use_container_width=True,on_click=nav,args=(PAGES[n],))
    st.divider()
    cols=st.columns(4)
    for c,v,l in zip(cols,["9","12+","5","LIVE"],["Core modules","Education topics","SDG connections","Prototype status"]):
        with c: st.markdown(f'<div class="metric"><small>{l}</small><strong>{v}</strong></div>',unsafe_allow_html=True)
    st.markdown('<div class="good"><b>🌱 Purpose</b><br>Nouriva AI demonstrates how accessible digital tools can support nutrition awareness, preliminary screening and education. It is an educational prototype, not a diagnostic medical system.</div>',unsafe_allow_html=True)

# ---------- SCAN ----------
elif st.session_state.page==PAGES[1]:
    st.markdown('<div class="module"><div class="eyebrow">SCREENING MODULE</div><h1>🔍 Nutrition Scan</h1><p>Calculate BMI and explore basic nutrition-related indicators.</p></div>',unsafe_allow_html=True)
    with st.form("scan"):
        c1,c2=st.columns(2)
        with c1:
            age=st.number_input("Age (years)",1,120,20); sex=st.selectbox("Sex",["Male","Female"]); meals=st.selectbox("Meals per day",[1,2,3,4,5],index=2)
        with c2:
            h=st.number_input("Height (cm)",30.,250.,170.); w=st.number_input("Weight (kg)",1.,300.,55.); fruit=st.selectbox("Fruit & vegetable intake",["Rarely","Sometimes","Daily"])
        protein=st.multiselect("Common protein sources",["Eggs","Milk / Dairy","Pulses / Lentils","Fish","Chicken / Meat","Nuts / Seeds"])
        access=st.selectbox("Access to sufficient food",["Usually sufficient","Sometimes difficult","Often difficult"])
        submit=st.form_submit_button("🔍 Analyze My Nutrition",use_container_width=True)
    if submit:
        b=calc_bmi(h,w); s,l,f=risk(age,b,meals,protein,fruit,access)
        st.session_state.screening={"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"age":age,"sex":sex,"height":h,"weight":w,"bmi":b,"meals":meals,"protein":protein,"fruit":fruit,"access":access,"score":s,"level":l,"factors":f}
    if st.session_state.screening:
        x=st.session_state.screening; st.markdown("## 📊 Screening Result")
        c1,c2,c3=st.columns(3)
        for c,label,val in [(c1,"BMI",x["bmi"]),(c2,"Risk score",x["score"]),(c3,"Result",x["level"])]:
            with c: st.markdown(f'<div class="metric"><small>{label}</small><strong style="font-size:22px">{val}</strong></div>',unsafe_allow_html=True)
        if x["age"]>=18:
            cat=adult_cat(x["bmi"])
            st.markdown(f'<div class="{"warn" if x["bmi"]<18.5 or x["bmi"]>=30 else "good"}"><b>{cat}</b><br>Adult BMI screening interpretation.</div>',unsafe_allow_html=True)
        else: st.markdown('<div class="neutral"><b>Age-specific interpretation</b><br>For people under 18, BMI should be interpreted using validated age- and sex-specific growth references.</div>',unsafe_allow_html=True)
        st.markdown("### 🌱 Identified Factors")
        if x["factors"]:
            for f in x["factors"]: st.write("•",f)
        else: st.success("No basic risk indicators were identified.")
        st.markdown("### 💡 General Educational Guidance")
        for t in ["Aim for a varied and balanced eating pattern.","Include appropriate protein sources regularly.","Include fruits and vegetables regularly.","Maintain appropriate fluid intake.","Seek professional advice for persistent health or nutrition concerns."]: st.write("•",t)
        st.caption("BMI and the prototype risk score are screening/educational tools, not diagnoses or validated clinical risk scores.")

# ---------- DIET ----------
elif st.session_state.page==PAGES[2]:
    st.markdown('<div class="module"><div class="eyebrow">PLANNING MODULE</div><h1>🍽️ Diet Planner</h1><p>Create practical example meals around a general goal.</p></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: goal=st.selectbox("General goal",["Balanced nutrition","Healthy weight gain","Healthy weight management","Athletic nutrition"])
    with c2: veg=st.checkbox("Vegetarian pattern"); budget=st.checkbox("Budget-friendly substitutions")
    if st.button("🍽️ Generate My Example Plan",use_container_width=True):
        st.session_state.plan=meal_plan(goal,veg,budget)
    if st.session_state.plan:
        st.markdown('<div class="good"><b>Plan generated successfully.</b><br>Educational example based on your selected goal.</div>',unsafe_allow_html=True)
        cols=st.columns(2)
        for i,(name,food) in enumerate(st.session_state.plan):
            with cols[i%2]: st.markdown(f'<div class="card"><div class="eyebrow">{name}</div><h3>🥗 {food}</h3></div>',unsafe_allow_html=True)
        st.markdown('<div class="neutral">These are example meal ideas, not individualized medical diets. Allergies, conditions and energy requirements require professional assessment.</div>',unsafe_allow_html=True)

# ---------- COACH ----------
elif st.session_state.page==PAGES[3]:
    st.markdown('<div class="module"><div class="eyebrow">EDUCATION ASSISTANT</div><h1>🤖 Nutrition Coach</h1><p>Ask a general nutrition education question.</p></div>',unsafe_allow_html=True)
    st.caption("Try: protein • iron • hydration • BMI • fiber • calcium • food safety • balanced diet")
    q=st.text_input("Your question",placeholder="Why is protein important?")
    if st.button("🤖 Ask Nouriva",use_container_width=True) and q.strip(): st.session_state.coach.append((q,coach_answer(q)))
    for q,a in reversed(st.session_state.coach[-8:]):
        st.markdown(f'<div class="panel"><b>YOU</b><br>{q}<br><br><b style="color:#5ff0a8">🌿 NOURIVA COACH</b><br>{a}</div>',unsafe_allow_html=True)

# ---------- EDUCATION ----------
elif st.session_state.page==PAGES[4]:
    st.markdown('<div class="module"><div class="eyebrow">LEARNING CENTER</div><h1>📚 Nutrition Education</h1><p>Structured lessons, key points and knowledge checks.</p></div>',unsafe_allow_html=True)
    topic=st.selectbox("Choose a topic",list(EDU))
    overview,points,q,opts,ans=EDU[topic]
    st.markdown(f'<div class="good"><b>{topic}</b><br>{overview}</div>',unsafe_allow_html=True)
    st.markdown("### 📌 Key Points")
    cols=st.columns(2)
    for i,p in enumerate(points):
        with cols[i%2]: st.markdown(f'<div class="card"><b>0{i+1}</b><p>{p}</p></div>',unsafe_allow_html=True)
    st.divider(); st.markdown("### 🧠 Knowledge Check")
    selected=st.radio(q,opts,key=f"quiz_{topic}")
    if st.button("Check Answer",use_container_width=True):
        ok=opts.index(selected)==ans; st.session_state.quiz[topic]=ok
        if ok: st.success("✅ Correct — excellent.")
        else: st.error(f"❌ Not quite. Correct answer: {opts[ans]}")
    if topic in st.session_state.quiz: st.metric("Latest result","1 / 1" if st.session_state.quiz[topic] else "0 / 1")

# ---------- INSIGHTS ----------
elif st.session_state.page==PAGES[5]:
    st.markdown('<div class="module"><div class="eyebrow">DATA & AWARENESS</div><h1>📊 Nutrition Insights</h1><p>Explore indicators, charts and SDG connections.</p></div>',unsafe_allow_html=True)
    choice=st.selectbox("Choose an insight",["Adult BMI screening concepts","Prototype risk weights","SDG connections"])
    if choice=="Adult BMI screening concepts":
        df=pd.DataFrame({"Category":["Below 18.5","18.5–24.9","25–29.9","30+"],"Reference":[18.5,24.9,29.9,30]}).set_index("Category"); st.bar_chart(df); st.info("Adult BMI categories are screening concepts, not a complete health diagnosis.")
    elif choice=="Prototype risk weights":
        df=pd.DataFrame({"Indicator":["Low meals","No protein","Rare fruit/veg","Some access difficulty","Often difficult access"],"Points":[1,1,1,1,2]}).set_index("Indicator"); st.bar_chart(df); st.info("These weights are prototype values, not a validated clinical score.")
    else:
        df=pd.DataFrame({"SDG":["SDG 2","SDG 3","SDG 4","SDG 12","SDG 1"],"Connection":[5,5,4,3,2]}).set_index("SDG"); st.bar_chart(df); st.success("Nouriva connects nutrition awareness with Zero Hunger, Good Health, Quality Education, sustainability and poverty reduction.")

# ---------- GROWTH ----------
elif st.session_state.page==PAGES[6]:
    st.markdown('<div class="module"><div class="eyebrow">GROWTH AWARENESS</div><h1>🧒 Growth Monitor</h1><p>Educational demonstration of measurements used in child growth assessment.</p></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: age=st.number_input("Child age (years)",.1,19.,10.); sex=st.selectbox("Sex",["Male","Female"],key="gsex")
    with c2: h=st.number_input("Height (cm)",30.,220.,140.); w=st.number_input("Weight (kg)",1.,150.,35.)
    if st.button("🧒 Assess Growth Information",use_container_width=True): st.session_state.growth={"age":age,"sex":sex,"height":h,"weight":w,"bmi":calc_bmi(h,w)}
    if st.session_state.growth:
        g=st.session_state.growth
        c1,c2,c3=st.columns(3); c1.metric("Age",f'{g["age"]:g} years'); c2.metric("Height",f'{g["height"]:g} cm'); c3.metric("BMI",g["bmi"])
        st.markdown('<div class="neutral"><b>ℹ️ Interpretation</b><br>BMI alone cannot determine whether a child is growing normally. Proper assessment requires validated age- and sex-specific growth references and professional interpretation.</div>',unsafe_allow_html=True)

# ---------- FOOD SCANNER ----------
elif st.session_state.page==PAGES[7]:
    st.markdown('<div class="module"><div class="eyebrow">IMAGE WORKFLOW</div><h1>📷 Food Scanner</h1><p>Upload an image to demonstrate Nouriva’s food-analysis workflow.</p></div>',unsafe_allow_html=True)
    up=st.file_uploader("Upload a food image",type=["jpg","jpeg","png","webp"])
    if up:
        raw=up.getvalue(); im=Image.open(io.BytesIO(raw)); st.image(im,caption="Uploaded food image",use_container_width=True)
        c1,c2,c3=st.columns(3); c1.metric("Width",f"{im.width}px"); c2.metric("Height",f"{im.height}px"); c3.metric("Size",f"{len(raw)/1024:.1f} KB")
        st.markdown('<div class="good"><b>✓ Image received successfully</b><br>This prototype receives and inspects the image. Reliable food recognition and nutrient estimation would require a trained model and validated database.</div>',unsafe_allow_html=True)

# ---------- GLOBAL ----------
elif st.session_state.page==PAGES[8]:
    st.markdown('<div class="module"><div class="eyebrow">GLOBAL AWARENESS</div><h1>🌍 Global Nutrition</h1><p>Explore major nutrition challenges and development connections.</p></div>',unsafe_allow_html=True)
    t=st.selectbox("Choose a topic",list(GLOBAL)); desc,impact,sdgs=GLOBAL[t]
    st.markdown(f'<div class="good"><b>{t}</b><br>{desc}</div>',unsafe_allow_html=True)
    st.markdown("### 🌎 Why this matters"); st.write(impact)
    st.markdown("### 🎯 SDG Connection"); st.success(sdgs)

# ---------- REPORT ----------
elif st.session_state.page==PAGES[9]:
    st.markdown('<div class="module"><div class="eyebrow">DOCUMENT CENTER</div><h1>📄 Health Report</h1><p>Generate an educational summary from the latest screening.</p></div>',unsafe_allow_html=True)
    if not st.session_state.screening:
        st.markdown('<div class="neutral"><b>No screening available.</b><br>Complete Nutrition Scan first.</div>',unsafe_allow_html=True)
        st.button("Open Nutrition Scan",use_container_width=True,on_click=nav,args=(PAGES[1],))
    else:
        x=st.session_state.screening
        report=f"""NOURIVA AI
NUTRITION SCREENING & EDUCATION REPORT
Generated: {x["date"]}

PERSON
Age: {x["age"]}
Sex: {x["sex"]}
Height: {x["height"]} cm
Weight: {x["weight"]} kg

SCREENING
BMI: {x["bmi"]}
BMI interpretation: {adult_cat(x["bmi"]) if x["age"]>=18 else "Age-specific interpretation required"}
Meals per day: {x["meals"]}
Protein sources: {", ".join(x["protein"]) if x["protein"] else "None listed"}
Fruit & vegetables: {x["fruit"]}
Food access: {x["access"]}

PRELIMINARY PROTOTYPE
Risk score: {x["score"]}
Result: {x["level"]}
Factors:
{chr(10).join("- "+z for z in x["factors"]) if x["factors"] else "- None identified"}

GUIDANCE
- Aim for a varied and balanced eating pattern.
- Include appropriate protein sources.
- Include fruits and vegetables regularly.
- Maintain appropriate fluid intake.
- Seek professional advice for persistent concerns.

DISCLAIMER
Educational prototype only. Not a diagnosis or validated clinical risk assessment.
"""
        st.text_area("Report preview",report,height=450)
        st.download_button("⬇️ Download Nouriva Report",report,"Nouriva_AI_Nutrition_Report.txt","text/plain",use_container_width=True)

# ---------- ABOUT ----------
else:
    st.markdown('<div class="module"><div class="eyebrow">THE PROJECT</div><h1>ℹ️ About Nouriva AI</h1><p>A student-built nutrition and health-technology prototype.</p></div>',unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1: st.markdown('<div class="card"><h3>🌿 Mission</h3><p>Make nutrition awareness easier to explore through screening, education, planning and accessible digital tools.</p></div>',unsafe_allow_html=True)
    with c2: st.markdown('<div class="card"><h3>🚀 Scope</h3><p>Nouriva demonstrates interactive nutrition workflows while separating educational features from clinical diagnosis.</p></div>',unsafe_allow_html=True)
    st.markdown("### 👨‍💻 Creator"); st.write("**Muhammad Ahsan Shahzad**"); st.write("BS Human Nutrition & Dietetics Student • Pakistan")
    st.markdown("### 🌍 SDG alignment"); st.write("SDG 2 — Zero Hunger • SDG 3 — Good Health and Well-Being • SDG 4 — Quality Education • SDG 12 — Responsible Consumption and Production • SDG 1 — No Poverty")
    st.markdown('<div class="warn"><b>⚠️ Educational prototype</b><br>Nouriva AI does not diagnose disease, prescribe treatment or replace qualified healthcare professionals.</div>',unsafe_allow_html=True)

st.markdown('<div class="footer">🌿 <b>Nouriva AI</b> • Nutrition • Education • Awareness<br>Student Health-Technology Prototype • 2026<br>Educational prototype — not a diagnostic medical system.</div>',unsafe_allow_html=True)
