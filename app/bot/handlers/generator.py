## Personal and social QR code bot
## Loyihani oxiriga yetamiz, Inshaalloh
## Malumot uchun: 02.11.2026
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from io import BytesIO

from app.bot.states.qr_states import GenerateQR
from app.bot.keyboards.inline import get_qr_type_keyboard, get_customization_keyboard
from app.services.qr_generator import generate_custom_qr
from app.services.qr_validator import format_wifi, format_phone, format_email
from app.database.repositories.history_repo import add_qr_history

router = Router()

@router.message(F.text == "🆕 Create QR Code")
async def start_qr_generation(message: Message, state: FSMContext):
    await message.answer("Qanday turdagi QR kod yaratmoqchisiz?", reply_markup=get_qr_type_keyboard())
    await state.set_state(GenerateQR.waiting_for_type)

@router.callback_query(GenerateQR.waiting_for_type, F.data.startswith("qrtype_"))
async def process_qr_type(callback: CallbackQuery, state: FSMContext):
    qr_type = callback.data.split("_")[1]
    await callback.message.delete()
    
    if qr_type == "text":
        await callback.message.answer("Matn yoki URL manzilni yuboring:")
        await state.set_state(GenerateQR.waiting_for_text)
    elif qr_type == "wifi":
        await callback.message.answer("Wi-Fi tarmog'ining nomini (SSID) yuboring:")
        await state.set_state(GenerateQR.waiting_for_wifi_ssid)
    elif qr_type == "phone":
        await callback.message.answer("Telefon raqamni yuboring (masalan, +998901234567):")
        await state.set_state(GenerateQR.waiting_for_phone)
    elif qr_type == "email":
        await callback.message.answer("Elektron pochta manzilini yuboring:")
        await state.set_state(GenerateQR.waiting_for_email)
        
    await callback.answer()

# Qayta ishlangan QR yuborish funksiyasi
async def send_qr_result(message: Message, data: str, caption: str, state: FSMContext):
    # Dastlabki holatni FSM xotirasida saqlab qolamiz (ranglar o'zgarishi uchun)
    await state.update_data(qr_payload=data, fg_color="black", logo_bytes=None)
    
    # Bazaga tarixni yozamiz
    await add_qr_history(telegram_id=message.from_user.id, qr_data=data)
    
    qr_stream = generate_custom_qr(data=data, fill_color="black")
    photo = BufferedInputFile(qr_stream.read(), filename="qr_code.png")
    
    await message.answer_photo(
        photo=photo, 
        caption=f"✅ Tayyor!\n\n{caption}\n\nQuyidagi menyu orqali QR kodni bezatishingiz mumkin:",
        reply_markup=get_customization_keyboard()
    )
    # E'tibor bering: bu yerda state.clear() qilmaymiz, jarayon davom etadi

# --- Asosiy ma'lumotlarni qabul qilish ---
@router.message(GenerateQR.waiting_for_text, F.text)
async def process_text(message: Message, state: FSMContext):
    await send_qr_result(message, message.text, "Matn/URL asosida QR yaratildi.", state)

@router.message(GenerateQR.waiting_for_phone, F.text)
async def process_phone(message: Message, state: FSMContext):
    await send_qr_result(message, format_phone(message.text), f"Telefon: {message.text}", state)

@router.message(GenerateQR.waiting_for_email, F.text)
async def process_email(message: Message, state: FSMContext):
    await send_qr_result(message, format_email(message.text), f"Email: {message.text}", state)

@router.message(GenerateQR.waiting_for_wifi_ssid, F.text)
async def process_wifi_ssid(message: Message, state: FSMContext):
    await state.update_data(ssid=message.text)
    await message.answer(f"✅ Tarmoq: {message.text}\n\nWi-Fi parolini yuboring:")
    await state.set_state(GenerateQR.waiting_for_wifi_pass)

@router.message(GenerateQR.waiting_for_wifi_pass, F.text)
async def process_wifi_pass(message: Message, state: FSMContext):
    data = await state.get_data()
    formatted_wifi = format_wifi(data.get("ssid"), message.text)
    await send_qr_result(message, formatted_wifi, f"Wi-Fi tarmog'i: {data.get('ssid')}", state)

# --- Kastomizatsiya (Rang va Logo) boshqaruvi ---
@router.callback_query(F.data.startswith("color_"))
async def process_color_change(callback: CallbackQuery, state: FSMContext):
    color = callback.data.split("_")[1]
    
    data = await state.get_data()
    payload = data.get("qr_payload")
    logo = data.get("logo_bytes")
    
    if not payload:
        await callback.answer("Xatolik: Ma'lumot topilmadi.", show_alert=True)
        return
        
    await state.update_data(fg_color=color)
    
    qr_stream = generate_custom_qr(data=payload, fill_color=color, logo_bytes=logo)
    photo = BufferedInputFile(qr_stream.read(), filename="qr_custom.png")
    
    # Rasmni eski xabarni tahrirlab o'zgartiramiz
    await callback.message.edit_media(
        media=photo.__dict__.get('_InputMediaPhoto', None) or {"type": "photo", "media": photo}, # aiogram 3.x media hack
        reply_markup=get_customization_keyboard()
    )
    # To'g'ri ishlashi uchun xabarni o'chirib qayta yozish ham mumkin:
    await callback.message.delete()
    await callback.message.answer_photo(photo=photo, caption="🎨 Rang o'zgartirildi!", reply_markup=get_customization_keyboard())
    await callback.answer()

@router.callback_query(F.data == "action_add_logo")
async def ask_for_logo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("🖼 QR kod markaziga joylash uchun logotip (rasm) yuboring:")
    await state.set_state(GenerateQR.waiting_for_logo)
    await callback.answer()

@router.message(GenerateQR.waiting_for_logo, F.photo)
async def process_logo(message: Message, state: FSMContext):
    data = await state.get_data()
    payload = data.get("qr_payload")
    color = data.get("fg_color", "black")
    
    # Rasmni xotiraga yuklab olamiz
    photo_file = await message.bot.download(message.photo[-1], destination=BytesIO())
    logo_bytes = photo_file.read()
    
    await state.update_data(logo_bytes=logo_bytes)
    
    qr_stream = generate_custom_qr(data=payload, fill_color=color, logo_bytes=logo_bytes)
    photo = BufferedInputFile(qr_stream.read(), filename="qr_logo.png")
    
    await message.answer_photo(
        photo=photo, 
        caption="🌟 Logotip muvaffaqiyatli qo'shildi!", 
        reply_markup=get_customization_keyboard()
    )

@router.callback_query(F.data == "action_finish")
async def finish_customization(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("✅ QR kodingiz tayyor! Undan bemalol foydalanishingiz mumkin.")
    await state.clear()
    await callback.answer()