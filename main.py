import os
import smtplib
from email.message import EmailMessage

import requests

RAIN_KEYWORDS = ("rain", "drizzle", "thunderstorm", "snow", "shower")


def should_send_alert(*weather_states):
    combined_text = " ".join(weather_states).lower()
    return any(keyword in combined_text for keyword in RAIN_KEYWORDS)


def main():
    lat = os.environ.get("LAT")
    longitude = os.environ.get("LONG")
    api_id = os.environ.get("ID")
    mail = os.environ.get("MAIL")
    password = os.environ.get("PSW")
    to_mail = os.environ.get("TO_MAIL")

    if not all([lat, longitude, api_id, mail, password, to_mail]):
        raise RuntimeError("Missing required environment variables")

    parameters = {
        "appid": api_id,
        "lat": float(lat),
        "lon": float(longitude),
    }

    response = requests.get(
        url="https://api.openweathermap.org/data/2.5/forecast",
        params=parameters,
        timeout=10,
    )
    response.raise_for_status()

    weather_data = response.json()
    weather_state = weather_data["list"][0]["weather"][0]["description"]
    future_weather_state = weather_data["list"][4]["weather"][0]["description"]

    if not should_send_alert(weather_state, future_weather_state):
        print("No weather alert needed.")
        return

    message = EmailMessage()
    message["From"] = mail
    message["To"] = to_mail
    message["Subject"] = "Weather Alert in Berlin"
    message.set_content(
        f"Hello, Jackson! \nHere is the weather forecast for today :3\n"
        f"There will be {weather_state} in approximately one hour.\n"
        f"There is a chance of {future_weather_state} later today.\n\n"
        "With love,\n\n"
        "Your weather forecaster Lara"
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(mail, password)
        smtp.send_message(message)

        message["To"] = mail
        smtp.send_message(message)


if __name__ == "__main__":
    main()
