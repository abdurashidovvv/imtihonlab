from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests

BACKEND_URL = "http://127.0.0.1:8000/api"  # backend url

sessions = {}
waiting_for_name = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    waiting_for_name.add(user_id)
    await update.message.reply_text("Salom! Iltimos, ismingizni kiriting.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Foydalanuvchi matn yubordi (ism)
    if update.message and update.message.text:
        text = update.message.text.strip()
        if user_id in waiting_for_name:
            waiting_for_name.remove(user_id)
            context.user_data["name"] = text

            # Telefon raqam tugmasi
            button = KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
            markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text("Rahmat! Telefon raqamingizni yuboring.", reply_markup=markup)
            return

    # Foydalanuvchi telefon raqam yubordi (contact)
    if update.message and update.message.contact:
        phone = update.message.contact.phone_number
        name = context.user_data.get("name")
        telegram_id = user_id

        # API ga yuborish
        response = requests.post(f"{BACKEND_URL}/auth/register/", json={
            "telegram_id": telegram_id,
            "name": name,
            "phone_number": phone
        })

        if response.status_code == 200:
            data = response.json()
            sessions[user_id] = data["access"]
            await update.message.reply_text(f"Ro'yxatdan o'tdingiz!\n\nIsm: {name}\nTelefon: {phone}", reply_markup=ReplyKeyboardRemove())
        else:
            await update.message.reply_text("Xatolik! Telefon raqam yoki ism noto'g'ri. Qayta urinib ko‘ring.")

# Inline buttonlar
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "account_selected":
        await query.edit_message_text("Endi /test orqali testlarni olishingiz mumkin.")

# Application
app = ApplicationBuilder().token("7728088936:AAHjlFJjPEF3HGoTbk2pVBGiVz5uMi8OyEY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.CONTACT, handle_message))
app.add_handler(CallbackQueryHandler(button_callback))

app.run_polling()
