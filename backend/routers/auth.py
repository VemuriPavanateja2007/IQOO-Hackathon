from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import User, HealthProfile, Medication, Appointment, ActivityEntry
from backend.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        # If user exists, log them in directly for smoother hackathon demo flow
        token = f"fake-jwt-token-for-{existing.id}"
        return {"access_token": token, "token_type": "bearer", "user": existing}

    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=f"hashed_{user_data.password}"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize default Health Profile
    profile = HealthProfile(
        user_id=user.id,
        age=32,
        height_cm=178.0,
        weight_kg=74.5,
        blood_group="O+",
        allergies="None reported",
        medical_history="Space Adaptation Syndrome mild onset (Day 2 orbit); Baseline bone density normal.",
        station_role="Orbital Systems Engineer & Payload Specialist"
    )
    db.add(profile)

    # Initialize sample medications
    med1 = Medication(
        user_id=user.id,
        name="Calcium + Vitamin D3 (Zero-G Bone Density Supp)",
        dosage="1000mg / 800 IU",
        frequency="Daily",
        schedule_time="08:00 UTC",
        is_taken_today=True,
        notes="Mandatory zero-g osteopenia prevention protocol."
    )
    med2 = Medication(
        user_id=user.id,
        name="Promethazine / Scopolamine (Space Anti-Nausea)",
        dosage="25mg",
        frequency="As needed",
        schedule_time="12:00 UTC",
        is_taken_today=False,
        notes="Prescribed by CMO for EVA suit operations."
    )
    db.add_all([med1, med2])

    # Initialize sample appointments
    appt1 = Appointment(
        user_id=user.id,
        doctor_name="Dr. Aris Thorne",
        specialty="Chief Medical Officer (CMO)",
        appointment_date="2026-09-08",
        appointment_time="14:30 UTC",
        status="Confirmed",
        notes="Routine 30-day orbital health review & bone densitometry ultrasound."
    )
    db.add(appt1)

    # Initialize sample activity entries
    db.add(ActivityEntry(user_id=user.id, activity_type="hr", value=72, unit="bpm", source="Wearable telemetry node"))
    db.add(ActivityEntry(user_id=user.id, activity_type="spo2", value=98, unit="%", source="Wearable telemetry node"))
    db.add(ActivityEntry(user_id=user.id, activity_type="sleep", value=7.4, unit="hours", source="Sleep Pod sensor mat"))
    db.add(ActivityEntry(user_id=user.id, activity_type="work_kj", value=950, unit="kJ", source="ARED Piston Telemetry"))

    db.commit()

    token = f"fake-jwt-token-for-{user.id}"
    return {"access_token": token, "token_type": "bearer", "user": user}


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        # Auto-create user for demo if not found
        return register(UserRegister(name="Astronaut Alex Vance", email=credentials.email, password=credentials.password), db)

    token = f"fake-jwt-token-for-{user.id}"
    return {"access_token": token, "token_type": "bearer", "user": user}
