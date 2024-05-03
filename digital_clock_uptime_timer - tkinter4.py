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
legend_label = tk.Label(
    window, text="", font=("Calibri", 100), bg="black", fg="white", bd=0
)
info_label = tk.Label(
    window, text="", font=("Calibri", 14), bg="black", fg="white", bd=0
)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")


def get_hardware_temperatures():
    # This function requires OpenHardwareMonitor to be running on the machine
    try:
        response = requests.get("http://localhost:8085/data.json", timeout=1)
        data = response.json()
        temperatures = {}
        for hardware in data['Children']:
            for sensor in hardware['Children']:
                for value in sensor['Children']:
                    if value['Text'] == 'Temperatures':
                        for temp in value['Children']:
                            temperatures[temp['Text']] = temp['Value']
        return temperatures
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error retrieving temperatures: {str(e)}")
        return {}  # Return an empty dictionary on error

def calculate_health_index(temperatures, cpu_usage, ram_usage, disk_usage, network_usage):
    # Improved formula for health index
    max_health_index = 100
    temp_factor = 100 - (sum(temperatures.values()) / len(temperatures)) if temperatures else 100
    cpu_factor = 100 - cpu_usage
    ram_factor = 100 - (ram_usage * 0.5)  # RAM usage is less critical
    disk_factor = 100 - disk_usage
    network_factor = 100 - (network_usage * 0.1)  # Network usage is less critical

    health_index = (temp_factor + cpu_factor + ram_factor + disk_factor + network_factor) / 5
    
    # Ensure health index is not negative
    health_index = max(0, health_index)
    
    return int(health_index), max_health_index


def system_health_monitor():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
    temperatures = get_hardware_temperatures()

    health_index, max_health_index = calculate_health_index(
        temperatures, cpu_usage, ram_usage, disk_usage, network_usage)

    legend = ""
    if health_index >= 80:
        color = "white"
    else:
        if cpu_usage > 90:  # Only show warning for severe CPU overload
            legend += "CPU usage is critically high. "
        if ram_usage > 90:  # Only show warning for severe RAM overload  
            legend += "RAM usage is critically high. "
        if disk_usage > 95:  # Only show warning for severe disk overload
            legend += "Disk usage is critically high. "
        if network_usage > 10000000:  # 10MB, only show for very high network usage
            legend += "Network usage is very high. "
        if temperatures and any(temp > 90 for temp in temperatures.values()):  # Only show for critical temperatures
            legend += "Some component temperatures are critically high."

    if health_index >= 60:
        color = "yellow"
    elif health_index >= 40:
        color = "orange"
    else:
        color = "red"

    health_label.config(fg=color)
    legend_label.config(text=legend, fg=color)
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
    current_day_name = datetime.datetime.now().strftime("%A")
    timer1 = timer_from_start_of_program()
    last_r = get_last_restart()
    system_health = system_health_monitor()

    # Calculate the uptime in days and hours
    if last_r:
        uptime = f'{(datetime.datetime.now() - datetime.datetime.strptime(last_r[0], "%d.%m.%Y")).days} days, {
            (datetime.datetime.now() - datetime.datetime.strptime(last_r[1], "%H:%M:%S")).seconds // 3600} hours'
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
legend_label.pack(side=tk.TOP, fill=tk.X)
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Disable window resizing to prevent flickering
window.resizable(False, False)

# Run the main loop
window.mainloop()
