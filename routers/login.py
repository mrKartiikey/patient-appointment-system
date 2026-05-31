from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import Patient
from auth import verify_password, create_token
from logger import get_logger

router = APIRouter()
logger = get_logger("routers.login")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for: {form_data.username}")

    user = db.query(Patient).filter(Patient.email == form_data.username).first()
    if not user:
        logger.warning(f"Login failed - user not found: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, user.password):
        logger.warning(f"Login failed - wrong password for: {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.email)
    logger.info(f"Login successful for: {form_data.username}")
    return {"access_token": token, "token_type": "bearer"}
