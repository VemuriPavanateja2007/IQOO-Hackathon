from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import AIConversation, HealthProfile, ActivityEntry, Medication, MentalHealthLog
from backend.schemas import AIChatRequest, AIChatResponse
from backend.services.ai_service import generate_ai_response
from datetime import datetime

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])

@router.post("/chat", response_model=AIChatResponse)
def ai_chat(payload: AIChatRequest, user_id: int = 1, db: Session = Depends(get_db)):
    # Gather user context
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    recent_hr = db.query(ActivityEntry).filter(ActivityEntry.user_id == user_id, ActivityEntry.activity_type == "hr").order_by(ActivityEntry.timestamp.desc()).first()
    recent_spo2 = db.query(ActivityEntry).filter(ActivityEntry.user_id == user_id, ActivityEntry.activity_type == "spo2").order_by(ActivityEntry.timestamp.desc()).first()
    recent_sleep = db.query(ActivityEntry).filter(ActivityEntry.user_id == user_id, ActivityEntry.activity_type == "sleep").order_by(ActivityEntry.timestamp.desc()).first()
    recent_mh = db.query(MentalHealthLog).filter(MentalHealthLog.user_id == user_id).order_by(MentalHealthLog.timestamp.desc()).first()
    active_meds = db.query(Medication).filter(Medication.user_id == user_id).all()

    meds_summary = ", ".join([f"{m.name} ({'Taken' if m.is_taken_today else 'Pending'})" for m in active_meds]) if active_meds else "None"

    context = {
        "station_role": profile.station_role if profile else "Orbital Payload Specialist",
        "age": profile.age if profile else 32,
        "weight_kg": profile.weight_kg if profile else 74.5,
        "hr": recent_hr.value if recent_hr else 72,
        "spo2": recent_spo2.value if recent_spo2 else 98,
        "sleep_hours": recent_sleep.value if recent_sleep else 7.2,
        "mood_score": recent_mh.mood_score if recent_mh else 7,
        "stress_score": recent_mh.stress_score if recent_mh else 3,
        "medications_summary": meds_summary
    }

    ai_result = generate_ai_response(payload.question, context)

    # Save to history DB
    chat_log = AIConversation(
        user_id=user_id,
        question=payload.question,
        response=ai_result["response"],
        safety_flag=ai_result["safety_flag"],
        escalation_triggered=ai_result["escalation_triggered"]
    )
    db.add(chat_log)
    db.commit()

    return {
        "question": payload.question,
        "response": ai_result["response"],
        "safety_flag": ai_result["safety_flag"],
        "escalation_triggered": ai_result["escalation_triggered"],
        "timestamp": datetime.utcnow()
    }
