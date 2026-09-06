from typing import Dict, Any, List
from backend.services.safety_policy import DEFAULT_DISCLAIMER

QUESTIONS = [
    {"id": "q1_down", "text": "Over the past 2 weeks in orbit, how often have you felt down, depressed, or hopeless?"},
    {"id": "q2_pleasure", "text": "How often have you felt little interest or pleasure in daily zero-g tasks or station activities?"},
    {"id": "q3_anxious", "text": "How often have you felt nervous, anxious, or on edge regarding mission duties or space environment?"},
    {"id": "q4_relax", "text": "How often have you found it difficult to relax or stop worrying?"}
]

def evaluate_mental_health_risk(q1: int, q2: int, q3: int, q4: int, notes: str = "") -> Dict[str, Any]:
    """
    Evaluates 4 PHQ-2/GAD-2 inspired questions (0-3 each, total 0-12).
    0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day
    """
    total = max(0, min(12, q1 + q2 + q3 + q4))

    if total >= 8:
        risk_tier = "High Concern"
        title = "Station CMO & Psychological Support Priority"
        message = (
            "Your responses indicate high psychological strain or stress in orbit. "
            "Because prolonged isolation and microgravity can impact emotional well-being, "
            "we strongly advise scheduling a confidential consultation with the Chief Medical Officer (CMO) "
            "or Station Tele-mental Health Support Team immediately."
        )
        escalation = True
        actions = [
            "Contact Station Chief Medical Officer (CMO) or Flight Surgeon via private comm link.",
            "Initiate Station Psychological Support Protocol (Channel 4-Alpha).",
            "Notify Mission Operations Commander if immediate duty relief is needed."
        ]

    elif total >= 4:
        risk_tier = "Moderate Concern"
        title = "Moderate Strain - Guided Wellness Recommended"
        message = (
            "You are experiencing moderate stress or lower mood scores. "
            "It is common during long-duration spaceflight. Engaging in guided breathing, "
            "adjusting sleep pod circadian lighting, and talking with crew mates can help stabilize mood."
        )
        escalation = False
        actions = [
            "Try the 5-minute zero-g box breathing exercise on your dashboard.",
            "Schedule a light recovery workout and review hydration intake.",
            "Consider a routine check-in with your assigned Station Medical Advisor."
        ]

    else:
        risk_tier = "Low Concern"
        title = "Optimal Mental Resilience & Well-being"
        message = (
            "Your responses suggest healthy mood balance and stress management in microgravity. "
            "Continue your regular physical resistance schedule, maintain circadian sleep pod routines, and perform weekly check-ins."
        )
        escalation = False
        actions = [
            "Maintain your current ARED resistance training schedule.",
            "Log daily mood and sleep scores to track long-term orbital trends.",
            "Keep up social check-ins with fellow crew members during meal times."
        ]

    return {
        "total_score": total,
        "risk_tier": risk_tier,
        "title": title,
        "message": message,
        "escalation_required": escalation,
        "recommended_actions": actions,
        "disclaimer": DEFAULT_DISCLAIMER
    }
