from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("HealthProfile", back_populates="user", uselist=False)
    activities = relationship("ActivityEntry", back_populates="user")
    medications = relationship("Medication", back_populates="user")
    appointments = relationship("Appointment", back_populates="user")
    mental_health_logs = relationship("MentalHealthLog", back_populates="user")
    ai_conversations = relationship("AIConversation", back_populates="user")


class HealthProfile(Base):
    __tablename__ = "health_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    age = Column(Integer, default=32)
    height_cm = Column(Float, default=178.0)
    weight_kg = Column(Float, default=74.5)
    blood_group = Column(String(10), default="O+")
    allergies = Column(Text, default="None reported")
    medical_history = Column(Text, default="Space Adaptation Syndrome mild onset (Day 2 orbit); Baseline bone density normal.")
    station_role = Column(String(100), default="Orbital Systems Engineer & Payload Specialist")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class ActivityEntry(Base):
    __tablename__ = "activity_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_type = Column(String(50))  # hr, spo2, sleep, steps, work_kj, mood, stress
    value = Column(Float, nullable=False)
    unit = Column(String(20), default="")
    source = Column(String(50), default="Wearable Telemetry Sensor Node")
    notes = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), default="Daily")
    schedule_time = Column(String(50), default="08:00 UTC")
    is_taken_today = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="medications")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_name = Column(String(100), nullable=False)
    specialty = Column(String(100), default="Chief Medical Officer (CMO)")
    appointment_date = Column(String(50), nullable=False)
    appointment_time = Column(String(50), nullable=False)
    status = Column(String(30), default="Confirmed")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="appointments")


class MentalHealthLog(Base):
    __tablename__ = "mental_health_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood_score = Column(Integer, default=7)    # 1 to 10
    stress_score = Column(Integer, default=4)  # 1 to 10
    phq2_gad2_score = Column(Integer, default=1) # 0 to 12
    risk_tier = Column(String(30), default="Low Concern") # Low, Moderate, High
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mental_health_logs")


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    safety_flag = Column(String(50), default="SAFE")
    escalation_triggered = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ai_conversations")
