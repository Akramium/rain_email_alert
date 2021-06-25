import requests
import smtplib
import os

END_POINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.getenv("OWM_API_KEY")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

parameters = {
    "lat": 42.331429,
    "lon": -83.045753,
    "appid": API_KEY,
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(url=END_POINT, params=parameters)
response.raise_for_status()
weather_data = response.json()["hourly"][:12]

will_rain = False

for hour_data in weather_data:
    weather_id = hour_data["weather"][0]["id"]
    if weather_id < 700:
        will_rain = True

if will_rain:
    print("Bring an Umbrella")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIL,
            to_addrs=TO_EMAIL,
            msg="Subject:It will rain\n\nBring an umbrella."
        )


