from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Appointment, Doctor, Patient
from routers import patients, doctors, appointments, login
from logger import get_logger
from utils import send_appointment_email

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Appointment System", version="2.0.0")
logger = get_logger("main")
templates = Jinja2Templates(directory="templates")

app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(doctors.router, prefix="/doctors", tags=["Doctors"])
app.include_router(appointments.router, prefix="/appointments", tags=["Appointments"])
app.include_router(login.router, prefix="/auth", tags=["Authentication"])


@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "API is running"}


@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    logger.info("Dashboard endpoint hit")

    all_appointments = db.query(Appointment).all()
    total_patients = db.query(Patient).count()
    total_doctors = db.query(Doctor).count()

    logger.debug(
        f"Dashboard stats - appointments: {len(all_appointments)}, "
        f"patients: {total_patients}, doctors: {total_doctors}"
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "appointments": all_appointments,
            "p_count": total_patients,
            "d_count": total_doctors
        }
    )


@app.get("/test-email")
async def test_email():
    logger.info("Test email endpoint triggered")
    await send_appointment_email(
        email_to="kartikmalviya6375@gmail.com",
        patient_name="Kartik",
        doctor_name="Sharma",
        date="18 May",
        time="5 PM"
    )
    logger.info("Test email sent successfully")
    return {"message": "Email Sent Successfully"}
