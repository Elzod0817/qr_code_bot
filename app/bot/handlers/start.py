from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from app.bot.keyboards.inline import get_language_keyboard
from app.bot.keyboards.reply import get_main_menu
from app.database.repositories.user_repo import get_or_create_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    # Foydalanuvchini bazaga yozamiz
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
    
    welcome_text = f"Salom, {user.full_name}! QR Studio Bot'ga xush kelibsiz. Iltimos, tilni tanlang:"
    await message.answer(welcome_text, reply_markup=get_language_keyboard())

@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    
    await callback.message.delete()
    await callback.message.answer(
        "Til muvaffaqiyatli tanlandi! Endi botdan to'liq foydalanishingiz mumkin.",
        reply_markup=get_main_menu()
    )
    await callback.answer()