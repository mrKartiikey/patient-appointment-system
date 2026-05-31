from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    specialty = Column(String(100))
    experience_years = Column(Integer)
    fee = Column(DECIMAL(10, 2))
    available_days = Column(String(100))

    appointments = relationship("Appointment", back_populates="doctor")
