import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
load_dotenv()
city = "Thailand,Bangkok"
api_key = os.getenv("API_KEY_OPENWEATHERMAP")
webhook_url = os.getenv("DISCORD_WEBHOOK")
data_locations = []
try:
    with open("./locations.json", "r", encoding="utf-8") as f:
        data_locations = json.load(f)
        logging.info("Load file locations.json success")
except FileNotFoundError:
    logging.error("Fail to load file locations.json")

def greeting():
    now = datetime.now()
    hour = now.hour
    greeting_emoji = "❓"
    if 5 <= hour < 11:
        time_period = "เช้า"
        greeting_emoji = "🌅"
    elif 11 <= hour < 15:
        time_period = "กลางวัน"
        greeting_emoji = "☀️"
    elif 15 <= hour < 18:
        time_period = "เย็น"
        greeting_emoji = "🌇"
    else:
        time_period = "มืด"
        greeting_emoji = "🌙"

    greeting = (
        f"👋 สวัสดียาม{time_period} {greeting_emoji}\n"
        f"\n"
    )
    payload = {
                "content": greeting
    }
    requests.post(webhook_url, json=payload)

def send_webnook(log_time):
    for i in data_locations:
        location = i["location"]
        lat = i["lat"]
        lon = i["lon"]
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=th"

        response = requests.get(weather_url)
        data = response.json()
        if data.get("cod") != 200:
            logging.error(f"[{log_time}] ❌ {data.get('message')}")
        else:
            weather_description = data['weather'][0]['description']
            weather = data["weather"][0]["main"].lower()
            emoji = "❓"
            if weather == "clear":
                emoji = "☀️"
            elif weather == "clouds":
                emoji = "☁️"
            elif weather == "rain":
                emoji = "🌧️"
            elif weather == "thunderstorm":
                emoji = "⛈️"
            elif weather == "drizzle":
                emoji = "🌦️"
            elif weather == "snow":
                emoji = "❄️"
            elif weather == "mist" or weather == "fog":
                emoji = "🌫️"
            else:
                emoji = "🌍"

            temp = data['main']['temp']
            humidity = data['main']['humidity']
            speed = data['wind']['speed']
            deg = data['wind']['deg']

            message = (
                f"📍 สภาพอากาศวันนี้ที่ **{location}**\n"
                f"{emoji} สภาพอากาศ: {weather_description}\n"
                f"🌡 อุณหภูมิ: {temp}°C\n"
                f"💧 ความชื้น: {humidity}%\n"
                f"🌬️ ลมเฉลี่ย: {speed * 3.6:.1f} km/h (ทิศ {deg}°)\n"
                f"🕒 เวลาส่งข้อมูล: {log_time}\n"
                f"===================================================\n"
            )
            payload = {
                "content": message
            }
            res = requests.post(webhook_url, json=payload)
            if res.status_code == 204:
                logging.info(f"[{log_time}] ✅ ส่งข้อความสำเร็จ: {location}")
            else:
                logging.error(f"[{log_time}] ❌ ส่งไม่สำเร็จ: {location} | Status Code: {res.status_code}")


def job():
        log_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        logging.info(f"Hook {log_time}")
        greeting()
        send_webnook(log_time)
        
if __name__ == "__main__":
    logging.info("Cronjob Start")
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour='0,6,12,18', minute=0, misfire_grace_time=3600)
    scheduler.start()
