from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ActivityEntry, Medication, MentalHealthLog
from backend.schemas import RecommendationResponse
from backend.services.recommendation_engine import calculate_antigravity_recommendation

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("", response_model=RecommendationResponse)
def get_recommendation(user_id: int = 1, db: Session = Depends(get_db)):
    # Calculate telemetry metrics
    sleep_entries = db.query(ActivityEntry).filter(ActivityEntry.user_id == user_id, ActivityEntry.activity_type == "sleep").all()
    sleep_avg = sum([e.value for e in sleep_entries]) / len(sleep_entries) if sleep_entries else 7.2

    work_entries = db.query(ActivityEntry).filter(ActivityEntry.user_id == user_id, ActivityEntry.activity_type == "work_kj").all()
    steps_avg = sum([e.value for e in work_entries]) / len(work_entries) if work_entries else 8500

    recent_mh = db.query(MentalHealthLog).filter(MentalHealthLog.user_id == user_id).order_by(MentalHealthLog.timestamp.desc()).first()
    mood_score = recent_mh.mood_score if recent_mh else 7
    stress_score = recent_mh.stress_score if recent_mh else 3

    missed_meds = db.query(Medication).filter(Medication.user_id == user_id, Medication.is_taken_today == False).count()

    metrics = {
        "steps_avg": steps_avg,
        "sleep_hours_avg": sleep_avg,
        "mood_score_avg": mood_score,
        "stress_score_avg": stress_score,
        "workouts_completed": len(work_entries) or 4,
        "missed_medications": missed_meds
    }

    result = calculate_antigravity_recommendation(metrics)
    return result
