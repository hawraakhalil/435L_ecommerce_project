from datetime import datetime

def get_utc_now():
    return datetime.utcnow()

def format_phone(phone):
    phone = '+961-' + phone[:2] + '-' + phone[2:5] + '-' + phone[5:]
    return phone
