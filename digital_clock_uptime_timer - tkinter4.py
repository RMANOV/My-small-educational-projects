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
temperature_label = tk.Label(window, text="", font=(
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
        return None


def calculate_health_index(temperatures, cpu_usage, ram_usage, disk_usage):
    max_health_index = 100
    critical_temp_threshold = 80
    warning_temp_threshold = 60

    if temperatures:
        max_temp = max(temperatures.values())
        if max_temp >= critical_temp_threshold:
            temp_factor = 0
        elif max_temp >= warning_temp_threshold:
            temp_factor = 50
        else:
            temp_factor = 100
    else:
        temp_factor = 100

    cpu_factor = 100 - cpu_usage
    ram_factor = 100 - ram_usage
    disk_factor = 100 - disk_usage

    health_index = (temp_factor * 0.4 + cpu_factor * 0.3 +
                    ram_factor * 0.2 + disk_factor * 0.1)
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
        temperatures, cpu_usage, ram_usage, disk_usage)

    legend = ""
    if health_index >= 80:
        color = "white"
        legend = "System running smoothly"
    elif health_index >= 60:
        color = "yellow"
        legend = "System running with some issues"
    elif health_index >= 40:
        color = "orange"
        legend = "System performance degraded"
    else:
        color = "red"
        legend = "System health critical"

    health_label.config(fg=color)
    legend_label.config(text=legend, fg=color)

    # Update individual component labels
    cpu_color = "red" if cpu_usage > 90 else "orange" if cpu_usage > 70 else "white"
    cpu_label.config(text=f"CPU Usage: {cpu_usage}%", fg=cpu_color)

    ram_color = "red" if ram_usage > 90 else "orange" if ram_usage > 70 else "white"
    ram_label.config(text=f"RAM Usage: {ram_usage}%", fg=ram_color)

    disk_color = "red" if disk_usage > 95 else "orange" if disk_usage > 80 else "white"
    disk_label.config(text=f"Disk Usage: {disk_usage}%", fg=disk_color)

    network_label.config(text=f"Network Usage: {
                         network_usage / 1024 / 1024:.2f} MB/s", fg="white")

    temp_text = "Temperatures:\n"
    temp_color = "white"
    if temperatures is not None:
        for component, temp in temperatures.items():
            if temp > 80:
                temp_color = "red"
            elif temp > 60:
                temp_color = "orange"
            temp_text += f"{component}: {temp}°C\n"
    else:
        temp_text += "N/A"
    temperature_label.config(text=temp_text, fg=temp_color)

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


def update_labels():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
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

    time_label.config(text=current_time)
    date_label.config(text=f"Date: {current_date}\nDay: {current_day_name}")
    health_label.config(text=f"System Health Index:\n{system_health}")
    info_label.config(text=f"Uptime: {uptime}\nTimer from start: {timer1}")

    window.after(1000, update_labels)


# Call the update_labels function to start updating the labels
update_labels()

# Pack the label widgets into the window
date_label.pack(side=tk.TOP, fill=tk.X)
time_label.pack(expand=True)
health_label.pack(side=tk.TOP, fill=tk.X)
legend_label.pack(side=tk.TOP, fill=tk.X)
cpu_label.place(relx=1.0, rely=0.0, anchor='ne')
ram_label.place(relx=1.0, rely=0.05, anchor='ne')
disk_label.place(relx=1.0, rely=0.1, anchor='ne')
network_label.place(relx=1.0, rely=0.15, anchor='ne')
temperature_label.place(relx=1.0, rely=0.2, anchor='ne')
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Disable window resizing to prevent flickering
window.resizable(False, False)

# Run the main loop
window.mainloop()
