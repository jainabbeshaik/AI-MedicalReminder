import sqlite3
import requests
import schedule
import time
from datetime import datetime

BOT_TOKEN = "8849847983:AAHjOANY11Uc-73g-QMVyJq4ZMSy77BQ6gA"
CHAT_ID = "1626598261"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)

def check_reminders():
    current_time = datetime.now().strftime("%H:%M")

    conn = sqlite3.connect("medical.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT medicine_name, dosage FROM medicines WHERE medicine_time=?",
        (current_time,)
    )

    medicines = cursor.fetchall()
    conn.close()

    for medicine in medicines:
        message = f"""
💊 Medical Reminder

Medicine: {medicine[0]}
Dosage: {medicine[1]}

Please take your medicine now.
"""
        send_telegram(message)

schedule.every(1).minutes.do(check_reminders)

print("reminder service started")
while True:
    schedule.run_pending()
    time.sleep(1)