import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
GEMINI_KEY = os.environ['GEMINI_KEY']

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ael'vori here 👑 Ask me anything.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Flask for Render health check
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Bot is alive"

def run_flask():
    flask_app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask).start()

print("Bot is alive. Ael'vori thal enu")
app.run_polling()
