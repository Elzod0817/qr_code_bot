from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🆕 Create QR Code")],
            [KeyboardButton(text="📜 Mening QR kodlarim")],
            [KeyboardButton(text="⚙️ Settings"), KeyboardButton(text="ℹ️ Help")]
        ],
        resize_keyboard=True
    )