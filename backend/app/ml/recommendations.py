from typing import List, Dict, Any
from app.schemas.prediction import PatientInput, Recommendation

def generate_recommendations(data: PatientInput, analysis: Dict[str, Any]) -> List[Recommendation]:
    recommendations: List[Recommendation] = []
    risk_score = analysis.get("risk_score", 50)
    risk_level = analysis.get("risk_level", "Moderate Risk")
    
    # 1. Emergency / Clinical Alert if critical
    if risk_score >= 70 or analysis.get("urgency_level") == "emergency":
        recommendations.append(Recommendation(
            category="Urgent Clinical Action",
            title="Cardiology Consultation Recommended",
            description="Your analysis indicates multiple elevated clinical markers. Schedule an appointment with a cardiologist for an echocardiogram, stress test, and biomarker review.",
            urgency="immediate",
            icon="AlertTriangle"
        ))
    elif risk_score >= 40:
        recommendations.append(Recommendation(
            category="Medical Monitoring",
            title="Schedule Routine Lipid & Cardiac Panel",
            description="Book an annual checkup to track resting blood pressure, fasting lipid profile, and serum biomarkers with your primary physician.",
            urgency="high",
            icon="Stethoscope"
        ))

    # 2. Blood Pressure Advice
    sbp = data.systolic_bp or (150 if data.blood_pressure == "High" else 135 if data.blood_pressure == "Elevated" else 120)
    if sbp >= 135 or data.blood_pressure in ["Elevated", "High"]:
        recommendations.append(Recommendation(
            category="Dietary Strategy",
            title="Adopt DASH Diet & Reduce Sodium (<1,500 mg/day)",
            description="Elevated blood pressure benefits significantly from the Dietary Approaches to Stop Hypertension (DASH) protocol—rich in potassium, magnesium, whole grains, and leafy greens.",
            urgency="high",
            icon="Utensils"
        ))
        recommendations.append(Recommendation(
            category="Medical Monitoring",
            title="Daily Blood Pressure Logging",
            description="Monitor resting blood pressure twice daily (morning and evening) in a quiet seated position and log results for your healthcare provider.",
            urgency="moderate",
            icon="Activity"
        ))

    # 3. Smoking Advice
    smoke = (data.smoking or "Never").lower()
    if "regular" in smoke or smoke == "yes" or "occasion" in smoke:
        recommendations.append(Recommendation(
            category="Lifestyle Intervention",
            title="Smoking Cessation Program",
            description="Smoking is the most reversible major risk factor. Quitting reduces cardiac event probability by 50% within the first 12 months.",
            urgency="immediate" if "regular" in smoke else "high",
            icon="ShieldAlert"
        ))

    # 4. Physical Activity
    act = (data.physical_activity or "Moderate").lower()
    if act == "low" or data.exercise_days in ["0-1 days"]:
        recommendations.append(Recommendation(
            category="Physical Activity",
            title="Structured Aerobic Exercise Protocol",
            description="Start with 25-30 minutes of low-impact brisk walking, stationary cycling, or swimming 4-5 days a week to strengthen myocardial endurance and reduce peripheral resistance.",
            urgency="moderate",
            icon="Flame"
        ))
    else:
        recommendations.append(Recommendation(
            category="Protective Strengths",
            title="Maintain Active Cardiovascular Regimen",
            description="Your current exercise frequency actively preserves ventricular compliance and metabolic health. Continue incorporating zone 2 cardio.",
            urgency="maintenance",
            icon="CheckCircle"
        ))

    # 5. Cholesterol & Metabolic
    chol = data.cholesterol or 190
    if chol >= 200:
        recommendations.append(Recommendation(
            category="Dietary Strategy",
            title="Target LDL Reduction with Soluble Fiber & Omega-3s",
            description="Incorporate oats, flaxseeds, legumes, and fatty fish (salmon, mackerel) to improve lipid fractions and lower systemic arterial inflammation.",
            urgency="moderate",
            icon="Heart"
        ))

    # 6. Stress and Sleep
    stress = (data.stress_level or "Medium").lower()
    sleep = (data.sleep_hours or "7-9 hours").lower()
    if stress == "high" or "less than 5" in sleep:
        recommendations.append(Recommendation(
            category="Lifestyle Intervention",
            title="Optimizing Sleep Hygiene & Autonomic Recovery",
            description="Target 7-8 hours of uninterrupted sleep. Practice diaphragmatic breathing or mindfulness exercises to lower sympathetic nervous system hyperactivity.",
            urgency="moderate",
            icon="Moon"
        ))

    # Guarantee at least 3 high-quality recommendations
    if len(recommendations) < 3:
        recommendations.append(Recommendation(
            category="Preventative Wellness",
            title="Annual Preventative Health Screening",
            description="Maintain regular health wellness checkups and stay up to date with resting ECG and biometric baselines.",
            urgency="maintenance",
            icon="ShieldCheck"
        ))

    return recommendations
