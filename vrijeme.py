import sys
import requests
from datetime import datetime
from rich.table import Table
from rich.console import Console
from rich import box
from shared import (
    BASE_URL, LATITUDE, LONGITUDE, TIMEZONE,
    weather_codes, get_temp_color, get_humidity_color,
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
        'hourly': ['temperature_2m', 'relative_humidity_2m'],
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    time_response = data['hourly']['time']
    temp_response = data['hourly']['temperature_2m']
    humidity_response = data['hourly']['relative_humidity_2m']

    # Every other hour
    time_even_display = [datetime.fromisoformat(i).strftime('%H:%M') for i in time_response[::2]]
    time_even_dt = [datetime.fromisoformat(i) for i in time_response[::2]]
    temp_even = [round(i) for i in temp_response[::2]]
    hum_even = [i for i in humidity_response[::2]]

    # Highlight closest time slot
    now = datetime.now()
    time_min_difference = min(time_even_dt, key=lambda t: abs(now - t)).strftime('%H:%M')
    time_display = [f'[green]{t}[/green]' if t == time_min_difference else t for t in time_even_display]

    # Color code values
    temp_color = [f'[{get_temp_color(t)}]{t}°[/{get_temp_color(t)}]' for t in temp_even]
    hum_colored = [f'[{get_humidity_color(h)}]{h}%[/{get_humidity_color(h)}]' for h in hum_even]

    table = Table(show_header=False, border_style="grey54", show_lines=True, box=box.ROUNDED)
    table.add_row(*time_display)
    table.add_row(*temp_color)
    table.add_row(*hum_colored)

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
        'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum'],
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    dates = data['daily']['time']
    temp_max = data['daily']['temperature_2m_max']
    temp_min = data['daily']['temperature_2m_min']
    precipitation = data['daily']['precipitation_sum']

    day_names = {0: 'Pon', 1: 'Uto', 2: 'Sri', 3: 'Čet', 4: 'Pet', 5: 'Sub', 6: 'Ned'}

    day_labels = []
    max_colored = []
    min_colored = []
    precip_display = []

    for i, date_str in enumerate(dates):
        dt = datetime.fromisoformat(date_str)
        day_label = f"{day_names[dt.weekday()]} {dt.strftime('%d.%m')}"

        if dt.date() == datetime.now().date():
            day_labels.append(f'[green]{day_label}[/green]')
        else:
            day_labels.append(day_label)

        hi = round(temp_max[i])
        lo = round(temp_min[i])
        max_colored.append(f'[{get_temp_color(hi)}]{hi}°[/{get_temp_color(hi)}]')
        min_colored.append(f'[{get_temp_color(lo)}]{lo}°[/{get_temp_color(lo)}]')

        rain = precipitation[i]
        color = get_precip_color(rain)
        if color:
            precip_display.append(f'[{color}]{rain:.1f}mm[/{color}]')
        else:
            precip_display.append(f'{rain:.1f}mm')

    table = Table(show_header=False, border_style="grey54", show_lines=True, box=box.ROUNDED)
    table.add_row(*day_labels)
    table.add_row(*max_colored)
    table.add_row(*min_colored)
    table.add_row(*precip_display)

    console.print(table)


def fetch_daily(days):
    """Fetch and display hourly forecast per day for N days."""
    params = {
        'latitude': LATITUDE,
        'longitude': LONGITUDE,
        'timezone': TIMEZONE,
        'forecast_days': days,
        'hourly': ['temperature_2m', 'precipitation'],
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    time_response = data['hourly']['time']
    temp_response = data['hourly']['temperature_2m']
    precip_response = data['hourly']['precipitation']

    day_names = {0: 'Pon', 1: 'Uto', 2: 'Sri', 3: 'Čet', 4: 'Pet', 5: 'Sub', 6: 'Ned'}

    # Group data by day (24 hours per day, take every other = 12 per day)
    hours_per_day = 24
    for day_index in range(days):
        start = day_index * hours_per_day
        end = start + hours_per_day

        day_times = time_response[start:end:2]
        day_temps = temp_response[start:end:2]
        day_precip = precip_response[start:end:2]

        dt = datetime.fromisoformat(time_response[start])
        day_label = day_names[dt.weekday()]
        is_today = dt.date() == datetime.now().date()

        # Time row
        time_display = [datetime.fromisoformat(t).strftime('%H:%M') for t in day_times]

        # First column is day label
        if is_today:
            day_col = f'[green]{day_label}[/green]'
        else:
            day_col = day_label

        # Color coded rows
        temp_even = [round(t) for t in day_temps]
        temp_color = [f'[{get_temp_color(t)}]{t}°[/{get_temp_color(t)}]' for t in temp_even]
        precip_display = []
        for p in day_precip:
            color = get_precip_color(p)
            if color:
                precip_display.append(f'[{color}]{p:.1f}mm[/{color}]')
            else:
                precip_display.append(f'{p:.1f}mm')

        table = Table(show_header=False, border_style="grey54", show_lines=True, box=box.ROUNDED)
        table.add_row(day_col, *time_display)
        table.add_row('Temp', *temp_color)
        table.add_row('Kiša', *precip_display)

        console.print(table)


if mode == "today":
    fetch_hourly()
elif mode == "summary":
    fetch_summary()
elif mode == "full":
    fetch_daily(7)
