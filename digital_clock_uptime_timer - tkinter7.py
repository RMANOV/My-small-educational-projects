import datetime
import tkinter as tk
import os
import re
import psutil
import wmi

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
component_label = tk.Label(window, text="", font=(
    "Calibri", 14), bg="black", fg="white", bd=0, justify=tk.LEFT)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")


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


def calculate_health_index(cpu_usage, ram_usage, disk_usage, hardware_info):
    max_health_index = 100

    component_states = {}

    cpu_state = calculate_component_state(cpu_usage, 50, 70)
    component_states['CPU Usage'] = cpu_state

    ram_state = calculate_component_state(ram_usage, 60, 80)
    component_states['RAM Usage'] = ram_state

    disk_state = calculate_component_state(disk_usage, 60, 80)
    component_states['Disk Usage'] = disk_state

    temp_state = "white"
    for component, temp in hardware_info.get('Temperatures', {}).items():
        if temp > 50:
            temp_state = "red"
            break
        elif temp > 40:
            temp_state = "orange"
    component_states['Temperatures'] = temp_state

    load_state = "white"
    for component, load in hardware_info.get('Load', {}).items():
        if load > 80:
            load_state = "red"
            break
        elif load > 60:
            load_state = "orange"
    component_states['Load'] = load_state

    fan_state = "white"
    for component, fan_speed in hardware_info.get('Fan', {}).items():
        if fan_speed < 500:
            fan_state = "red"
            break
        elif fan_speed < 1000:
            fan_state = "orange"
    component_states['Fan'] = fan_state

    voltage_state = "white"
    for component, voltage in hardware_info.get('Voltage', {}).items():
        if voltage < 0.95 or voltage > 1.05:
            voltage_state = "red"
            break
        elif voltage < 0.98 or voltage > 1.02:
            voltage_state = "orange"
    component_states['Voltage'] = voltage_state

    clock_state = "white"
    for component, clock in hardware_info.get('Clock', {}).items():
        if clock < 0.95 or clock > 1.05:
            clock_state = "red"
            break
        elif clock < 0.98 or clock > 1.02:
            clock_state = "orange"
    component_states['Clock'] = clock_state

    component_factors = {
        'Temperatures': 0.3,
        'Load': 0.2,
        'CPU Usage': 0.2,
        'RAM Usage': 0.1,
        'Disk Usage': 0.1,
        'Fan': 0.05,
        'Voltage': 0.03,
        'Clock': 0.02
    }

    health_index = sum(100 if state == "white" else 50 if state ==
                       "orange" else 0 for state in component_states.values())
    health_index = health_index / \
        len(component_states) if component_states else 100
    health_index = max(0, min(health_index, max_health_index))

    overall_state = "red" if any(state == "red" for state in component_states.values()) else \
                    "orange" if any(state == "orange" for state in component_states.values()) else \
                    "white"

    return int(health_index), overall_state, component_states


def system_health_monitor():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_usage = psutil.net_io_counters().bytes_sent + \
        psutil.net_io_counters().bytes_recv
    hardware_info = get_hardware_info()

    health_index, overall_state, component_states = calculate_health_index(
        cpu_usage, ram_usage, disk_usage, hardware_info)

    health_label.config(fg=overall_state)

    if overall_state == "white":
        legend = "System running smoothly"
    elif overall_state == "orange":
        legend = "System running with some issues"
    else:
        legend = "System health critical"

    legend_label.config(text=legend, fg=overall_state)

    component_text = "Component States:\n"
    for component, state in component_states.items():
        component_text += f"{component}: {state}\n"

    component_label.config(text=component_text)

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
component_label.place(relx=1.0, rely=0.0, anchor='ne')
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Disable window resizing to prevent flickering
window.resizable(False, False)

# Run the main loop
window.mainloop()
