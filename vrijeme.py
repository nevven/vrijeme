import sys
import requests
from datetime import datetime
from rich.table import Table
from rich.console import Console
from rich import box
from shared import (
    BASE_URL, LATITUDE, LONGITUDE, TIMEZONE,
    weather_icons, get_temp_color,
)

console = Console()

# Parse CLI argument: no arg = today hourly, 7 = daily summary, 7f = full hourly per day
mode = "today"
if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == "7":
        mode = "summary"
    elif arg == "7f":
        mode = "full"
    else:
        console.print(f"[red]Invalid argument: {arg}. Use: vrijeme [7|7f][/red]")
        sys.exit(1)


def fetch_hourly():
    """Fetch and display hourly forecast for today."""
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'timezone': TIMEZONE,
        'forecast_days': 1,
        'hourly': ['temperature_2m', 'weather_code'],
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    time_response = data['hourly']['time']
    temp_response = data['hourly']['temperature_2m']
    code_response = data['hourly']['weather_code']

    # Every other hour
    time_even_display = [datetime.fromisoformat(i).strftime('%H:%M') for i in time_response[::2]]
    time_even_dt = [datetime.fromisoformat(i) for i in time_response[::2]]
    temp_even = [round(i) for i in temp_response[::2]]
    icons_even = [weather_icons[c] for c in code_response[::2]]

    # Highlight closest time slot
    now = datetime.now()
    time_min_difference = min(time_even_dt, key=lambda t: abs(now - t)).strftime('%H:%M')
    time_display = [f'[green]{t}[/green]' if t == time_min_difference else t for t in time_even_display]

    # Color code values
    temp_color = [f'[{get_temp_color(t)}]{t}°[/{get_temp_color(t)}]' for t in temp_even]

    table = Table(show_header=False, border_style="grey54", show_lines=True, box=box.ROUNDED)
    table.add_row(*time_display)
    table.add_row(*temp_color)
    table.add_row(*icons_even)

    console.print(table)


def get_precip_color(mm):
    if mm >= 5:
        return "dodger_blue2"
    elif mm > 0:
        return "dodger_blue1"
    return None


def fetch_summary():
    """Fetch and display 7-day summary: one column per day."""
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'timezone': TIMEZONE,
        'forecast_days': 7,
        'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum', 'weather_code'],
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    dates = data['daily']['time']
    temp_max = data['daily']['temperature_2m_max']
    temp_min = data['daily']['temperature_2m_min']
    precipitation = data['daily']['precipitation_sum']
    codes = data['daily']['weather_code']

    day_names = {0: 'Pon', 1: 'Uto', 2: 'Sri', 3: 'Čet', 4: 'Pet', 5: 'Sub', 6: 'Ned'}

    day_labels = []
    temp_display = []
    weather_display = []

    for i, date_str in enumerate(dates):
        dt = datetime.fromisoformat(date_str)
        day_label = f"{day_names[dt.weekday()]} {dt.strftime('%d.%m')}"

        if dt.weekday() >= 5:  # Weekend
            day_labels.append(f'[green]{day_label}[/green]')
        else:
            day_labels.append(day_label)

        hi = round(temp_max[i])
        lo = round(temp_min[i])
        hi_color = get_temp_color(hi)
        lo_color = get_temp_color(lo)
        temp_display.append(f'[{lo_color}]{lo}°[/{lo_color}][white] | [/white][{hi_color}]{hi}°[/{hi_color}]')

        icon = weather_icons[codes[i]]
        rain = precipitation[i]
        color = get_precip_color(rain)
        if color:
            weather_display.append(f'{icon} [{color}]{rain:.1f}mm[/{color}]')
        else:
            weather_display.append(f'{icon} [dim]{rain:.1f}mm[/dim]')

    table = Table(show_header=False, border_style="grey54", show_lines=True, box=box.ROUNDED)
    for _ in range(7):
        table.add_column(justify="center")
    table.add_row(*day_labels)
    table.add_row(*temp_display)
    table.add_row(*weather_display)

    console.print(table)


def fetch_daily(days):
    """Fetch and display hourly forecast per day for N days."""
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'timezone': TIMEZONE,
        'forecast_days': days,
        'hourly': ['temperature_2m', 'weather_code'],
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    time_response = data['hourly']['time']
    temp_response = data['hourly']['temperature_2m']
    code_response = data['hourly']['weather_code']

    day_names = {0: 'Pon', 1: 'Uto', 2: 'Sri', 3: 'Čet', 4: 'Pet', 5: 'Sub', 6: 'Ned'}

    # Group data by day (24 hours per day, take every other = 12 per day)
    hours_per_day = 24
    for day_index in range(days):
        start = day_index * hours_per_day
        end = start + hours_per_day

        day_times = time_response[start:end:2]
        day_temps = temp_response[start:end:2]
        day_codes = code_response[start:end:2]

        dt = datetime.fromisoformat(time_response[start])
        day_label = day_names[dt.weekday()]

        # Time row
        time_display = [datetime.fromisoformat(t).strftime('%H:%M') for t in day_times]

        # First column is day label (weekend in green)
        if dt.weekday() >= 5:
            day_col = f'[green]{day_label}[/green]'
        else:
            day_col = day_label

        # Color coded rows
        temp_even = [round(t) for t in day_temps]
        temp_color = [f'[{get_temp_color(t)}]{t}°[/{get_temp_color(t)}]' for t in temp_even]
        icons = [weather_icons[c] for c in day_codes]

        table = Table(show_header=False, border_style="grey54", show_lines=True, box=box.ROUNDED)
        table.add_row(day_col, *time_display)
        table.add_row('Temp', *temp_color)
        table.add_row('Prog', *icons)

        console.print(table)


if mode == "today":
    fetch_hourly()
elif mode == "summary":
    fetch_summary()
elif mode == "full":
    fetch_daily(7)
