from pydantic import BaseModel
from typing import Optional


class DoctorCreate(BaseModel):
    name: str
    email: str
    specialty: Optional[str] = None
    experience_years: Optional[int] = None
    fee: Optional[float] = None
    available_days: Optional[str] = None


class DoctorOut(BaseModel):
    id: int
    name: str
    email: str
    specialty: Optional[str]
    experience_years: Optional[int]
    fee: Optional[float]
    available_days: Optional[str]

    class Config:
        from_attributes = True
