import random, time
from django.core.cache import cache

OTP_TTL = 5 * 60
MAX_PER_HOUR = 5
COOLDOWN = 60

def _rate_limit_key(phone): return f"otp_rate_{phone}"

def send_sms_code(phone: str) -> str:
    rec = cache.get(_rate_limit_key(phone), {'count':0,'last_reset':time.time(),'last':0})
    now = time.time()
    if now - rec['last_reset'] > 3600:
        rec = {'count':0,'last_reset':now,'last':0}
    if rec['count'] >= MAX_PER_HOUR:
        raise Exception('بیش از حد مجاز درخواست فرستادن کد')
    if now - rec['last'] < COOLDOWN:
        raise Exception('لطفاً یک دقیقه صبر کنید')
    code = f"{random.randint(100000,999999)}"
    cache.set(f"otp_{phone}", code, OTP_TTL)
    rec['count'] += 1; rec['last'] = now
    cache.set(_rate_limit_key(phone), rec, 3600)
    # TODO: integrate real SMS
    print(f"[SMS]={phone}:{code}")
    return code

def verify_sms_code(phone: str, code: str) -> bool:
    stored = cache.get(f"otp_{phone}")
    cache.delete(f"otp_{phone}")
    return stored == code