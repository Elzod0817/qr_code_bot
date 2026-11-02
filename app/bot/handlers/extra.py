from aiogram import Router, F
from aiogram.types import Message, CallbackQuery  # <-- CallbackQuery shu yerga qo'shildi
from aiogram.filters import Command
from app.core.config import settings
from app.database.repositories.user_repo import get_users_count
from app.database.repositories.history_repo import get_history_count, get_user_history

# --- Settings uchun yangi importlar ---
from app.bot.keyboards.inline import get_settings_keyboard
from app.database.database import AsyncSessionLocal
from app.database.models.history import History
from sqlalchemy import delete

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    # Faqat admin kira olishi uchun tekshiruv
    if message.from_user.id != settings.ADMIN_ID:
        return
    
    users_count = await get_users_count()
    qrs_count = await get_history_count()
    
    text = (
        "📊 <b>Admin Panel</b>\n\n"
        f"👥 Jami ro'yxatdan o'tganlar: {users_count} ta\n"
        f"🔲 Yaratilgan jami QR kodlar: {qrs_count} ta"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "📜 Mening QR kodlarim")
async def show_history(message: Message):
    history = await get_user_history(message.from_user.id)
    
    if not history:
        await message.answer("Siz hali birorta ham QR kod yaratmagansiz.")
        return
        
    text = "📜 <b>Sizning oxirgi 5 ta QR kodingiz:</b>\n\n"
    for i, record in enumerate(history, 1):
        text += f"{i}. {record.qr_data[:30]}... ({record.created_at.strftime('%Y-%m-%d %H:%M')})\n"
        
    await message.answer(text, parse_mode="HTML")
@router.message(F.text == "⚙️ Settings")
async def process_settings(message: Message):
    text = (
        "⚙️ <b>Sozlamalar</b>\n\n"
        "Quyidagi menyu orqali bot tilini o'zgartirishingiz yoki saqlangan QR kodlar tarixingizni tozalashingiz mumkin:"
    )
    await message.answer(text, reply_markup=get_settings_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "clear_history")
async def process_clear_history(callback: CallbackQuery):
    async with AsyncSessionLocal() as session:
        await session.execute(delete(History).where(History.telegram_id == callback.from_user.id))
        await session.commit()
    
    await callback.message.edit_text("✅ Tarixingiz muvaffaqiyatli tozalandi!")
    await callback.answer()

@router.callback_query(F.data.startswith("setlang_"))
async def process_set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    # Kelajakda bu yerni user_repo orqali bazadagi tilni o'zgartiradigan qilasiz
    await callback.message.edit_text(f"✅ Til o'zgartirildi: {lang.upper()}")
    await callback.answer()
@router.message(F.text == "ℹ️ Help")
async def process_help(message: Message):
    text = (
        "ℹ️ <b>Yordam bo'limi</b>\n\n"
        "Botdan foydalanish bo'yicha qisqacha qo'llanma:\n"
        "1. <b>🆕 Create QR Code</b> tugmasini bosing.\n"
        "2. O'zingizga kerakli QR kod turini tanlang (Matn, Wi-Fi, Telefon, Email).\n"
        "3. So'ralgan ma'lumotni yuboring.\n"
        "4. Tayyor bo'lgan QR kodning rangini o'zgartiring yoki o'rtasiga rasm (logo) joylang!\n\n"
        "Barcha yaratilgan QR kodlaringiz tarixda saqlanib boradi."
    )
    await message.answer(text, parse_mode="HTML")