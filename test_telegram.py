import requests

TOKEN = "7604446870:AAHpQRJQfMKCPsCt6CG86hPMZtsh24jevts"
CHAT_ID = "719052415"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    response = requests.post(url, data=data)
    return response.json()

print(send_telegram_message("✅ Test message: Bot is working!"))
print(send_telegram_message("✅ Railway bot started successfully!"))
