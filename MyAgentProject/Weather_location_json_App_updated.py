







#https://openweathermap.org/current#geo

# Run this before executing the code:
# python -m pip install requests plotly

from tkinter import *
from tkinter import filedialog
import requests
import plotly.graph_objs as go
from plotly.offline import plot
import webbrowser
from datetime import datetime
from collections import defaultdict

# --------------------------------------
# OpenWeatherMap API Key
API_KEY = '4a887990b64a0245edd5fcef94bf8619'  
GEOCODE_API = "http://api.openweathermap.org/geo/1.0/direct"
FORECAST_API = "https://api.openweathermap.org/data/2.5/forecast"

# --------------------------------------
def get_lat_lon(city):
    params = {'q': city, 'limit': 1, 'appid': API_KEY}
    try:
        res = requests.get(GEOCODE_API, params=params)
        res.raise_for_status()
        data = res.json()
        if data:
            return data[0]['lat'], data[0]['lon']
        else:
            return None, None
    except Exception as e:
        print("Error in get_lat_lon:", e)
        return None, None

# --------------------------------------
def fetch_5day_forecast(lat, lon):
    params = {'lat': lat, 'lon': lon, 'units': 'metric', 'appid': API_KEY}
    try:
        res = requests.get(FORECAST_API, params=params)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print("Error fetching forecast:", e)
        raise Exception("Failed to fetch 5-day forecast.")

# --------------------------------------
def plot_weather(data, city):
    forecast_by_day = defaultdict(list)

    for entry in data['list']:
        dt = datetime.fromtimestamp(entry['dt'])
        day = dt.strftime('%a %d')
        hour = dt.hour
        if 11 <= hour <= 14:
            forecast_by_day[day].append(entry['main']['temp'])

    days = []
    temps = []

    for day, temp_list in forecast_by_day.items():
        if temp_list:
            days.append(day)
            temps.append(sum(temp_list) / len(temp_list))

    fig = go.Figure(data=go.Scatter(
        x=days, y=temps, mode='lines+markers',
        line=dict(color='deepskyblue')
    ))
    fig.update_layout(
        title=f'5-Day Forecast for {city}',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        template='plotly_dark'
    )

    plot(fig, filename='weather_plot.html', auto_open=False)
    webbrowser.open('weather_plot.html')

# --------------------------------------
def show_forecast():
    city = city_value.get().strip()
    if not city:
        result_label.config(text="Please enter a city name.")
        return

    lat, lon = get_lat_lon(city)
    if lat is None:
        result_label.config(text=f"City '{city}' not found. Try again.")
        return

    try:
        data = fetch_5day_forecast(lat, lon)
        report_text.delete('1.0', END)

        forecast_by_day = defaultdict(list)
        for entry in data['list']:
            dt = datetime.fromtimestamp(entry['dt'])
            day = dt.strftime('%a %d')
            time = dt.strftime('%H:%M')
            temp = entry['main']['temp']
            weather = entry['weather'][0]['description'].capitalize()
            line = f"{day} {time} | {temp:.1f}°C | {weather}"
            forecast_by_day[day].append(line)

        report_lines = []
        for day, lines in forecast_by_day.items():
            report_lines.append(f"\n{day}:")
            report_lines.extend(lines)

        full_report = "\n".join(report_lines)
        report_text.insert(END, full_report)
        plot_weather(data, city)
        result_label.config(text=f"Showing 5-day forecast for '{city}'.")
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# --------------------------------------
def save_report():
    report = report_text.get("1.0", END).strip()
    if not report:
        result_label.config(text="No report to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")],
                                             title="Save Forecast Report")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report)
        result_label.config(text=f"Report saved to {file_path}")

# --------------------------------------
# GUI Setup
root = Tk()
root.title("5-Day Weather Forecast")
root.geometry("600x500")
root.resizable(False, False)

Label(root, text="Enter City Name:", font='Arial 12').pack(pady=10)

city_value = StringVar()
Entry(root, textvariable=city_value, font='Arial 12', width=25).pack()

Button(root, text="Get 5-Day Forecast", font='Arial 11 bold', bg='lightblue',
       padx=5, pady=5, command=show_forecast).pack(pady=10)

report_text = Text(root, height=15, width=70, font='Courier 10', wrap=WORD)
report_text.pack(pady=10)

Button(root, text="Save Report", font='Arial 11', bg='lightgreen',
       command=save_report).pack(pady=5)

result_label = Label(root, text="", font='Arial 10', fg='green')
result_label.pack()

root.mainloop()


