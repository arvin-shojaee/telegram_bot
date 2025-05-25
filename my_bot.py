from telegram import Update, ChatMember, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import logging

# فعال‌سازی لاگ‌ها
logging.basicConfig(level=logging.INFO)

# لیست کلمات بد
bad_words = ['گوه', 'بیشعور', 'احمق', 'عوضی', 'ناموس', 'آشغال' , 'کثافت' , 'حروم' , 'حمال' ,]

# دیکشنری اخطارها
warnings = {}  # user_id: count

# --- دستورات اصلی ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup([['/start', '/help', '/about']], resize_keyboard=True)
    await update.message.reply_text("سلام! خوش اومدی 😄", reply_markup=keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup([['/start', '/help', '/about']], resize_keyboard=True)
    await update.message.reply_text("📌 دستورات:\n/start - شروع\n/help - راهنما\n/about - درباره ما", reply_markup=keyboard)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup([['/start', '/help', '/about']], resize_keyboard=True)
    await update.message.reply_text("من فقط یه بات ساده هستم 😁 ساخته شده توسط @arvin_py", reply_markup=keyboard)

# --- بررسی فحش ---

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    for word in bad_words:
        if word in text:
            await update.message.reply_text("فحش نده مرتیکه 🐄", reply_to_message_id=update.message.message_id)
            await update.message.delete()
            break

# --- دستور /warn ---

async def warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("ریپلای کن بعد بزن /warn")
        return

    admin_status = await context.bot.get_chat_member(update.message.chat_id, update.message.from_user.id)
    if admin_status.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await update.message.reply_text("میخوای مثل من باشی؟ موفق باشی😂")
        return

    target_user = update.message.reply_to_message.from_user
    user_id = target_user.id
    chat_id = update.message.chat_id

    warnings[user_id] = warnings.get(user_id, 0) + 1
    count = warnings[user_id]

    await update.message.reply_text(f"⚠️ {target_user.full_name} اخطار گرفت. اخطار فعلی: {count}/3")

    if count >= 3:
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            await update.message.reply_text(f"🚫 {target_user.full_name} با 3 اخطار بن شد.")
            del warnings[user_id]
        except Exception as e:
            await update.message.reply_text(f"خطا در بن کردن: {e}")

# --- دستور /resetwarn ---

async def reset_warn_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("باید روی پیام طرف ریپلای کنی بعد بزنی /resetwarn")
        return

    admin_status = await context.bot.get_chat_member(update.message.chat_id, update.message.from_user.id)
    if admin_status.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        await update.message.reply_text("فقط ادمین‌ها می‌تونن اخطار رو پاک کنن!")
        return

    target_user = update.message.reply_to_message.from_user
    user_id = target_user.id

    if warnings.get(user_id):
        del warnings[user_id]
        await update.message.reply_text(f"✅ اخطارهای {target_user.full_name} پاک شد.")
    else:
        await update.message.reply_text(f"{target_user.full_name} اخطاری نداشت.")

# --- بن با /ban ریپلای شده ---

async def keyword_ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return

    member = await update.effective_chat.get_member(update.effective_user.id)
    if member.status not in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]:
        return

    if "/ban" in update.message.text.lower():
        user_to_ban = update.message.reply_to_message.from_user
        try:
            await update.effective_chat.ban_member(user_to_ban.id)
            await update.message.reply_text(f"{user_to_ban.full_name} بن شد ❌")
        except Exception as e:
            await update.message.reply_text(f"خطا در بن کردن: {e}")

# --- اجرای بات ---

if __name__ == '__main__':
    app = ApplicationBuilder().token("7193575457:AAGOVsWLc40******5Bphl0VOinU").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("warn", warn_command))
    app.add_handler(CommandHandler("resetwarn", reset_warn_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), check_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, keyword_ban))

    app.run_polling()
