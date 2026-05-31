from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Doctor, Patient
from schemas import DoctorCreate, DoctorOut
from auth import get_current_user
from logger import get_logger

router = APIRouter()
logger = get_logger("routers.doctors")


@router.post("/", response_model=DoctorOut)
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Create doctor request - by: {current_user.email}, doctor email: {doctor.email}")

    existing = db.query(Doctor).filter(Doctor.email == doctor.email).first()
    if existing:
        logger.warning(f"Doctor creation failed - email already exists: {doctor.email}")
        raise HTTPException(status_code=400, detail="Doctor with this email already exists")

    new_doctor = Doctor(**doctor.model_dump())
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    logger.info(f"Doctor created successfully: id={new_doctor.id}, email={new_doctor.email}")
    return new_doctor


@router.get("/", response_model=list[DoctorOut])
def get_all_doctors(db: Session = Depends(get_db)):
    logger.info("Fetching all doctors")
    doctors = db.query(Doctor).all()
    logger.debug(f"Total doctors fetched: {len(doctors)}")
    return doctors


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching doctor id={doctor_id}")
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        logger.warning(f"Doctor not found: id={doctor_id}")
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Delete request for doctor id={doctor_id} - by: {current_user.email}")
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        logger.warning(f"Delete failed - doctor not found: id={doctor_id}")
        raise HTTPException(status_code=404, detail="Doctor not found")

    db.delete(doctor)
    db.commit()
    logger.info(f"Doctor deleted successfully: id={doctor_id}")
    return {"message": f"Doctor {doctor_id} deleted successfully"}
