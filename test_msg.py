import os
import telebot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN or not ADMIN_ID:
    print("Error: BOT_TOKEN or ADMIN_ID not found in .env")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

try:
    print(f"Sending test message to {ADMIN_ID}...")
    bot.send_message(ADMIN_ID, "🚀 *Test xabari*\n\nTizim xabarnomalari sozlanganini tekshirish.", parse_mode="Markdown")
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
