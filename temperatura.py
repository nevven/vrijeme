import requests
import time
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
}

response = requests.get(BASE_URL, params=params)
data = response.json()

temperature = round(data['current']['temperature_2m'])
weather_icon = weather_icons[data['current']['weather_code']]
humidity = data['current']['relative_humidity_2m']
wind_speed = data['current']['wind_speed_10m']
wind_gust = data['current']['wind_gusts_10m']
wind_direction = wind_direction_to_compass(data['current']['wind_direction_10m'])

current_time = time.strftime('%H:%M')

tc = get_temp_color(temperature)
hc = get_humidity_color(humidity)
wc = get_wind_color(wind_speed)
gc = get_wind_color(wind_gust)

print(f'Zagreb [{current_time}] {weather_icon} [{tc}]{temperature}c[/{tc}] | '
      f'Vlaga [{hc}]{humidity}%[/{hc}] | Vjetar [{wc}]{wind_speed}[/{wc}]/[{gc}]{wind_gust}[/{gc}] km/h [{wc}]{wind_direction}[/{wc}]\n')
