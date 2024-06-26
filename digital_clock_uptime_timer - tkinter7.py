import datetime
import tkinter as tk
import os
import re
import psutil
import wmi
from collections import deque

# Create the main window
window = tk.Tk()
window.title("System Information Screensaver")
window.state('zoomed')  # Maximized window that is not full screen
window.configure(background='black')  # Set the background to absolute black

# Create label widgets for different information
time_label = tk.Label(window, text="", font=(
    "Calibri", 400), bg="black", fg="white", bd=0)
date_label = tk.Label(window, text="", font=(
    "Calibri", 24), bg="black", fg="white", bd=0)
health_label = tk.Label(window, text="", font=(
    "Calibri", 60), bg="black", fg="white", bd=0)
legend_label = tk.Label(window, text="", font=(
    "Calibri", 40), bg="black", fg="white", bd=0)
info_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)

# Create labels for each component
cpu_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
gpu_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
ram_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
disk_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
temp_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
fan_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
power_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)
clock_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")

# Initialize a deque to store the health index history
health_index_history = deque(maxlen=10)


def get_hardware_info():
    hardware_info = {}
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        hardware_data = w.Sensor()
        for sensor in hardware_data:
            if sensor.SensorType == u'Temperature':
                hardware_info.setdefault('Temperatures', {})[
                                         sensor.Name] = sensor.Value
            elif sensor.SensorType == u'Load':
                hardware_info.setdefault('Load', {})[
                                         sensor.Name] = sensor.Value
            elif sensor.SensorType == u'Fan':
                hardware_info.setdefault('Fan', {})[sensor.Name] = sensor.Value
            elif sensor.SensorType == u'Voltage':
                hardware_info.setdefault('Voltage', {})[
                                         sensor.Name] = sensor.Value
            elif sensor.SensorType == u'Clock':
                hardware_info.setdefault('Clock', {})[
                                         sensor.Name] = sensor.Value
            elif sensor.SensorType == u'Power':
                hardware_info.setdefault('Power', {})[
                                         sensor.Name] = sensor.Value
    except:
        pass
    return hardware_info


def calculate_component_state(value, warning_threshold, critical_threshold):
    if value >= critical_threshold:
        return "red"
    elif value >= warning_threshold:
        return "orange"
    else:
        return "white"


def calculate_health_index(cpu_usage, gpu_usage, ram_usage, disk_usage, hardware_info):
    max_health_index = 100

    component_states = {}

    cpu_state = calculate_component_state(cpu_usage, 50, 70)
    component_states['CPU Usage'] = (cpu_state, cpu_usage)

    gpu_state = calculate_component_state(gpu_usage, 50, 70)
    component_states['GPU Usage'] = (gpu_state, gpu_usage)

    ram_state = calculate_component_state(ram_usage, 60, 80)
    component_states['RAM Usage'] = (ram_state, ram_usage)

    disk_state = calculate_component_state(disk_usage, 60, 80)
    component_states['Disk Usage'] = (disk_state, disk_usage)

    temp_state = "white"
    temp_value = 0
    for component, temp in hardware_info.get('Temperatures', {}).items():
        if 'CPU' in component and temp > 50:
            temp_state = "red"
            temp_value = max(temp_value, temp)
        elif 'CPU' in component and temp > 40:
            temp_state = "orange"
            temp_value = max(temp_value, temp)
        elif 'GPU' in component and temp > 60:
            temp_state = "red"
            temp_value = max(temp_value, temp)
        elif 'GPU' in component and temp > 50:
            temp_state = "orange"
            temp_value = max(temp_value, temp)
    component_states['Temperatures'] = (temp_state, temp_value)

    fan_state = "white"
    fan_value = float('inf')
    for component, fan_speed in hardware_info.get('Fan', {}).items():
        if fan_speed < 500:
            fan_state = "red"
            fan_value = min(fan_value, fan_speed)
        elif fan_speed < 1000:
            fan_state = "orange"
            fan_value = min(fan_value, fan_speed)
    component_states['Fan'] = (fan_state, fan_value)

    power_state = "white"
    power_value = 0
    for component, power in hardware_info.get('Power', {}).items():
        if 'CPU' in component and power > 40:
            power_state = "red"
            power_value = max(power_value, power)
        elif 'CPU' in component and power > 30:
            power_state = "orange"
            power_value = max(power_value, power)
        elif 'GPU' in component and power > 60:
            power_state = "red"
            power_value = max(power_value, power)
        elif 'GPU' in component and power > 50:
            power_state = "orange"
            power_value = max(power_value, power)
    component_states['Power'] = (power_state, power_value)

    clock_state = "white"
    clock_value = 0
    for component, clock in hardware_info.get('Clock', {}).items():
        if 'CPU' in component and (clock < 1500 or clock > 4000):
            clock_state = "red"
            clock_value = clock
            break
        elif 'CPU' in component and (clock < 2000 or clock > 3500):
            clock_state = "orange"
            clock_value = clock
        elif 'GPU' in component and (clock < 500 or clock > 2000):
            clock_state = "red"
            clock_value = clock
            break
        elif 'GPU' in component and (clock < 800 or clock > 1500):
            clock_state = "orange"
            clock_value = clock
    component_states['Clock'] = (clock_state, clock_value)

    component_factors = {
        'Temperatures': 0.3,
        'CPU Usage': 0.2,
        'GPU Usage': 0.15,
        'RAM Usage': 0.1,
        'Disk Usage': 0.1,
        'Fan': 0.05,
        'Power': 0.07,
        'Clock': 0.03
    }

    health_index = sum(100 if state[0] == "white" else 50 if state[0]
                       == "orange" else 0 for state in component_states.values())
    health_index = health_index / \
        len(component_states) if component_states else 100
    health_index = max(0, min(health_index, max_health_index))

    # Calculate the time-weighted average of the health index
    health_index_history.append(health_index)
    weights = list(range(1, len(health_index_history) + 1))
    weighted_health_index = sum(
        h * w for h, w in zip(health_index_history, weights)) / sum(weights)

    overall_state = "red" if any(state[0] == "red" for state in component_states.values()) else \
                    "orange" if any(state[0] == "orange" for state in component_states.values()) else \
                    "white"

    return int(weighted_health_index), overall_state, component_states


def system_health_monitor():
    cpu_usage = psutil.cpu_percent()
    gpu_usage = 0
    try:
        gpu_usage = psutil.sensors_gpus()[0].load
    except:
        pass
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    hardware_info = get_hardware_info()

    health_index, overall_state, component_states = calculate_health_index(
        cpu_usage, gpu_usage, ram_usage, disk_usage, hardware_info)

    health_label.config(fg=overall_state)

    if overall_state == "white":
        legend = "System running smoothly"
    elif overall_state == "orange":
        legend = "System running with some issues"
    else:
        legend = "System health critical"

    legend_label.config(text=legend, fg=overall_state)

    cpu_state, cpu_value = component_states['CPU Usage']
    cpu_label.config(text=f"CPU Usage: {cpu_value:.0f}%", fg=cpu_state)

    gpu_state, gpu_value = component_states['GPU Usage']
    gpu_label.config(text=f"GPU Usage: {gpu_value:.0f}%", fg=gpu_state)

    ram_state, ram_value = component_states['RAM Usage']
    ram_label.config(text=f"RAM Usage: {ram_value:.0f}%", fg=ram_state)

    disk_state, disk_value = component_states['Disk Usage']
    disk_label.config(text=f"Disk Usage: {disk_value:.0f}%", fg=disk_state)

    temp_state, temp_value = component_states['Temperatures']
    temp_label.config(text=f"Temperature: {temp_value:.0f}°C", fg=temp_state)

    fan_state, fan_value = component_states['Fan']
    if fan_value == float('inf'):
        fan_label.config(text=f"Fan: N/A", fg=fan_state)
    else:
        fan_label.config(text=f"Fan: {fan_value:.0f} RPM", fg=fan_state)

    power_state, power_value = component_states['Power']
    power_label.config(text=f"Power: {power_value:.0f} W", fg=power_state)

    clock_state, clock_value = component_states['Clock']
    clock_label.config(text=f"Clock: {clock_value:.0f} MHz", fg=clock_state)

    return f"{health_index} / 100"


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
gpu_label.place(relx=1.0, rely=0.05, anchor='ne')
ram_label.place(relx=1.0, rely=0.1, anchor='ne')
disk_label.place(relx=1.0, rely=0.15, anchor='ne')
temp_label.place(relx=1.0, rely=0.2, anchor='ne')
fan_label.place(relx=1.0, rely=0.25, anchor='ne')
power_label.place(relx=1.0, rely=0.3, anchor='ne')
clock_label.place(relx=1.0, rely=0.35, anchor='ne')
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Disable window resizing to prevent flickering
window.resizable(False, False)

# Run the main loop
window.mainloop()


