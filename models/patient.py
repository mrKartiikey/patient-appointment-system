from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15))
    age = Column(Integer)
    password = Column(String(255), nullable=False)
    role = Column(
        Enum("patient", "admin"),
        default="patient"
    )

    appointments = relationship("Appointment", back_populates="patient")
