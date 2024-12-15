import json
from tkinter import *
import tkinter as tk
from unittest import result
from geopy.geocoders import Photon
from configparser import ConfigParser
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz


def _get_api_key():
    """Fetch the API key from configuration file.

    Expects a config file named "secrets.ini" with structure:

        [openweather]
        api_key=<YOUR-OPENWEATHER-API-KEY>

    Returns: 
        string: your API key
    """
    config = ConfigParser()
    config.read("secrets.ini")
    return str(config["openweather"]["api_key"])


def getWeather():
    """Gets weather data of city. 
    Name of city read from textfield.
    Updates time and data textboxes
    """
    try:
        city = textfield.get()
        geolocator = Photon(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Weather
        api_key = _get_api_key()
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
            city+"&appid=8dc9442b439bdca4751aae42fa0f3957"

        json_data = requests.get(api).json()
        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        temp = int(json_data["main"]["temp"] - 273.15)
        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]

        temp_text.config(text=(temp, "°"))
        feels_like_text.config(
            text=(condition, "|", "FEELS", "LIKE", temp, "°"))
        description_text.config(text=description)
        pressure_text.config(text=pressure)
        humidity_text.config(text=humidity)
        wind_text.config(text=wind)
    except Exception as e:
        messagebox.showerror("Weather App", "Invalid Entry")


root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# Search Box
Search_image = PhotoImage(
    file="C:/Users/a_pavlov23/OneDrive - Winchester College/Documents/WeatherApp/Images/search.png")
image = Label(image=Search_image)
image.place(x=20, y=20)

# Text field for search
textfield = tk.Entry(root, justify="center", width=17,
                     font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

# Icon for search bar
Search_icon = PhotoImage(
    file="C:/Users/a_pavlov23/OneDrive - Winchester College/Documents/WeatherApp/Images/search_icon.png")
image_icon = Button(image=Search_icon, borderwidth=0,
                    cursor="hand2", bg="#404040", command=getWeather)
# So user can also press enter key
root.bind('<Return>', lambda event: getWeather()
          if textfield.get().strip() else None)
image_icon.place(x=400, y=34)

# Logo
Logo_image = PhotoImage(
    file="C:/Users/a_pavlov23/OneDrive - Winchester College/Documents/WeatherApp/Images/logo.png")
logo = Label(image=Logo_image)
logo.place(x=150, y=100)

# Bottom Box
Frame_image = PhotoImage(
    file="C:/Users/a_pavlov23/OneDrive - Winchester College/Documents/WeatherApp/Images/box.png")
frame_image = Label(image=Frame_image)
frame_image.pack(padx=5, pady=5, side=BOTTOM)

# Time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)


def produce_label(description):
    """Produces Label given descriptipn

    Args:
        description (string): What you want it to show

    Returns:
        tkinter Label object: your Label to be placed
    """
    return Label(root, text=description, font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")


def produce_label_text():
    """Produces text '...' below labels

    Returns:
        Tkinter Label object: the text '...'
    """
    return Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")


# Weather labels
temp_text = Label(font=("arial", 70, "bold"), fg="#ee666d")
temp_text.place(x=400, y=150)
feels_like_text = Label(font=("arial", 15, "bold"))
feels_like_text.place(x=400, y=250)

wind_label = produce_label("WIND")
wind_label.place(x=120, y=400)
wind_text = produce_label_text()
wind_text.place(x=120, y=430)

humidity_label = produce_label("HUMIDITY")
humidity_label.place(x=255, y=400)
humidity_text = produce_label_text()
humidity_text.place(x=280, y=430)

descripton_label = produce_label("DESCRIPTION")
descripton_label.place(x=430, y=400)
description_text = produce_label_text()
description_text.place(x=430, y=430)

pressure_label = produce_label("PRESSURE")
pressure_label.place(x=650, y=400)
pressure_text = produce_label_text()
pressure_text.place(x=670, y=430)

root.mainloop()
