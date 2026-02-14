BASE_URL = "https://api.open-meteo.com/v1/forecast"

LATITUDE = 45.8150
LONGITUDE = 15.9819
TIMEZONE = "Europe/Berlin"

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

weather_icons = {
    0: "🔆",
    1: "🔆",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    53: "🌦️",
    55: "🌦️",
    56: "🌧️❄️",
    57: "🌧️❄️",
    61: "🌧️",
    63: "🌧️",
    65: "🌧️",
    66: "🌧️❄️",
    67: "🌧️❄️",
    71: "❄️",
    73: "❄️",
    75: "❄️",
    77: "❄️",
    80: "🌧️",
    81: "🌧️",
    82: "🌧️",
    85: "❄️",
    86: "❄️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️",
}


def wind_direction_to_compass(degrees):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(degrees / 45) % 8]


def get_temp_color(temp: int) -> str:
    if temp > 35:
        return "deep_pink4"
    elif temp >= 30:
        return "red"
    elif temp >= 25:
        return "bright_red"
    elif temp >= 20:
        return "dark_orange3"
    elif temp >= 15:
        return "orange3"
    elif temp >= 10:
        return "yellow"
    elif temp >= 5:
        return "green"
    elif temp >= 0:
        return "dark_turquoise"
    elif temp >= -5:
        return "cyan"
    elif temp >= -15:
        return "dodger_blue1"
    else:
        return "blue"


def get_humidity_color(humidity: int) -> str:
    if humidity > 75:
        return "dodger_blue2"
    elif humidity >= 50:
        return "dodger_blue1"
    elif humidity >= 25:
        return "deep_sky_blue1"
    else:
        return "bright_cyan"


def get_wind_color(speed: float) -> str:
    if speed >= 60:
        return "red"
    elif speed >= 40:
        return "orange3"
    elif speed >= 25:
        return "yellow"
    elif speed >= 10:
        return "green"
    else:
        return "cyan"
