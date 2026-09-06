from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None
    station_role: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    age: int
    height_cm: float
    weight_kg: float
    blood_group: str
    allergies: str
    medical_history: str
    station_role: str

    class Config:
        from_attributes = True

class ActivityCreate(BaseModel):
    activity_type: str
    value: float
    unit: Optional[str] = ""
    source: Optional[str] = "Manual Entry"
    notes: Optional[str] = None

class ActivityResponse(BaseModel):
    id: int
    activity_type: str
    value: float
    unit: str
    source: str
    notes: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    frequency: str = "Daily"
    schedule_time: str = "08:00 UTC"
    notes: Optional[str] = None

class MedicationResponse(BaseModel):
    id: int
    name: str
    dosage: str
    frequency: str
    schedule_time: str
    is_taken_today: bool
    notes: Optional[str]

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    doctor_name: str
    specialty: str = "Chief Medical Officer (CMO)"
    appointment_date: str
    appointment_time: str
    notes: Optional[str] = None

class AppointmentResponse(BaseModel):
    id: int
    doctor_name: str
    specialty: str
    appointment_date: str
    appointment_time: str
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True

class RiskScreenRequest(BaseModel):
    q1_down: int      # 0 to 3
    q2_pleasure: int  # 0 to 3
    q3_anxious: int   # 0 to 3
    q4_relax: int     # 0 to 3
    additional_notes: Optional[str] = None

class RiskScreenResponse(BaseModel):
    total_score: int
    risk_tier: str # Low Concern, Moderate Concern, High Concern
    title: str
    message: str
    escalation_required: bool
    recommended_actions: List[str]

class AIChatRequest(BaseModel):
    question: str

class AIChatResponse(BaseModel):
    question: str
    response: str
    safety_flag: str # SAFE, MEDICAL_EMERGENCY, DIAGNOSIS_ATTEMPT, PRESCRIPTION_ATTEMPT
    escalation_triggered: bool
    timestamp: datetime

class RecommendationResponse(BaseModel):
    recommendation_type: str # normal_workout, recovery_workout, wellness_rest
    title: str
    summary: str
    exercise_protocol: List[str]
    wellness_tips: List[str]
    disclaimer: str
