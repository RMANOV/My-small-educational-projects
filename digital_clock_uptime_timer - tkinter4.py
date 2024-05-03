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

# Create label widgets for different information
time_label = tk.Label(window, text="", font=(
    "Calibri", 80), bg="black", fg="white", bd=0)
date_label = tk.Label(window, text="", font=(
    "Calibri", 24), bg="black", fg="white", bd=0)
health_label = tk.Label(window, text="", font=(
    "Calibri", 60), bg="black", fg="white", bd=0)
legend_label = tk.Label(window, text="", font=(
    "Calibri", 40), bg="black", fg="white", bd=0)
info_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
cpu_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
ram_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
disk_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
network_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
recommendation_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")


def get_hardware_temperatures():
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
        return {}


def calculate_health_index(temperatures, cpu_usage, ram_usage, disk_usage, network_usage):
    max_health_index = 100
    critical_temp_threshold = 60
    high_temp_threshold = 50

    if temperatures:
        max_temp = max(temperatures.values())
        if max_temp >= critical_temp_threshold:
            temp_factor = 0
        elif max_temp >= high_temp_threshold:
            temp_factor = 50
        else:
            temp_factor = 100
    else:
        temp_factor = 100

    cpu_factor = 100 - cpu_usage
    ram_factor = 100 - (ram_usage * 0.5)
    disk_factor = 100 - disk_usage
    network_factor = 100 - (network_usage * 0.001)

    health_index = (temp_factor * 0.4 + cpu_factor * 0.3 + disk_factor *
                    0.2 + ram_factor * 0.1) / (1 + network_factor * 0.001)
    health_index = max(0, min(health_index, max_health_index))

    return int(health_index), max_health_index


def system_health_monitor():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_usage = psutil.net_io_counters().bytes_sent + \
        psutil.net_io_counters().bytes_recv
    temperatures = get_hardware_temperatures()

    health_index, max_health_index = calculate_health_index(
        temperatures, cpu_usage, ram_usage, disk_usage, network_usage)

    legend = ""
    recommendation = ""
    if health_index >= 80:
        color = "white"
        legend = "System running smoothly"
    elif health_index >= 60:
        color = "yellow"
        if cpu_usage > 90:
            legend += "High CPU usage. "
            recommendation += "Close unnecessary programs or processes. "
        if disk_usage > 95:
            legend += "Disk nearly full. "
            recommendation += "Free up disk space. "
        if temperatures and any(temp > 90 for temp in temperatures.values()):
            legend += "High temperatures!"
            recommendation += "Check cooling system and ensure proper ventilation. "
    elif health_index >= 40:
        color = "orange"
        legend = "Performance impacted. Check resources."
        if cpu_usage > 90:
            recommendation += "Close CPU-intensive programs or limit their usage. "
        if ram_usage > 90:
            recommendation += "Close memory-intensive programs or add more RAM. "
        if "Chrome" in (p.name() for p in psutil.process_iter()):
            recommendation += "Close Chrome or reduce the number of open tabs. "
    else:
        color = "red"
        legend = "System health critical!"
        recommendation = "System information will update shortly."

    health_label.config(fg=color)
    legend_label.config(text=legend, fg=color)
    recommendation_label.config(text=recommendation, fg=color)

    # Update individual component labels
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
    ram_label.config(text=f"RAM Usage: {ram_usage}%")
    disk_label.config(text=f"Disk Usage: {disk_usage}%")
    network_label.config(text=f"Network Usage: {
                         network_usage / 1024 / 1024:.2f} MB/s")

    return f"{health_index} / {max_health_index}"


def get_last_restart():
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


def timer_from_start_of_program():
    timer = (datetime.datetime.now() -
             datetime.datetime.strptime(time_of_start, "%H:%M:%S")).seconds
    if timer > 60:
        timer = f"{timer // 3600} h, {(timer // 60) %
                                      60} min, {timer % 60} sec"
    return timer


def update_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    time_label.config(text=current_time)
    window.after(1000, update_time)


def update_system_info():
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    current_day_name = datetime.datetime.now().strftime("%A")
    timer1 = timer_from_start_of_program()
    last_r = get_last_restart()
    system_health = system_health_monitor()

    if last_r:
        uptime = f'{(datetime.datetime.now() - datetime.datetime.strptime(last_r[0], "%d.%m.%Y")).days} days, {
            (datetime.datetime.now() - datetime.datetime.strptime(last_r[1], "%H:%M:%S")).seconds // 3600} hours'
    else:
        uptime = "Uptime data not available"

    date_label.config(text=f"Date: {current_date}\nDay: {current_day_name}")
    health_label.config(text=f"System Health Index:\n{system_health}")
    info_label.config(text=f"Uptime: {uptime}\nTimer from start: {timer1}")

    # Update system info every 30 seconds
    window.after(30000, update_system_info)


# Call the update functions to start updating the labels
update_time()
update_system_info()

# Pack the label widgets into the window
date_label.pack(side=tk.TOP, fill=tk.X)
time_label.pack(expand=True)
health_label.pack(side=tk.TOP, fill=tk.X)
legend_label.pack(side=tk.TOP, fill=tk.X)
cpu_label.pack(side=tk.TOP, fill=tk.X)
ram_label.pack(side=tk.TOP, fill=tk.X)
disk_label.pack(side=tk.TOP, fill=tk.X)
network_label.pack(side=tk.TOP, fill=tk.X)
recommendation_label.pack(side=tk.TOP, fill=tk.X)
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Disable window resizing to prevent flickering
window.resizable(False, False)

# Run the main loop
window.mainloop()
