from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
        ]
    )
def get_qr_type_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔗 Text / URL", callback_data="qrtype_text"),
                InlineKeyboardButton(text="📶 Wi-Fi", callback_data="qrtype_wifi")
            ],
            [
                InlineKeyboardButton(text="📱 Phone", callback_data="qrtype_phone"),
                InlineKeyboardButton(text="📧 Email", callback_data="qrtype_email")
            ]
        ]
    )
def get_customization_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎨 Qora", callback_data="color_black"),
                InlineKeyboardButton(text="🔴 Qizil", callback_data="color_red")
            ],
            [
                InlineKeyboardButton(text="🔵 Ko'k", callback_data="color_blue"),
                InlineKeyboardButton(text="🟢 Yashil", callback_data="color_green")
            ],
            [InlineKeyboardButton(text="🖼 Logo yuklash", callback_data="action_add_logo")],
            [InlineKeyboardButton(text="✅ Yakunlash", callback_data="action_finish")]
        ]
    )
def get_settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="setlang_uz"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="setlang_en")
            ],
            [InlineKeyboardButton(text="🗑 Tarixni tozalash", callback_data="clear_history")]
        ]
    )