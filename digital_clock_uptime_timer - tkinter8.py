import datetime
import tkinter as tk
import os
import re
import psutil
import wmi
from collections import deque

window = tk.Tk()
window.title("System Information Screensaver")
window.state('zoomed')
window.configure(background='black')

time_label = tk.Label(window, text="", font=(
    "Calibri", 120), bg="black", fg="white", bd=0)
date_label = tk.Label(window, text="", font=(
    "Calibri", 40), bg="black", fg="white", bd=0)
health_label = tk.Label(window, text="", font=(
    "Calibri", 70), bg="black", fg="white", bd=0)
legend_label = tk.Label(window, text="", font=(
    "Calibri", 50), bg="black", fg="white", bd=0)
info_label = tk.Label(window, text="", font=(
    "Calibri", 20), bg="black", fg="white", bd=0)
component_labels = {}

time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")

health_index_history = deque(maxlen=10)


def get_hardware_info():
    hardware_info = {}
    try:
        w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
        hardware_data = w.Sensor()
        for sensor in hardware_data:
            hardware_info.setdefault(sensor.SensorType, {})[
                sensor.Name] = sensor.Value
    except:
        pass
    return hardware_info


def calculate_component_state(value, warning_threshold, critical_threshold):
    if value >= critical_threshold:
        return "red", "Critical"
    elif value >= warning_threshold:
        return "orange", "Warning"
    else:
        return "white", "Okay"


def calculate_health_index(component_states):
    max_health_index = 100
    health_index = sum(100 if state[0] == "white" else 50 if state[0]
                       == "orange" else 0 for state in component_states.values())
    health_index = health_index / \
        len(component_states) if component_states else 100
    health_index = max(0, min(health_index, max_health_index))
    health_index_history.append(health_index)
    weights = list(range(1, len(health_index_history) + 1))
    weighted_health_index = sum(
        h * w for h, w in zip(health_index_history, weights)) / sum(weights)
    overall_state = "red" if any(state[0] == "red" for state in component_states.values()) else \
                    "orange" if any(state[0] == "orange" for state in component_states.values()) else \
                    "white"
    return int(weighted_health_index), overall_state


def system_health_monitor():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    hardware_info = get_hardware_info()

    component_states = {
        'CPU Usage': calculate_component_state(cpu_usage, 50, 70),
        'RAM Usage': calculate_component_state(ram_usage, 80, 90),
        'Disk Usage': calculate_component_state(disk_usage, 80, 90),
        'Temperatures': calculate_component_state(max(hardware_info.get('Temperature', {}).values(), default=0), 70, 80),
        'Fan': calculate_component_state(min(hardware_info.get('Fan', {}).values(), default=float('inf')), 500, 1000),
        'Power': calculate_component_state(max(hardware_info.get('Power', {}).values(), default=0), 40, 50),
        'Clock': calculate_component_state(max(hardware_info.get('Clock', {}).values(), default=0), 2000, 3500)
    }

    health_index, overall_state = calculate_health_index(component_states)
    health_label.config(fg=overall_state)

    legend = "System running smoothly" if overall_state == "white" else \
             "System running with some issues" if overall_state == "orange" else \
             "System health critical"
    legend_label.config(text=legend, fg=overall_state)

    for component, state in component_states.items():
        label = component_labels.get(component)
        if label is None:
            label = tk.Label(window, text="", font=(
                "Calibri", 14), bg="black", fg="white", bd=0)
            label.pack(side=tk.TOP, fill=tk.X)
            component_labels[component] = label
        label.config(text=f"{component}: {state[1]}", fg=state[0])

    return f"{health_index} / 100"


def show_recommendations(component_states):
    recommendations = [f"- {component}: {state[2]}" for component,
                       state in component_states.items() if state[0] == "red"]
    return "Recommendations:\n" + "\n".join(recommendations) if recommendations else ""


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
                return last_restart_date, last_restart_time
            except ValueError:
                return None


def timer_from_start_of_program():
    timer = (datetime.datetime.now() -
             datetime.datetime.strptime(time_of_start, "%H:%M:%S")).seconds
    return f"{timer // 3600} h, {(timer // 60) % 60} min, {timer % 60} sec" if timer > 60 else f"{timer} sec"


def update_labels():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    current_day_name = datetime.datetime.now().strftime("%A")
    timer = timer_from_start_of_program()
    last_restart = get_last_restart()
    system_health = system_health_monitor()

    time_label.config(text=current_time)
    date_label.config(text=f"Date: {current_date}\nDay: {current_day_name}")
    health_label.config(text=f"System Health Index:\n{system_health}")

    uptime = f"Uptime: {(datetime.datetime.now() - datetime.datetime.strptime(last_restart[0], '%d.%m.%Y')).days} days, " \
        f"{(datetime.datetime.now() - datetime.datetime.strptime(last_restart[1], '%H:%M:%S')).seconds // 3600} hours" \
        if last_restart else "Uptime data not available"
    info_label.config(text=f"{uptime}\nTimer from start: {timer}")

    window.after(1000, update_labels)


time_label.pack(side=tk.TOP, fill=tk.X)
date_label.pack(side=tk.TOP, fill=tk.X)
health_label.pack(side=tk.TOP, fill=tk.X)
legend_label.pack(side=tk.TOP, fill=tk.X)
info_label.pack(side=tk.BOTTOM, fill=tk.X)

update_labels()
window.mainloop()
