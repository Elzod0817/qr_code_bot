from aiogram.fsm.state import State, StatesGroup

class GenerateQR(StatesGroup):
    waiting_for_type = State()
    waiting_for_text = State()
    waiting_for_wifi_ssid = State()
    waiting_for_wifi_pass = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_logo = State() # Yangi holat