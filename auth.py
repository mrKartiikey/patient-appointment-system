import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import Patient
from passlib.context import CryptContext
from dotenv import load_dotenv
from logger import get_logger

load_dotenv()

logger = get_logger("auth")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"JWT token created for email: {email}")
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            logger.warning("Token decode failed: 'sub' field missing")
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        logger.warning("JWT decode error: token may be expired or invalid")
        raise HTTPException(status_code=401, detail="Expired token")

    user = db.query(Patient).filter(Patient.email == email).first()
    if user is None:
        logger.warning(f"Authenticated user not found in DB: {email}")
        raise HTTPException(status_code=401, detail="User not found")

    logger.info(f"User authenticated successfully: {email}")
    return user
