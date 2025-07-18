import requests
from bs4 import BeautifulSoup
import time
import logging

# Telegram credentials
TOKEN = "7604446870:AAHpQRJQfMKCPsCt6CG86hPMZtsh24jevts"
CHAT_ID = "719052415"

# URLs to scrape
URLS = {
    "soccer": "https://inforadar.live/#/dashboard/soccer/live",
    "basketball": "https://inforadar.live/#/dashboard/basketball/live"
}

# Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": text}
        requests.post(url, data=data)
    except Exception as e:
        logging.error(f"Telegram error: {e}")

def scrape_inforadar():
    results = []
    for sport, url in URLS.items():
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                scripts = soup.find_all("script")
                for script in scripts:
                    if "Alg.1" in script.text:
                        try:
                            text = script.text
                            if "Alg.1" in text:
                                results.append((sport, text))
                        except:
                            pass
            else:
                logging.warning(f"Failed to load {sport}: {response.status_code}")
        except Exception as e:
            logging.error(f"Scrape error ({sport}): {e}")
    return results

def main():
    logging.info("Bot started successfully.")
    while True:
        try:
            logging.info("Checking Inforadar data...")
            data = scrape_inforadar()

            if not data:
                logging.info("No data found yet.")
            else:
                for sport, raw in data:
                    lines = raw.splitlines()
                    for line in lines:
                        if "Alg.1" in line:
                            try:
                                value = float(line.split("Alg.1")[1].split(":")[1].strip().replace(",", "."))
                                if value > 1.00 or value < -1.00:
                                    message = f"🔥 {sport.upper()} ALERT!\nValue: {value}"
                                    logging.info(message)
                                    send_telegram_message(message)
                            except:
                                continue

        except Exception as e:
            logging.error(f"Main loop error: {e}")

        time.sleep(60)

if __name__ == "__main__":
    main()
