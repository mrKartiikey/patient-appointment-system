from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    time_slot = Column(String(20), nullable=False)
    status = Column(
        Enum("pending", "confirmed", "cancelled", "completed"),
        default="pending"
    )
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
