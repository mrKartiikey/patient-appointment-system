from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment, Patient
from schemas import AppointmentCreate, AppointmentUpdate, AppointmentOut
from auth import get_current_user
from logger import get_logger

router = APIRouter()
logger = get_logger("routers.appointments")


@router.post("/", response_model=AppointmentOut)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(
        f"Create appointment - patient_id={appointment.patient_id}, "
        f"doctor_id={appointment.doctor_id}, date={appointment.appointment_date}, "
        f"requested by: {current_user.email}"
    )

    new_appt = Appointment(**appointment.model_dump())
    db.add(new_appt)
    db.commit()
    db.refresh(new_appt)

    logger.info(f"Appointment created successfully: id={new_appt.id}")
    return new_appt


@router.get("/", response_model=list[AppointmentOut])
def get_all_appointments(
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Fetching all appointments - requested by: {current_user.email}")
    appointments = db.query(Appointment).all()
    logger.debug(f"Total appointments fetched: {len(appointments)}")
    return appointments


@router.get("/{appointment_id}", response_model=AppointmentOut)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Fetching appointment id={appointment_id} - requested by: {current_user.email}")
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        logger.warning(f"Appointment not found: id={appointment_id}")
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt


@router.patch("/{appointment_id}", response_model=AppointmentOut)
def update_appointment(
    appointment_id: int,
    update_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Update appointment id={appointment_id} - requested by: {current_user.email}")
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        logger.warning(f"Update failed - appointment not found: id={appointment_id}")
        raise HTTPException(status_code=404, detail="Appointment not found")

    update_fields = update_data.model_dump(exclude_unset=True)
    for key, value in update_fields.items():
        setattr(appt, key, value)

    db.commit()
    db.refresh(appt)

    logger.info(f"Appointment updated: id={appointment_id}, fields={list(update_fields.keys())}")
    return appt


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: Patient = Depends(get_current_user)
):
    logger.info(f"Delete appointment id={appointment_id} - requested by: {current_user.email}")
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appt:
        logger.warning(f"Delete failed - appointment not found: id={appointment_id}")
        raise HTTPException(status_code=404, detail="Appointment not found")

    db.delete(appt)
    db.commit()
    logger.info(f"Appointment deleted successfully: id={appointment_id}")
    return {"message": f"Appointment {appointment_id} deleted successfully"}
