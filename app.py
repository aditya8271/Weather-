
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
from importlib.metadata import version
import requests
import pytz
import subprocess
from PIL import Image, ImageTk

root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

def open_exe():
    subprocess.run(["path_to_your_exe_file.exe"])
    root.title("Open EXE Example")

open_button = tk.Button(root, text="Open EXE", command=open_exe)
open_button.pack(pady=20)

def getWeather(city=None):
    try:
        # If city is not provided, check if the user allowed location access
        if not city:
            location_data = requests.get("https://ipinfo.io").json()
            city = location_data['city']
        
        geolocator = Nominatim(user_agent="my_weather_app_1245")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # Weather API
        api = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=e7a320c940812586a56929c70723c9c0"
        json_data = requests.get(api).json()

        # Extracting weather details
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)  # Convert from Kelvin to Celsius
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        
        # Display data in Tkinter labels
        t.config(text=(temp, "°C"))
        c.config(text=(condition, "|", "Feels Like", temp, "°C"))
        w.config(text=wind)
        h.config(text=humidity)
        d.config(text=description)
        p.config(text=pressure)

        # Update the search field with the current city
        textfield.delete(0, END)
        textfield.insert(0, city)

    except Exception as e:
        messagebox.showerror("Weather App", "Could not retrieve weather data!")

def request_location():
    response = messagebox.askyesno("Location Access", "Would you like to enable location for accurate weather data?")
    if response:  # User clicked Yes
        location_data = requests.get("https://ipinfo.io").json()
        city = location_data['city']
        getWeather(city)  # Fetch weather based on location
    else:  # User clicked No
        messagebox.showinfo("Manual Input", "Please enter the city name to get weather data.")

# GUI Elements
Search_image = PhotoImage(file="images/search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify='center', width=17, font=('poppins', 25, 'bold'), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file="images/icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=lambda: getWeather(textfield.get()))
myimage_icon.place(x=400, y=34)

# Logo
Logo_image = PhotoImage(file="images/Copy of logo.png")
logo = Label(image=Logo_image)
logo.place(x=150, y=100)

# Bottom
Frame_image = PhotoImage(file="images/Copy of box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time and Labels
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

label1 = Label(root, text="WIND", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)
label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)
label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)
label4 = Label(root, text="PRESSURE", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=("arial", 15, "bold"))
c.place(x=400, y=250)
w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

# Run location request popup on startup
request_location()

root.mainloop()