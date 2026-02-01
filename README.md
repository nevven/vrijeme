# Vrijeme

CLI weather tools for Zagreb using [Open-Meteo API](https://open-meteo.com/).

## Scripts

**temperatura.py** - Current weather snapshot: temperature, conditions, humidity, wind.

**vrijeme.py** - Forecast display with three modes:
- `vrijeme.py` - Today's hourly forecast (every 2h)
- `vrijeme.py 7` - 7-day summary (max/min temp, precipitation)
- `vrijeme.py 7f` - 7-day full hourly breakdown

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```
uv run temperatura.py
uv run vrijeme.py 7
```
