from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import MentalHealthLog
from backend.schemas import RiskScreenRequest, RiskScreenResponse
from backend.services.risk_service import evaluate_mental_health_risk

router = APIRouter(prefix="/api/risk", tags=["Risk & Mental Health Triage"])

@router.post("/screen", response_model=RiskScreenResponse)
def screen_mental_health_risk(payload: RiskScreenRequest, user_id: int = 1, db: Session = Depends(get_db)):
    result = evaluate_mental_health_risk(
        q1=payload.q1_down,
        q2=payload.q2_pleasure,
        q3=payload.q3_anxious,
        q4=payload.q4_relax,
        notes=payload.additional_notes or ""
    )

    # Save log to database
    log = MentalHealthLog(
        user_id=user_id,
        mood_score=max(1, 10 - (payload.q1_down + payload.q2_pleasure)),
        stress_score=min(10, (payload.q3_anxious + payload.q4_relax) * 2 + 1),
        phq2_gad2_score=result["total_score"],
        risk_tier=result["risk_tier"],
        notes=payload.additional_notes
    )
    db.add(log)
    db.commit()

    return result
