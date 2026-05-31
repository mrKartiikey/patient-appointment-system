from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Patient
from schemas import PatientCreate, PatientOut
from auth import hash_password, get_current_user
from logger import get_logger

router = APIRouter()
logger = get_logger("routers.patients")


@router.post("/register", response_model=PatientOut)
def register_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    logger.info(f"Register attempt for email: {patient.email}")

    existing = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing:
        logger.warning(f"Registration failed - email already exists: {patient.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(patient.password)
    new_patient = Patient(
        name=patient.name,
        email=patient.email,
        phone=patient.phone,
        age=patient.age,
        password=hashed
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    logger.info(f"Patient registered successfully: id={new_patient.id}, email={new_patient.email}")
    return new_patient


@router.get("/", response_model=list[PatientOut])
def get_all_patients(
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Fetching all patients - requested by: {current_user.email}")
    patients = db.query(Patient).all()
    logger.debug(f"Total patients fetched: {len(patients)}")
    return patients


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Fetching patient id={patient_id} - requested by: {current_user.email}")
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        logger.warning(f"Patient not found: id={patient_id}")
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Delete request for patient id={patient_id} - by: {current_user.email}")
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        logger.warning(f"Delete failed - patient not found: id={patient_id}")
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    logger.info(f"Patient deleted successfully: id={patient_id}")
    return {"message": f"Patient {patient_id} deleted successfully"}
