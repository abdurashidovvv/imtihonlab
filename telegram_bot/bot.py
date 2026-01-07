from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import requests
from config import TELEGRAM_TOKEN, BACKEND_URL

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
            name = text
            context.user_data["name"] = name

            # Telefon raqam tugmasi
            button = KeyboardButton(text="Telefon raqamni yuborish", request_contact=True)
            markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(
                "Rahmat! Telefon raqamingizni yuboring.",
                reply_markup=markup
            )
            return
        # Agar foydalanuvchi boshqa matn yozsa
        await update.message.reply_text("Noma’lum buyruq. Iltimos, /start ni bosing.")
        return

    # Foydalanuvchi telefon raqam yubordi (contact)
    if update.message and update.message.contact:
        phone = update.message.contact.phone_number
        name = context.user_data.get("name")
        telegram_id = user_id

        # API ga yuborish
        response = requests.post(f"{BACKEND_URL}/auth/telegram/", json={
            "telegram_id": telegram_id,
            "name": name,
            "phone": phone
        })

        if response.status_code == 200:
            data = response.json()
            sessions[user_id] = data['access']

            # Inline button yaratish
            inline_keyboard = [[InlineKeyboardButton(f"{name} ({phone})", callback_data="account_selected")]]
            inline_markup = InlineKeyboardMarkup(inline_keyboard)

            # Telefon raqam tugmasini olib tashlash
            await update.message.reply_text(
                "Imtihonlab dasturiga xush kelibsiz!",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await update.message.reply_text("Xatolik! Qayta urinib ko‘ring.")

        keyboard_buttons = [["Tests", "Attempts"]]
        markup = ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True, one_time_keyboard=True)

        await update.message.reply_text(
            "Quyidagi opsiyalardan birini tanlang:",
            reply_markup=markup
        )
        return

    # Boshqa holatlar
    if update.message:
        await update.message.reply_text("Noma’lum buyruq. Iltimos, /start ni bosing.")


# Inline button bosilganda
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "account_selected":
        await query.edit_message_text("Ajoyib! Endi /test buyrug'i orqali testlarni olishingiz mumkin.")


# Testlarni olish
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    token = sessions.get(user_id)
    if not token:
        await update.message.reply_text("Avval /start ni bosing va ismingizni yuboring, keyin telefon raqamini yuboring.")
        return

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/tests/", headers=headers)

    if response.status_code == 200:
        tests = response.json()
        text = "Mavjud testlar:\n"
        for t in tests:
            text += f"- {t['id']}: {t['title']} ({t['type']})\n"
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Testlarni olishda xatolik yuz berdi.")


# Application
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("test", test))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.CONTACT, handle_message))
app.add_handler(CallbackQueryHandler(button_callback))

app.run_polling()
