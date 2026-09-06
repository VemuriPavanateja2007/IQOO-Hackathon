from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, HealthProfile
from backend.schemas import ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/api/profile", tags=["Profile"])

@router.get("", response_model=ProfileResponse)
def get_profile(user_id: int = 1, db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    if not profile:
        # Create default profile if missing
        profile = HealthProfile(
            user_id=user_id,
            age=32,
            height_cm=178.0,
            weight_kg=74.5,
            blood_group="O+",
            allergies="None reported",
            medical_history="Space Adaptation Syndrome mild onset (Day 2 orbit); Baseline bone density normal.",
            station_role="Orbital Systems Engineer & Payload Specialist"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=ProfileResponse)
def update_profile(update_data: ProfileUpdate, user_id: int = 1, db: Session = Depends(get_db)):
    profile = db.query(HealthProfile).filter(HealthProfile.user_id == user_id).first()
    if not profile:
        profile = HealthProfile(user_id=user_id)
        db.add(profile)

    for field, val in update_data.model_dump(exclude_unset=True).items():
        if val is not None:
            setattr(profile, field, val)

    db.commit()
    db.refresh(profile)
    return profile
