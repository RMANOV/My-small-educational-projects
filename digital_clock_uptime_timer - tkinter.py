
import datetime
import tkinter as tk
import os
import re

# Create the main window
window = tk.Tk()
window.title("Current Time")

# Create a label widget to fully fill the all window
time_label = tk.Label(
    window, text="", font=("Calibry", 65), bg="black", fg="white", bd=0
)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")

# Define a function to get the weather data for current location from the OpenWeatherMap API


def get_weather_data():
    # get current location
    location = os.popen(
        "wmic path win32_computersystemproduct get uuid").read()
    match_location = re.search(r"UUID\s+(.+)", location)
    if match_location:
        try:
            location_str = match_location.group(1)
            location_str = location_str.strip()
            print(location_str)
        except ValueError:
            location_str = "Sofia"
            return location_str

    # get weather data from the OpenWeatherMap API
    def get_weather(location_str):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={
                location_str}&appid=API_KEY&units=metric"
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            print(error)
            return None
        else:
            return response.json()

    # format the weather data
    def format_weather(weather):
        try:
            name = weather["name"]
            desc = weather["weather"][0]["description"]
            temp = weather["main"]["temp"]
            formatted_weather = f"{name}: {desc}, {temp}°C"
            return formatted_weather
        except:
            print("Could not format weather.")
            return None


def get_last_restart():
    # this function should be called only once a day
    last_restart_date = ""
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")

    if last_restart_date != current_date:
        systeminfo = os.popen("systeminfo").read()
        match = re.search(r"System Boot Time:\s+(.+)", systeminfo)
        if match:
            try:
                last_restart_str = match.group(1)
                last_restart_date, junk, last_restart_time = last_restart_str.split(
                    " ")
                last_restart = (last_restart_date + "-" +
                                last_restart_time).strip()
                return last_restart_date, last_restart_time
            except ValueError:
                print("Could not get last restart time.")
                return None


# Define a function to add a timer to the label text - to count time from the start of the program
def timer_from_start_of_program():
    # get difference between current time and time of start of the program
    timer = (
        datetime.datetime.now() - datetime.datetime.strptime(time_of_start, "%H:%M:%S")
    ).seconds
    # if seconds is more than 60, calculate minutes and seconds and hours, else return seconds
    if timer > 60:
        timer = f"{timer // 3600} h, {(timer // 60) %
                                      60} min, {timer % 60} sec"
    return timer


# Define a function to update the label text every second
def update_time():
    # Format the current time and date as separate variables
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    timer1 = timer_from_start_of_program()
    weather_condition = get_weather_data()
    # do not update the uptime every second - only once a day
    global date_of_start
    if current_date != date_of_start:
        for i in range(1):
            last_r = get_last_restart()
            last_restart_date = current_date
            current_week = datetime.datetime.now().strftime("%U Week")
            current_day = datetime.datetime.now().strftime("%A")
            current_year_day = datetime.datetime.now().strftime("%j Day")
            date_of_start = current_date

    else:
        for i in range(1):
            last_r = get_last_restart()
            last_restart_date = current_date
            current_week = datetime.datetime.now().strftime("%U Week")
            current_day = datetime.datetime.now().strftime("%A")
            current_year_day = datetime.datetime.now().strftime("%j Day")

    # calculate the uptime in days and hours
    uptime = f'{(datetime.datetime.now() - datetime.datetime.strptime(last_r[0], "%d.%m.%Y")).days} days, {
        (datetime.datetime.now() - datetime.datetime.strptime(last_r[1], "%H:%M:%S")).seconds // 3600} hours'

    # Concatenate the date, time, and active users into a single string
    current_time_str = f"{current_time}\n{current_date}\n{current_week}\n{current_day}\n{current_year_day}\nUp-time: {
        uptime}\nUp-time date: {last_r[0]}\nUp-time time: {last_r[1]}\nTimer from start : {timer1} \nWeather: {weather_condition}"

    # Update the label text
    time_label.config(text=current_time_str)

    # Schedule the function to run again after 1 second
    window.after(1000, update_time)


# Call the update_time function to start updating the label text
update_time()

# Pack the label widget into the window
time_label.pack()

# Run the main loop
window.mainloop()
