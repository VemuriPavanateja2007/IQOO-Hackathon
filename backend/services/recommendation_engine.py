from typing import Dict, Any, List
from backend.services.safety_policy import DEFAULT_DISCLAIMER

def calculate_antigravity_recommendation(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates weekly/daily context to produce adaptive zero-g fitness & wellness protocol.
    Inputs:
        steps_avg (work equivalent)
        sleep_hours_avg
        mood_score_avg (1-10)
        stress_score_avg (1-10)
        workouts_completed (count)
        missed_medications (count)
    """
    steps = metrics.get("steps_avg", 8500)
    sleep = metrics.get("sleep_hours_avg", 7.0)
    mood = metrics.get("mood_score_avg", 7)
    stress = metrics.get("stress_score_avg", 4)
    workouts = metrics.get("workouts_completed", 4)
    missed_meds = metrics.get("missed_medications", 0)

    # Decision Logic:
    # Branch C: High stress (>=7), low sleep (<6.0), low mood (<=4), or missed medications (>1)
    if stress >= 7 or sleep < 6.0 or mood <= 4 or missed_meds > 1:
        rec_type = "wellness_rest"
        title = "Wellness Rest & Orbital Recovery Nudge"
        summary = (
            "Your telemetry indicates elevated stress scores, low sleep duration, or missed medications. "
            "In microgravity, pushing heavy load under physical strain can worsen fluid shift headaches and muscular fatigue. "
            "Today's recommendation focuses on active relaxation, hydration, and a gentle mental-health check-in."
        )
        protocol = [
            "0-G Sleep Pod Reset: 30 mins circadian red-light therapy & acoustic isolation",
            "Diaphragmatic Breathing: 10 mins box breathing in crew quarter module",
            "Passive Spinal Decompression: Floating stretch with knee-to-chest tether",
            "Hydration & Electrolyte Intake: 500mL mineralized water pouch"
        ]
        tips = [
            "Review missed medication schedule with Station CMO notes.",
            "Complete a 4-question Mental Health Check-In on the dashboard.",
            "Dim pod lighting 1 hour prior to sleep cycle."
        ]

    # Branch B: Moderate fatigue, sleep 6.0 - 6.8 hrs, or stress 5 - 6
    elif sleep < 6.8 or stress >= 5 or workouts >= 6:
        rec_type = "recovery_workout"
        title = "Lighter Zero-G Ergometer & Mobility Protocol"
        summary = (
            "You are maintaining consistent orbital training, but your physiological telemetry shows light strain. "
            "To protect bone mineral density without overtaxing your recovery system, we recommend a lighter ARED load paired with ergometer mobility."
        )
        protocol = [
            "ARED Light Load Squat: 3 sets x 10 reps @ 50% max vacuum piston resistance",
            "Cycle Ergometer (CEVIS): 20 mins low-resistance steady cadence (110-120 bpm HR target)",
            "Thoracic & Lumbar Zero-G Mobility: 15 mins tethered foam roll & axial extension"
        ]
        tips = [
            "Keep fluid intake steady during ergometer session.",
            "Perform post-workout hamstring stretches while tethered to wall foot-stops."
        ]

    # Branch A: Optimal condition (High mood, stress < 5, sleep >= 6.8)
    else:
        rec_type = "normal_workout"
        title = "Full Antigravity Resistance & Osteo-Preservation Protocol"
        summary = (
            "Your physiological telemetry, sleep scores, and mood logs are in prime condition. "
            "Proceed with high-intensity ARED resistance training to prevent osteopenia and maintain leg muscle mass."
        )
        protocol = [
            "ARED Heavy Deadlifts & Squats: 4 sets x 8 reps @ 80% max vacuum piston load",
            "T2 Treadmill Interval Run: 30 mins with shoulder harness @ 75% body-weight equivalent load",
            "Upper Body Core Stability: 3 sets ARED bench press & seated row",
            "Cool Down: 10 mins light cycle ergometer spinning"
        ]
        tips = [
            "Verify shoulder harness pad positioning before T2 treadmill sprint intervals.",
            "Log post-workout rate of perceived exertion (RPE) on the dashboard."
        ]

    return {
        "recommendation_type": rec_type,
        "title": title,
        "summary": summary,
        "exercise_protocol": protocol,
        "wellness_tips": tips,
        "disclaimer": DEFAULT_DISCLAIMER
    }
