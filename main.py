import requests
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

# Replace with your OpenWeatherMap API key
#PI_KEY = 'your_openweathermap_api_key'

def get_weather():
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude=38.6273&longitude=-90.1979&hourly=temperature_2m,rain,visibility"
    response = requests.get(base_url)
    data = response.json()
    return data

def send_weather_update():
    weather_data = get_weather()
    temperature_celsius = weather_data["hourly"]["temperature_2m"][0]
    #wind_speed = weather_data["hourly"]["windspeed_10m"][0]
    temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

    weather_info = (
        f"Good Morning!\n"
        #put desired text her
        f"Let's look at the weather in the Lou Today!\n"
        f"Temp: {temperature_fahrenheit:.2f}F\n"
        # you can add more weather info here as you desire
       # f"Wind Speed: {wind_speed} m/s"

    )
    send_text_message(weather_info)

def main():
    scheduler = BlockingScheduler()
    scheduler.add_job(send_weather_update, 'cron', hour=10, minute=52)  # Schedule to run at 8:00 AM

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def send_text_message(body):
    client = Client()#api info here
    message = client.messages.create(
        body=body,
        from_='+18336991946',
        to='+16306772617'
    )
    print("Message sent!")

if __name__ == "__main__":
    main()
