"""
Utility helpers for Jharkhand Tourism application.
Includes password hashing, JWT handling, OTP generation, email sending, and validation.
"""

import os
import re
import random
import string
from datetime import datetime, timedelta

import bcrypt
import jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"


def hash_password(password):
    if isinstance(password, str):
        password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")


def check_password(password, hashed_password):
    if isinstance(password, str):
        password = password.encode("utf-8")
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password, hashed_password)


def create_otp_code(length=6):
    return "".join(random.choices(string.digits, k=length))


def send_email(subject, recipient, body):
    # Placeholder email sender. Replace with a real mail service in production.
    print(f"[EMAIL] To: {recipient}\nSubject: {subject}\n\n{body}")
    return True


def generate_jwt(payload, expires_minutes=60):
    data = payload.copy()
    data["exp"] = datetime.utcnow() + timedelta(minutes=expires_minutes)
    data["iat"] = datetime.utcnow()
    return jwt.encode(data, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def is_valid_email(email):
    if not isinstance(email, str):
        return False
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


def is_strong_password(password):
    if not isinstance(password, str) or len(password) < 8:
        return False
    return bool(
        re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
        and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    )
