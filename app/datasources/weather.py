import pyowm
import pytz
from datetime import datetime

def convert_time(timestamp_utc):
    local_timezone = pytz.timezone('America/New_York')
    return datetime.fromtimestamp(timestamp_utc, tz=pytz.utc).astimezone(local_timezone)

def key_data(w):
    return {
        'time': convert_time(w.reference_time()),
        'status': w.status,
        'temperature': round(w.temperature('fahrenheit')['temp']),
        'humidity': w.humidity,
        'rainfall': w.rain['3h'] if w.rain else 0,    
        'snowfall': w.snow['3h'] if w.snow else 0
    }

def get_weather_data():
    owm = pyowm.OWM('6cbe1929ba54ad7adad77f7306bfb812')
    location = 'Princeton, NJ, US'

    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(location)

    data = []

    w = observation.weather
    data.append(key_data(w))

    forecast = mgr.forecast_at_place(location, '3h')
    for weather in forecast.forecast:
        data.append(key_data(weather))

    return data
