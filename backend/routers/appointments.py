from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Appointment
from backend.schemas import AppointmentCreate, AppointmentResponse

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

@router.get("", response_model=List[AppointmentResponse])
def get_appointments(user_id: int = 1, db: Session = Depends(get_db)):
    appts = db.query(Appointment).filter(Appointment.user_id == user_id).order_by(Appointment.created_at.desc()).all()
    if not appts:
        a1 = Appointment(
            user_id=user_id,
            doctor_name="Dr. Aris Thorne",
            specialty="Chief Medical Officer (CMO)",
            appointment_date="2026-09-08",
            appointment_time="14:30 UTC",
            status="Confirmed",
            notes="30-day orbital health review & bone densitometry ultrasound scan."
        )
        db.add(a1)
        db.commit()
        appts = [a1]
    return appts

@router.post("", response_model=AppointmentResponse)
def add_appointment(appt: AppointmentCreate, user_id: int = 1, db: Session = Depends(get_db)):
    new_appt = Appointment(
        user_id=user_id,
        doctor_name=appt.doctor_name,
        specialty=appt.specialty,
        appointment_date=appt.appointment_date,
        appointment_time=appt.appointment_time,
        status="Confirmed",
        notes=appt.notes
    )
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)
    return new_appt
