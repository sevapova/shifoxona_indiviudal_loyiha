import requests
import os
from dotenv import load_dotenv

load_dotenv()

def check_bot():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN not found in .env")
        return
    
    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("ok"):
            bot_info = data["result"]
            print(f"Bot info: {bot_info}")
            print(f"Actual Username: @{bot_info.get('username')}")
        else:
            print(f"Error from Telegram: {data}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    check_bot()
