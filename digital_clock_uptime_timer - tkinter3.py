import datetime
import tkinter as tk
import os
import re
import psutil
import requests

# Create the main window
window = tk.Tk()
window.title("System Information Screensaver")
window.state('zoomed')  # Maximized window that is not full screen
window.configure(background='black')  # Set the background to absolute black

# Create a label widget for time, date, and other information
time_label = tk.Label(
    window, text="", font=("Calibri", 120), bg="black", fg="white", bd=0
)
date_label = tk.Label(
    window, text="", font=("Calibri", 24), bg="black", fg="white", bd=0
)
health_label = tk.Label(
    window, text="", font=("Calibri", 100), bg="black", fg="white", bd=0
)
info_label = tk.Label(
    window, text="", font=("Calibri", 14), bg="black", fg="white", bd=0
)
legend_label = tk.Label(
    window, text="", font=("Calibri", 14), bg="black", fg="white", bd=0
)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")

def get_hardware_temperatures():
    # This function requires OpenHardwareMonitor to be running on the machine
    try:
        response = requests.get("http://localhost:8085/data.json")
        data = response.json()
        temperatures = {}
        for hardware in data['Children']:
            for sensor in hardware['Children']:
                for value in sensor['Children']:
                    if value['Text'] == 'Temperatures':
                        for temp in value['Children']:
                            temperatures[temp['Text']] = temp['Value']
        return temperatures
    except Exception as e:
        return {}

def calculate_health_index(temperatures, cpu_usage, ram_usage):
    # Example formula for health index
    max_health_index = 100
    if temperatures:
        temp_factor = 100 - (sum(temperatures.values()) / len(temperatures))
        health_index = 100 - (cpu_usage + ram_usage + (100 - temp_factor)) / 3
    else:
        health_index = 100 - (cpu_usage + ram_usage) / 2
    return int(health_index), max_health_index

def system_health_monitor():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    temperatures = get_hardware_temperatures()

    health_index, max_health_index = calculate_health_index(temperatures, cpu_usage, ram_usage)
    
    legend = ""
    if health_index >= 80:
        color = "white"
    else:
        if cpu_usage > 20:
            legend += "CPU usage is high. "
        if ram_usage > 20:  
            legend += "RAM usage is high. "
        if temperatures and any(temp > 60 for temp in temperatures.values()):
            legend += "Some component temperatures are high."
            
    if health_index >= 60:
        color = "yellow"
    elif health_index >= 40:
        color = "orange"  
    else:
        color = "red"
        
    health_label.config(fg=color)
    legend_label.config(text=legend)
    return f"{health_index} / {max_health_index}"

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
                last_restart_date, junk, last_restart_time = last_restart_str.split(" ")
                last_restart = (last_restart_date + "-" + last_restart_time).strip()
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
        timer = f"{timer // 3600} h, {(timer // 60) % 60} min, {timer % 60} sec"
    return timer

# Define a function to update the label text every second
def update_time():
    # Format the current time and date as separate variables
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    current_day_name = datetime.datetime.now().strftime("%A")
    timer1 = timer_from_start_of_program()
    last_r = get_last_restart()
    system_health = system_health_monitor()

    # Calculate the uptime in days and hours
    if last_r:
        uptime = f'{(datetime.datetime.now() - datetime.datetime.strptime(last_r[0], "%d.%m.%Y")).days} days, {(datetime.datetime.now() - datetime.datetime.strptime(last_r[1], "%H:%M:%S")).seconds // 3600} hours'
    else:
        uptime = "Uptime data not available"

    # Update the labels
    time_label.config(text=current_time)
    date_label.config(text=f"Date: {current_date}\nDay: {current_day_name}")
    health_label.config(text=f"System Health Index:\n{system_health}")
    info_label.config(text=f"Uptime: {uptime}\nTimer from start: {timer1}")

    # Schedule the function to run again after 1 second
    window.after(1000, update_time)

# Call the update_time function to start updating the label text
update_time()

# Pack the label widgets into the window
date_label.pack(side=tk.TOP, fill=tk.X)
time_label.pack(expand=True)
health_label.pack(side=tk.TOP, fill=tk.X)
legend_label.pack(side=tk.BOTTOM, fill=tk.X)
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Run the main loop
window.mainloop()
