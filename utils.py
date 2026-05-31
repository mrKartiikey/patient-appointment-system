import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from twilio.rest import Client

load_dotenv(".env")

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

# Twilio Client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)


async def send_appointment_email(
    email_to: str,
    patient_name: str,
    doctor_name: str,
    date: str,
    time: str
):
    message = MessageSchema(
        subject="Appointment Confirmation",
        recipients=[email_to],
        body=f"""
Namaste {patient_name},

Aapka appointment Dr. {doctor_name} ke saath confirm ho gaya hai.

Date: {date}
Time: {time}

Dhanyawad!
""",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)


def send_whatsapp_msg(
    to_number: str,
    patient_name: str,
    doctor_name: str,
    date: str,
    time: str
):
    try:
        message = twilio_client.messages.create(
            from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
            body=f"Hi {patient_name}, aapka appointment Dr. {doctor_name} ke saath {date} ko {time} baje confirm ho gaya hai.",
            to=f"whatsapp:{to_number}"
        )
        return message.sid
    except Exception as e:
        print("WhatsApp Error:", e)
