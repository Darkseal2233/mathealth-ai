import streamlit as st
from datetime import datetime

st.set_page_config(page_title="MatHealth AI", layout="centered")

st.title("👶 MatHealth AI - Pregnancy & Inherited Risk Checker")

# --- Section 1: Danger Symptom Checker ---
st.header("🔍 1. Danger Symptom Checker")

# Symptom flag dictionaries (abbreviated here for brevity, use full definitions from your original code)
RED_FLAGS = {
    'Severe bleeding or fluid loss': [
        'Bright-red bleeding soaking ≥ 1 pad/hour',
        'Passage of clots or tissue',
        'Sudden gush of clear/blood-stained fluid + abdominal pain'
    ]
}
ORANGE_FLAGS = {
    'Moderate bleeding / leakage': [
        'Spotting or light bleeding persisting >2h',
        'Continuous watery leakage (PROM) without pain or fever'
    ]
}
YELLOW_FLAGS = {
    'Mild oedema / varicosities': [
        'Ankle swelling at day\'s end, improves overnight'
    ]
}

# Combine all symptoms into a single list
all_symptoms = []
for group in [RED_FLAGS, ORANGE_FLAGS, YELLOW_FLAGS]:
    for symptoms in group.values():
        all_symptoms.extend(symptoms)

# User selects present symptoms
selected_symptoms = st.multiselect("Select all symptoms you're experiencing:", all_symptoms)

def pregnancy_triage(signs_present):
    red_signs, orange_signs, yellow_signs = [], [], []

    for symptom in signs_present:
        if any(symptom in s for s in RED_FLAGS.values()):
            red_signs.append(symptom)
        elif any(symptom in s for s in ORANGE_FLAGS.values()):
            orange_signs.append(symptom)
        elif any(symptom in s for s in YELLOW_FLAGS.values()):
            yellow_signs.append(symptom)

    if red_signs:
        return "RED 🚨", red_signs, "Go to hospital immediately"
    elif len(orange_signs) >= 2:
        return "RED 🚨", orange_signs, "Multiple urgent symptoms – seek emergency care"
    elif orange_signs:
        return "ORANGE ⚠️", orange_signs, "See a doctor within 24 hours"
    elif yellow_signs:
        return "YELLOW 🟡", yellow_signs, "Review within 7 days"
    else:
        return "GREEN ✅", [], "No danger signs detected"

if st.button("🩺 Analyze Symptoms"):
    level, signs, message = pregnancy_triage(selected_symptoms)
    st.subheader(f"Triage Level: {level}")
    st.markdown(f"**Action:** {message}")
    if signs:
        st.markdown("**Detected symptoms:**")
        for s in signs:
            st.markdown(f"- {s}")

# --- Section 2: Early Pregnancy Stage Assessment ---
st.header("🌱 2. Early Pregnancy Stage Assessment")

questions = {
    "Have you missed your period?": 3,
    "Do you feel nauseous or vomit especially in the morning?": 2,
    "Are your breasts sore or swollen?": 2,
    "Do you feel unusually tired?": 1,
    "Are you urinating more frequently?": 2,
    "Do you have unusual food cravings or aversions?": 1,
    "Are you experiencing mood swings?": 1,
    "Have you noticed light spotting or mild cramping?": 2
}

total_score = 0
positive_symptoms = []

with st.form("pregnancy_check"):
    for question, weight in questions.items():
        answer = st.checkbox(question)
        if answer:
            total_score += weight
            positive_symptoms.append(question)
    submitted = st.form_submit_button("Check Pregnancy Likelihood")

    if submitted:
        st.subheader("📊 Assessment Results")
        if total_score >= 9:
            likelihood = "High"
            color = "error"
        elif total_score >= 5:
            likelihood = "Moderate"
            color = "warning"
        else:
            likelihood = "Low"
            color = "success"

        getattr(st, color)(f"Pregnancy Likelihood: **{likelihood}**")

        if positive_symptoms:
            st.markdown("**Symptoms you selected:**")
            for symptom in positive_symptoms:
                st.markdown(f"- {symptom}")
        else:
            st.markdown("No symptoms selected.")

        st.markdown("📌 **Recommendation:**")
        if likelihood == "High":
            st.markdown("- Take a pregnancy test and consult your doctor.")
        elif likelihood == "Moderate":
            st.markdown("- Monitor symptoms and consider taking a test.")
        else:
            st.markdown("- Unlikely pregnancy. Recheck in a few days if needed.")


