import asyncio
import nest_asyncio
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from telegram import Update, ReplyKeyboardMarkup

BOT_TOKEN = "7570785487:A^^^^^^^^^^^^^KVuURZY"
ADMIN_ID = 12345678  # آیدی عددی خودت

# تابع پردازش پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if update.message.text == "شروع ✅":
        message = (
            f"🆕 کاربر جدید:\n\n"
            f"👤 نام: {user.full_name}\n"
            f"🆔 آیدی عددی: {user.id}\n"
            f"🔤 زبان: {user.language_code}\n"
            f"📎 یوزرنیم: @{user.username if user.username else 'ندارد'}"
        )

        await update.message.reply_text("اطلاعاتت ثبت شد ✅")

        await context.bot.send_message(chat_id=ADMIN_ID, text=message)
    else:
        await update.message.reply_text("لطفاً روی دکمه 'شروع ✅' بزن.")

# تابع وقتی کسی بات رو باز کرد
async def send_start_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup([["شروع ✅"]], resize_keyboard=True)
    await update.message.reply_text("برای شروع روی دکمه زیر کلیک کن 👇", reply_markup=keyboard)

# اجرای ربات
async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # وقتی اولین بار ربات باز میشه یا start زده میشه
    app.add_handler(MessageHandler(filters.COMMAND, send_start_keyboard))
    # وقتی دکمه رو میزنه
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
