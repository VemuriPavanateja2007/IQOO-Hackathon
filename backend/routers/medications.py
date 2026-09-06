from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Medication
from backend.schemas import MedicationCreate, MedicationResponse

router = APIRouter(prefix="/api/medications", tags=["Medications"])

@router.get("", response_model=List[MedicationResponse])
def get_medications(user_id: int = 1, db: Session = Depends(get_db)):
    meds = db.query(Medication).filter(Medication.user_id == user_id).all()
    if not meds:
        m1 = Medication(user_id=user_id, name="Calcium + Vitamin D3 (Zero-G Bone Supp)", dosage="1000mg / 800 IU", frequency="Daily", schedule_time="08:00 UTC", is_taken_today=True, notes="Mandatory osteopenia prevention")
        m2 = Medication(user_id=user_id, name="Promethazine / Scopolamine Patch", dosage="25mg", frequency="As needed", schedule_time="12:00 UTC", is_taken_today=False, notes="EVA anti-motion sickness")
        db.add_all([m1, m2])
        db.commit()
        meds = [m1, m2]
    return meds

@router.post("", response_model=MedicationResponse)
def add_medication(med: MedicationCreate, user_id: int = 1, db: Session = Depends(get_db)):
    new_med = Medication(
        user_id=user_id,
        name=med.name,
        dosage=med.dosage,
        frequency=med.frequency,
        schedule_time=med.schedule_time,
        is_taken_today=False,
        notes=med.notes
    )
    db.add(new_med)
    db.commit()
    db.refresh(new_med)
    return new_med

@router.put("/{med_id}/toggle", response_model=MedicationResponse)
def toggle_medication_adherence(med_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    med = db.query(Medication).filter(Medication.id == med_id, Medication.user_id == user_id).first()
    if not med:
        raise HTTPException(status_code=404, detail="Medication record not found")
    med.is_taken_today = not med.is_taken_today
    db.commit()
    db.refresh(med)
    return med
