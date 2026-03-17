import re


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    pattern = r"^(\+7|8)\d{10}$"
    return re.match(pattern, ''.join(filter(str.isdigit, phone))) is not None and len(phone) <= 12


def validate_name(name: str) -> bool:
    return name.strip().replace(" ", "").isalpha() and len(name.strip()) >= 2