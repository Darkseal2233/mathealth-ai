import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Page setup
st.set_page_config(page_title="MatHealth AI", layout="centered")

# Custom background
st.markdown("""
    <style>
    .main {
        background-color: #ffe6f0;
        padding: 20px;
        border-radius: 10px;
    }
    .stApp {
        background-color: #fff0f5;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar slide selector
slide = st.sidebar.selectbox(
    "Choose a section:",
    [
        "🔍 Danger Symptom Checker",
        "👣 Baby Kick Tracker",
        "🧬 Inherited Risk Predictor",
        "🌱 Early Pregnancy Assessment"
    ]
)

st.title("👶 MatHealth AI - Pregnancy & Inherited Risk Checker")

# --- Section 1 ---
if slide == "🔍 Danger Symptom Checker":
    st.header("🔍 1. Danger Symptom Checker")
    danger_symptoms = [
        "Severe abdominal pain", "Heavy bleeding", "Severe headache", "Blurred vision",
        "Swelling of hands/face", "High fever", "Reduced baby movements",
        "Painful urination", "Persistent vomiting"
    ]
    user_symptoms = st.multiselect("Select any symptoms you're currently experiencing:", danger_symptoms)
    if user_symptoms:
        st.error("⚠️ Please visit a healthcare center IMMEDIATELY.")
    else:
        st.success("✅ No urgent danger symptoms selected.")

# --- Section 2 ---
elif slide == "👣 Baby Kick Tracker":
    st.header("👣 2. Baby Kick Tracker")
    kick_times = st.text_area("Enter times the baby kicked today (comma-separated, e.g., 08:30, 14:45):")
    if kick_times:
        kicks = [time.strip() for time in kick_times.split(",") if time.strip()]
        st.info(f"You logged **{len(kicks)} kicks** today.")
        if len(kicks) < 10:
            st.warning("⚠️ Fewer than 10 kicks. Please consult your doctor.")
        else:
            st.success("✅ Normal baby activity.")

# --- Section 3 ---
elif slide == "🧬 Inherited Risk Predictor":
    st.header("🧬 3. Predict Inherited Conditions for Your Baby")
    st.markdown("Provide known health conditions in the family.")
    inherited_conditions = [
        "Diabetes", "Asthma", "Hypertension", "Epilepsy", "Sickle Cell",
        "Heart Disease", "Mental Health Disorders", "Glaucoma", "Hearing Loss"
    ]
    family_history = {
        "Mother": st.multiselect("Mother's Conditions:", inherited_conditions),
        "Father": st.multiselect("Father's Conditions:", inherited_conditions),
        "Maternal Grandparents": st.multiselect("Maternal Grandparents' Conditions:", inherited_conditions),
        "Paternal Grandparents": st.multiselect("Paternal Grandparents' Conditions:", inherited_conditions)
    }
    relation_weights = {
        "Mother": 0.4, "Father": 0.4,
        "Maternal Grandparents": 0.1, "Paternal Grandparents": 0.1
    }
    risk_map = {}
    for rel, conds in family_history.items():
        for cond in conds:
            risk_map[cond] = risk_map.get(cond, 0) + relation_weights[rel]
    predicted_risks = {cond: round(score * 100) for cond, score in risk_map.items() if score >= 0.2}
    if predicted_risks:
        fig, ax = plt.subplots()
        conditions = list(predicted_risks.keys())
        values = list(predicted_risks.values())
        bar_colors = ['red' if v > 60 else 'orange' if v > 40 else 'yellow' for v in values]
        bars = ax.barh(conditions, values, color=bar_colors)
        ax.set_xlabel("Risk (%)")
        ax.set_title("Predicted Risk of Inherited Conditions")
        ax.invert_yaxis()
        ax.bar_label(bars, fmt='%d%%')
        st.pyplot(fig)
        st.info("🧾 Review high-risk conditions with a medical professional.")
    else:
        st.success("✅ No major inherited risks detected.")

# --- Section 4 ---
elif slide == "🌱 Early Pregnancy Assessment":
    st.header("🌱 4. Early Pregnancy Stage Assessment")
    st.markdown("Answer the following to check for early pregnancy symptoms.")
    early_symptoms = {
        "Missed period": st.checkbox("Missed your period?"),
        "Nausea or vomiting": st.checkbox("Feeling nauseous or vomiting?"),
        "Tender or swollen breasts": st.checkbox("Tender or swollen breasts?"),
        "Frequent urination": st.checkbox("Need to urinate more often?"),
        "Fatigue": st.checkbox("Feeling unusually tired?"),
        "Mood swings": st.checkbox("Experiencing mood swings?"),
        "Food aversions or cravings": st.checkbox("Unusual food cravings or aversions?"),
        "Mild cramping or spotting": st.checkbox("Light cramping or spotting?")
    }
    count = sum(early_symptoms.values())
    if count >= 5:
        st.warning("⚠️ You may be in early pregnancy. Take a test and consult a doctor.")
    elif 2 <= count < 5:
        st.info("ℹ️ You have some symptoms. Monitor and consider a pregnancy test.")
    else:
        st.success("✅ No strong pregnancy indicators.")
