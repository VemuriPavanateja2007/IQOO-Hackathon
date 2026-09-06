from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import ActivityEntry
from backend.schemas import ActivityCreate, ActivityResponse

router = APIRouter(prefix="/api/activity", tags=["Activity & Telemetry"])

@router.get("", response_model=List[ActivityResponse])
def get_activities(user_id: int = 1, db: Session = Depends(get_db)):
    entries = db.query(ActivityEntry).filter(ActivityEntry.user_id == user_id).order_by(ActivityEntry.timestamp.desc()).all()
    if not entries:
        # Seed initial entries if empty
        defaults = [
            ActivityEntry(user_id=user_id, activity_type="hr", value=72, unit="bpm", source="Wearable sensor"),
            ActivityEntry(user_id=user_id, activity_type="spo2", value=98, unit="%", source="Wearable sensor"),
            ActivityEntry(user_id=user_id, activity_type="sleep", value=7.4, unit="hours", source="Sleep pod mat"),
            ActivityEntry(user_id=user_id, activity_type="work_kj", value=920, unit="kJ", source="ARED telemetry"),
            ActivityEntry(user_id=user_id, activity_type="mood", value=8, unit="score", source="Dashboard quick log"),
            ActivityEntry(user_id=user_id, activity_type="stress", value=3, unit="score", source="Dashboard quick log")
        ]
        db.add_all(defaults)
        db.commit()
        entries = defaults
    return entries

@router.post("", response_model=ActivityResponse)
def add_activity(activity: ActivityCreate, user_id: int = 1, db: Session = Depends(get_db)):
    entry = ActivityEntry(
        user_id=user_id,
        activity_type=activity.activity_type,
        value=activity.value,
        unit=activity.unit or "",
        source=activity.source or "Manual entry",
        notes=activity.notes
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
