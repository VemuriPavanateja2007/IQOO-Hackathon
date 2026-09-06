import os
import google.generativeai as genai
from typing import Dict, Any
from backend.config import settings
from backend.services.safety_policy import check_safety_policy, apply_disclaimer

SYSTEM_INSTRUCTION = """
You are the VitalMind Antigravity AI Health Assistant, a supportive, educational voice integrated into a zero-gravity fitness, wellness, and physiological monitoring platform. You are designed to assist users operating in prolonged microgravity or antigravity environments. You are NOT a medical doctor or a flight surgeon, and you never present yourself as one.

Scope:
- Answer general, educational questions about zero-g fitness protocols, muscle atrophy prevention, bone density maintenance, sleep optimization in microgravity, and stress management.
- Reference the user's health profile, wearable sensor data, mood logs, and medication context ONLY when it is provided to you in the prompt; never invent medical facts about the user.
- Provide guidance on adapting standard workouts to antigravity resistance equipment (ARED, flywheel ergometer, T2 treadmill harness).
- Encourage healthy habits with a warm, non-judgmental tone.

Hard limits:
- Never diagnose a condition (e.g., Space Adaptation Syndrome, radiation sickness) or name what you think the user has.
- Never prescribe, adjust, or recommend a dose of any medication (e.g., anti-nausea meds or sleep aids).
- If the user describes a possible medical emergency, severe pain, disorientation, suicidal thoughts, or a mental-health crisis, do NOT continue the normal conversation. Respond with calm, direct guidance to contact the station's Chief Medical Officer or initiate emergency medical protocols immediately. Avoid asking probing follow-up questions that could delay emergency response.
- If uncertain whether something is safe to answer in a hazardous zero-g environment, default to recommending a licensed professional rather than guessing.

Style:
- Short, plain-language sentences; no complex medical or aerospace jargon unless the user uses it first.
- Always end risk-adjacent answers with a one-line disclaimer that this is educational information, not a medical diagnosis.
"""

def generate_ai_response(question: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
    # 1. First, check safety policy hard limits
    safety_flag, escalation, override_msg = check_safety_policy(question)
    if override_msg:
        return {
            "response": override_msg,
            "safety_flag": safety_flag,
            "escalation_triggered": escalation
        }

    # 2. Prepare Context Prompt
    context_str = ""
    if user_context:
        context_str = (
            f"\n[USER HEALTH CONTEXT]\n"
            f"Role: {user_context.get('station_role', 'Crew Member')}\n"
            f"Age: {user_context.get('age', 32)}, Weight: {user_context.get('weight_kg', 74)}kg\n"
            f"Recent Heart Rate: {user_context.get('hr', 72)} bpm, SpO2: {user_context.get('spo2', 98)}%\n"
            f"Sleep Last Night: {user_context.get('sleep_hours', 7.2)} hours\n"
            f"Mood Score: {user_context.get('mood_score', 7)}/10, Stress Score: {user_context.get('stress_score', 3)}/10\n"
            f"Medications: {user_context.get('medications_summary', 'All clear')}\n"
        )

    full_prompt = f"{context_str}\nUser Question: {question}"

    # 3. Call Gemini API if Key is present
    api_key = settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=SYSTEM_INSTRUCTION
            )
            response = model.generate_content(full_prompt)
            raw_text = response.text if response.text else "I am processing your query. Please maintain hydration and monitor telemetry."
            final_text = apply_disclaimer(raw_text)
            return {
                "response": final_text,
                "safety_flag": "SAFE",
                "escalation_triggered": False
            }
        except Exception as e:
            # Fallback to local intelligent response engine if network/key fails
            pass

    # 4. Built-in Microgravity Persona Fallback Engine
    fallback_text = get_fallback_antigravity_response(question, user_context)
    final_text = apply_disclaimer(fallback_text)
    return {
        "response": final_text,
        "safety_flag": "SAFE",
        "escalation_triggered": False
    }

def get_fallback_antigravity_response(question: str, context: Dict[str, Any] = None) -> str:
    q = question.lower()
    
    if "sleep" in q or "rest" in q:
        return (
            "In zero-g, circadian rhythms can be disrupted by 16 orbital sunrises a day. "
            "To optimize sleep in your pod, ensure your sleeping bag harness provides gentle axial pressure to mimic gravity. "
            "Set station pod lighting to deep red 45 minutes before sleep and keep airflow ventilation steady to prevent CO2 pockets near your face."
        )
    elif "workout" in q or "exercise" in q or "ared" in q or "muscle" in q or "bone" in q:
        return (
            "Preventing muscle atrophy and bone density loss in microgravity requires daily high-resistance loading. "
            "Ensure your Advanced Resistive Exercise Device (ARED) vacuum cylinders are set to your target eccentric load. "
            "Combine 45 minutes of ARED squat and deadlift variations with 30 minutes on the T2 Treadmill using your shoulder harness."
        )
    elif "stress" in q or "anxious" in q or "mood" in q:
        return (
            "Prolonged microgravity and station isolation can increase stress scores. "
            "Try a 5-minute zero-g box breathing exercise while floating in a quiet module. "
            "Focus on slow diaphragmatic breathing and sync your heart rate telemetry with station relaxing visualizers."
        )
    elif "food" in q or "nutrition" in q or "diet" in q or "water" in q or "hydration" in q:
        return (
            "Fluid shifts in microgravity alter taste perception and electrolyte balance. "
            "Maintain steady hydration using your pouch straw to avoid microgravity dehydration, and ensure your intake includes Calcium and Vitamin D3 to support bone turnover."
        )
    else:
        return (
            "Staying healthy in microgravity involves balancing daily ARED physical resistance training, steady hydration, sleep pod circadian alignment, and stress check-ins. "
            "Let me know if you would like guidance on adapting your workout, managing sleep cycles, or checking your daily telemetry."
        )
