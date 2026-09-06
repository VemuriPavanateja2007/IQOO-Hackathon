import re
from typing import Dict, Any, Tuple

EMERGENCY_KEYWORDS = [
    r"severe pain", r"chest pain", r"cannot breathe", r"can't breathe",
    r"disoriented", r"disorientation", r"suicid", r"self-harm", r"self harm",
    r"kill myself", r"crisis", r"passing out", r"unconscious", r"heavy bleeding",
    r"decompression", r"radiation sickness", r"acute vomiting", r"vision loss"
]

DIAGNOSIS_KEYWORDS = [
    r"do i have", r"diagnose", r"what disease", r"is this space adaptation syndrome",
    r"do i have sas", r"what illness", r"am i sick with"
]

PRESCRIPTION_KEYWORDS = [
    r"prescribe", r"dosage for me", r"recommend a dose", r"what pill should i take",
    r"give me medication for", r"how much scopolamine", r"how much sleep aid"
]

DEFAULT_DISCLAIMER = "VitalMind AI provides educational information only, not a medical diagnosis or prescription."

def check_safety_policy(question: str) -> Tuple[str, bool, str]:
    """
    Evaluates input text against safety policy hard limits.
    Returns: (safety_flag, escalation_triggered, emergency_response_override)
    """
    q_lower = question.lower()

    # 1. Emergency Protocol Check
    for pattern in EMERGENCY_KEYWORDS:
        if re.search(pattern, q_lower):
            emergency_msg = (
                "EMERGENCY MEDICAL PROTOCOL ACTIVATED:\n"
                "If you are experiencing severe pain, disorientation, chest tightness, acute psychological crisis, "
                "or a zero-g medical emergency, please IMMEDIATELY contact the Station Chief Medical Officer (CMO) "
                "or hit the Emergency Alert button on your suit/console. "
                "Do not wait for conversational AI response.\n\n"
                f"Disclaimer: {DEFAULT_DISCLAIMER}"
            )
            return "MEDICAL_EMERGENCY", True, emergency_msg

    # 2. Medical Diagnosis Attempt Check
    for pattern in DIAGNOSIS_KEYWORDS:
        if re.search(pattern, q_lower):
            diagnosis_msg = (
                "I am the VitalMind AI Assistant. I am designed for fitness, physiological monitoring, and wellness education "
                "in microgravity, but I am NOT a flight surgeon or medical doctor. I cannot diagnose medical conditions or Space Adaptation Syndrome.\n\n"
                "Please consult the Station Chief Medical Officer (CMO) for clinical diagnosis and evaluation.\n\n"
                f"Disclaimer: {DEFAULT_DISCLAIMER}"
            )
            return "DIAGNOSIS_ATTEMPT", False, diagnosis_msg

    # 3. Prescription / Dosage Adjustment Check
    for pattern in PRESCRIPTION_KEYWORDS:
        if re.search(pattern, q_lower):
            prescription_msg = (
                "I cannot prescribe, adjust, or recommend doses for medications (including anti-nausea meds, sleep aids, or supplements). "
                "Medication schedules in space must be strictly verified with your Station Flight Surgeon or CMO.\n\n"
                f"Disclaimer: {DEFAULT_DISCLAIMER}"
            )
            return "PRESCRIPTION_ATTEMPT", False, prescription_msg

    return "SAFE", False, ""

def apply_disclaimer(response_text: str) -> str:
    """Ensures every risk-adjacent or educational AI answer ends with the mandatory disclaimer line."""
    if DEFAULT_DISCLAIMER not in response_text:
        return f"{response_text.strip()}\n\nDisclaimer: {DEFAULT_DISCLAIMER}"
    return response_text
