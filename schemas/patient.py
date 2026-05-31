from pydantic import BaseModel
from typing import Optional


class PatientCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    age: Optional[int] = None
    password: str


class PatientOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    age: Optional[int]

    class Config:
        from_attributes = True
