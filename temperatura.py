import requests
import time
from datetime import datetime, timedelta
from rich import print
from shared import (
    BASE_URL, LATITUDE, LONGITUDE, TIMEZONE,
    weather_icons, wind_direction_to_compass,
    get_temp_color, get_humidity_color, get_wind_color,
)

params = {
    'latitude': LATITUDE,
    'longitude': LONGITUDE,
    'timezone': TIMEZONE,
    'current': ['temperature_2m', 'weather_code', 'relative_humidity_2m', 'wind_speed_10m', 'wind_gusts_10m', 'wind_direction_10m'],
    'daily': ['sunrise', 'sunset']
    
}

try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status() # checks for HTTP errors
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f'error occured: {e}')
    raise

def sun_rs(sunrises, sunsets):
    sunrise_today = datetime.fromisoformat(sunrises[0])
    sunset_today = datetime.fromisoformat(sunsets[0])
    d = sunset_today - sunrise_today
    hours, minutes = divmod(int(d.total_seconds() // 60), 60)
    return sunrise_today.strftime('%H:%M'), sunset_today.strftime('%H:%M'), f'{hours:02d}:{minutes:02d}'



temperature = round(data['current']['temperature_2m'])
weather_icon = weather_icons[data['current']['weather_code']]
humidity = data['current']['relative_humidity_2m']
wind_speed = data['current']['wind_speed_10m']
wind_gust = data['current']['wind_gusts_10m']
wind_direction = wind_direction_to_compass(data['current']['wind_direction_10m'])
sunrise = data['daily']['sunrise']
sunset = data['daily']['sunset']
sunrise_time, sunset_time, day_length = sun_rs(sunrise, sunset)

current_time = time.strftime('%H:%M')

tc = get_temp_color(temperature)
hc = get_humidity_color(humidity)
wc = get_wind_color(wind_speed)
gc = get_wind_color(wind_gust)

print(f'Zagreb [{current_time}] {weather_icon} [{tc}]{temperature}c[/{tc}] | '
      f'Vlaga [{hc}]{humidity}%[/{hc}] | Vjetar [{wc}]{wind_speed}[/{wc}]/[{gc}]{wind_gust}[/{gc}] km/h [{wc}]{wind_direction}[/{wc}] | '
      f'Dan traje {day_length} {sunrise_time}/{sunset_time}\n')