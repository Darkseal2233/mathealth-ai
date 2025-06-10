import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="MatHealth AI", layout="centered")

st.title("👶 MatHealth AI - Pregnancy & Inherited Risk Checker")

# --- Section 1: Danger Symptom Checker ---
st.header("🔍 1. Danger Symptom Checker")

def pregnancy_triage(signs_present):
    """
    Triage pregnancy-related symptoms based on severity using a traffic-light system.
    
    Args:
        signs_present (list): List of symptoms/signs the patient is experiencing
        
    Returns:
        dict: Contains triage level, action recommendation, and relevant signs
    """
    
    # Define the red, orange, and yellow flag signs
    RED_FLAGS = {
        'Severe bleeding or fluid loss': [
            'Bright-red bleeding soaking ≥ 1 pad/hour',
            'Passage of clots or tissue',
            'Sudden gush of clear/blood-stained fluid + abdominal pain'
        ],
        'Severe pain': [
            '"Tearing" or continuous abdominal pain at any gestation',
            'Sharp one-sided pain with dizziness (possible ectopic)',
            'Severe back/abdominal pain in woman with previous C-section'
        ],
        'Hypertensive crises': [
            'Convulsion / fit (eclampsia)',
            'Severe headache plus blurred vision or flashing lights',
            'Severe epigastric / right-upper-quadrant pain'
        ],
        'Shock or sepsis signs': [
            'Fainting, cold sweats, very rapid pulse (>110 bpm)',
            'Fever ≥ 39 °C with rigors',
            'Hot abdomen & foul vaginal waters after membranes rupture'
        ],
        'Acute respiratory / cardiac': [
            'Sudden breathlessness at rest, chest pain, palpitations',
            'Cyanosis or oxygen sat < 94%'
        ],
        'Fetal emergency': [
            'No fetal movement after a formal kick-count shows <10 kicks in 2h (≥ 28wk)'
        ],
        'Severe dehydration / metabolic': [
            'Persistent vomiting >12h with no fluid retention, sunken eyes, reduced urine'
        ]
    }
    
    ORANGE_FLAGS = {
        'Moderate bleeding / leakage': [
            'Spotting or light bleeding persisting >2h',
            'Continuous watery leakage (PROM) without pain or fever'
        ],
        'Moderate hypertension clues': [
            'BP ≥ 140/90 mmHg (home or clinic) plus mild headache or new swelling of face/hands',
            'Sudden weight gain > 2 kg in a week'
        ],
        'Infection indicators': [
            'Fever 38-38.9 °C',
            'Burning urination, flank pain',
            'Offensive vaginal discharge (no abdominal tenderness)'
        ],
        'Preterm-labour warning': [
            'Regular tightenings q 10 min or less before 37 wk',
            'Pelvic pressure/back ache with mucus "show"'
        ],
        'Reduced but not absent fetal movement': [
            '<10 kicks in a 12-hour count or subjective "much less than usual"'
        ],
        'Persistent itching / cholestasis concern': [
            'Severe itching of palms/soles especially at night, dark urine'
        ],
        'Other moderate worries': [
            'New onset swelling only in ankles plus headache',
            'Mild-to-moderate abdominal pain lasting >1h'
        ]
    }
    
    YELLOW_FLAGS = {
        'Mild oedema / varicosities': [
            'Ankle swelling at day\'s end, improves overnight',
            'New varicose veins with discomfort'
        ],
        'Digestive': [
            'Heartburn unrelieved by antacids for ≥3 days',
            'Constipation >3 days despite diet measures'
        ],
        'Musculoskeletal': [
            'Persistent low-back pain manageable with rest/heat'
        ],
        'Anaemia clues': [
            'Tiredness/pallor without breathlessness',
            'Lab Hb 8-10 g/dL'
        ],
        'Mild vulvo-vaginal issues': [
            'Thick white discharge (likely candidiasis) without odour or pain'
        ],
        'Skin / neuropathic': [
            'Carpal-tunnel tingling, leg cramps'
        ]
    }
    
    # Check for red flags
    red_signs = []
    for category, symptoms in RED_FLAGS.items():
        for symptom in symptoms:
            if symptom in signs_present:
                red_signs.append(symptom)
    
    if red_signs:
        return {
            'triage_level': 'RED 🚨',
            'action': 'Go to hospital immediately (within 1 hour)',
            'signs': red_signs,
            'message': 'Life-threatening emergency - seek care NOW'
        }
    
    # Check for orange flags
    orange_signs = []
    for category, symptoms in ORANGE_FLAGS.items():
        for symptom in symptoms:
            if symptom in signs_present:
                orange_signs.append(symptom)
    
    if len(orange_signs) >= 2:
        return {
            'triage_level': 'RED 🚨',
            'action': 'Go to hospital immediately (within 1 hour) - multiple concerning symptoms',
            'signs': orange_signs,
            'message': 'Multiple urgent symptoms - treat as emergency'
        }
    elif orange_signs:
        return {
            'triage_level': 'ORANGE ⚠️',
            'action': 'Seek care within 24 hours',
            'signs': orange_signs,
            'message': 'Urgent but not immediately life-threatening'
        }
    
    # Check for yellow flags
    yellow_signs = []
    for category, symptoms in YELLOW_FLAGS.items():
        for symptom in symptoms:
            if symptom in signs_present:
                yellow_signs.append(symptom)
    
    if yellow_signs:
        return {
            'triage_level': 'YELLOW 🟡',
            'action': 'Schedule appointment within 7 days',
            'signs': yellow_signs,
            'message': 'Non-urgent but needs medical review'
        }
    
    # No flags found
    return {
        'triage_level': 'GREEN',
        'action': 'Continue routine antenatal care',
        'signs': [],
        'message': 'No danger signs detected'
    }


# Example usage:
if __name__ == "__main__":
    # Example symptoms
    symptoms = [
        'Severe headache plus blurred vision or flashing lights',
        'New onset swelling only in ankles plus headache'
    ]
    
    result = pregnancy_triage(symptoms)
    
    print("\nTriage Result:")
    print(f"Level: {result['triage_level']}")
    print(f"Action: {result['action']}")
    print(f"Signs: {', '.join(result['signs'])}")
    print(f"Message: {result['message']}")


# --- Section 2: Early Pregnancy Assessment ---
st.header("🌱 2. Early Pregnancy Stage Assessment")

st.markdown("Answer the following to check if early pregnancy symptoms are present.")

def pregnancy_symptom_checker():
    """
    A simplified early pregnancy symptom checker.
    Returns a summary and likelihood of pregnancy based on common symptoms.
    """

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

    responses = {}
    total_score = 0
    positive_symptoms = []

    print("🤰 Early Pregnancy Symptom Checker\n")
    print("Please answer with 'yes' or 'no':\n")

    for question, weight in questions.items():
        while True:
            response = input(f"- {question} ").strip().lower()
            if response in ['yes', 'no', 'y', 'n']:
                break
            print("Please respond with 'yes' or 'no'.")
        if response.startswith('y'):
            responses[question] = True
            total_score += weight
            positive_symptoms.append(question)
        else:
            responses[question] = False

    print("\n📝 Summary:")
    if positive_symptoms:
        print("You reported the following symptoms:")
        for symptom in positive_symptoms:
            print(f"- {symptom}")
    else:
        print("You did not report any symptoms.")

    # Determine likelihood
    if total_score >= 9:
        likelihood = "High"
    elif total_score >= 5:
        likelihood = "Moderate"
    else:
        likelihood = "Low"

    print(f"\n📊 Pregnancy likelihood: {likelihood}")

    print("\n📌 Recommendation:")
    if likelihood == "High":
        print("- Take a pregnancy test and consult your doctor.")
    elif likelihood == "Moderate":
        print("- Consider taking a test and monitor symptoms.")
    else:
        print("- Symptoms are not strongly suggestive of pregnancy, but retest if needed.")

    return {
        "score": total_score,
        "likelihood": likelihood,
        "symptoms": positive_symptoms
    }

# Run the function
if __name__ == "__main__":
    pregnancy_symptom_checker()
