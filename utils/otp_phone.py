import random
import hashlib
import re

from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta

OTP_LENGTH = 6
OTP_EXPIRATION_MINUTES = 3

def generate_otp(length=OTP_LENGTH):
    return ''.join(random.choices('0123456789', k=length))

def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()

def is_otp_valid(provided_otp, stored_hash):
    return hash_otp(provided_otp) == stored_hash

def get_otp_expiration():
    return timezone.now() + timedelta(minutes=OTP_EXPIRATION_MINUTES)

def is_valid_phone(phone):
    return re.fullmatch(r'^(\+98|0)?9\d{9}$', phone) is not None

def verify_otp_hash(otp_raw, otp_hashed):
    """
    مقایسه OTP واردشده با هش ذخیره‌شده در دیتابیس
    """
    return check_password(otp_raw, otp_hashed)