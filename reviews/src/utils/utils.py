from datetime import datetime, timezone

def get_utc_now():
    return datetime.now(timezone.utc)

def format_phone(phone):
    phone = '+961-' + phone[:2] + '-' + phone[2:5] + '-' + phone[5:]
    return phone
