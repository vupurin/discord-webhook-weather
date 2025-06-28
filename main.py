import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
city = "Thailand,Bangkok"
api_key = os.getenv("API_KEY_OPENWEATHERMAP")
locations = ["ประเวศ","อารีย์"]
lat = [13.7058,13.7725]
lon = [100.6783,100.5412]
webhook_url = os.getenv("DISCORD_WEBHOOK")


log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for i in range(len(locations)):
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat[i]}&lon={lon[i]}&appid={api_key}&units=metric&lang=th"

    response = requests.get(weather_url)
    data = response.json()
    if data.get("cod") != 200:
        print(f"[{log_time}] ❌ {data.get('message')}")
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
            f"📍 สภาพอากาศวันนี้ที่ **{locations[i]}**\n"
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
            print(f"[{log_time}] ✅ ส่งข้อความสำเร็จ: {locations[i]}")
        else:
            print(f"[{log_time}] ❌ ส่งไม่สำเร็จ: {locations[i]} | Status Code: {res.status_code}")