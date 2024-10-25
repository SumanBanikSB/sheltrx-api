from datetime import datetime, timedelta
from jose import JWTError, jwt
from .config import settings
from passlib.context import CryptContext
from aiosmtplib import send
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

hostname = os.getenv("SMTP_HOSTNAME")
port = os.getenv("SMTP_PORT")
start_tls = os.getenv("SMTP_START_TLS") == 'True'
username = os.getenv("SMTP_USERNAME")
password = os.getenv("SMTP_PASSWORD")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def send_email(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = "baniksuman9434@gmail.com"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    await send(
        msg,
        hostname=hostname,
        port=int(port),
        start_tls=start_tls,
        username=username,
        password=password
    )
