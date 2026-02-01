import requests
import time
from rich import print
from shared import BASE_URL, LATITUDE, LONGITUDE, TIMEZONE, weather_codes, wind_direction_to_compass

params = {
    'latitude': LATITUDE,
    'longitude': LONGITUDE,
    'timezone': TIMEZONE,
    'current': ['temperature_2m', 'weather_code', 'relative_humidity_2m', 'wind_speed_10m', 'wind_gusts_10m', 'wind_direction_10m'],
}

response = requests.get(BASE_URL, params=params)
data = response.json()

temperature = round(data['current']['temperature_2m'])
current_weather = weather_codes[data['current']['weather_code']]
humidity = data['current']['relative_humidity_2m']
wind_speed = data['current']['wind_speed_10m']
wind_gust = data['current']['wind_gusts_10m']
wind_direction = wind_direction_to_compass(data['current']['wind_direction_10m'])

current_time = time.strftime('%H:%M')

print(f'Zagreb [{current_time}] [cyan]{temperature}c[/cyan] | [cyan]{current_weather}[/cyan] | '
      f'Vlaga [cyan]{humidity}%[/cyan] | Vjetar [cyan]{wind_speed}/{wind_gust}[/cyan] km/h [cyan]{wind_direction}[/cyan]\n')
