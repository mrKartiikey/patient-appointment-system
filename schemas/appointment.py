from pydantic import BaseModel
from typing import Optional
from datetime import date


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: str
    notes: Optional[str] = None


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    time_slot: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    time_slot: str
    status: str
    notes: Optional[str]

    class Config:
        from_attributes = True
