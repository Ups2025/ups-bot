from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3

TOKEN = "вставь_сюда_свой_токен_от_BotFather"

conn = sqlite3.connect("referrals.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    invited_by INTEGER
)""")
conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = context.args
    invited_by = int(args[0]) if args else None

    conn = sqlite3.connect("referrals.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user.id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, username, invited_by) VALUES (?, ?, ?)",
                       (user.id, user.username, invited_by))
        conn.commit()

    referral_link = f"https://t.me/{context.bot.username}?start={user.id}"
    await update.message.reply_text(f"Привет, {user.first_name}!
Вот твоя реферальная ссылка:
{referral_link}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Просто отправь /start")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()
