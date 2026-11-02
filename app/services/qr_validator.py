def format_wifi(ssid: str, password: str, hidden: bool = False) -> str:
    """Wi-Fi ulanish uchun standart QR format"""
    hidden_str = "true" if hidden else "false"
    return f"WIFI:T:WPA;S:{ssid};P:{password};H:{hidden_str};;"

def format_phone(phone: str) -> str:
    """Telefon raqam terish uchun standart QR format"""
    return f"tel:{phone}"

def format_email(email: str) -> str:
    """Elektron pochta yozish uchun standart QR format"""
    return f"mailto:{email}"

def format_location(lat: str, lng: str) -> str:
    """Geolokatsiya (xarita) uchun standart QR format"""
    return f"geo:{lat},{lng}"