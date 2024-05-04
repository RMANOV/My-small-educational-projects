from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import datetime
import tkinter as tk
import os
import re
import psutil
import wmi
from collections import deque
import matplotlib
matplotlib.use("Agg")

# Create the main window
window = tk.Tk()
window.title("System Information Screensaver")
window.state('zoomed')
window.configure(background='black')

# Create label widgets
time_label = tk.Label(window, text="", font=(
    "Calibri", 100), bg="black", fg="white", bd=0)
date_label = tk.Label(window, text="", font=(
    "Calibri", 36), bg="black", fg="white", bd=0)
health_label = tk.Label(window, text="", font=(
    "Calibri", 60), bg="black", fg="white", bd=0)
legend_label = tk.Label(window, text="", font=(
    "Calibri", 40), bg="black", fg="white", bd=0)
info_label = tk.Label(window, text="", font=(
    "Calibri", 18), bg="black", fg="white", bd=0)

# Create dynamic visualizations
cpu_figure, cpu_ax = plt.subplots(figsize=(4, 2))
cpu_figure.set_facecolor('black')
cpu_ax.set_facecolor('black')
cpu_ax.set_xlabel('CPU Usage (%)', color='white')
cpu_ax.set_ylabel('', color='white')
cpu_ax.tick_params(axis='both', colors='white')
cpu_canvas = FigureCanvasTkAgg(cpu_figure, master=window)
cpu_canvas.get_tk_widget().place(relx=0.1, rely=0.6, anchor='w')

gpu_figure, gpu_ax = plt.subplots(figsize=(4, 2))
gpu_figure.set_facecolor('black')
gpu_ax.set_facecolor('black')
gpu_ax.set_xlabel('GPU Usage (%)', color='white')
gpu_ax.set_ylabel('', color='white')
gpu_ax.tick_params(axis='both', colors='white')
gpu_canvas = FigureCanvasTkAgg(gpu_figure, master=window)
gpu_canvas.get_tk_widget().place(relx=0.4, rely=0.6, anchor='w')

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")

# Initialize a deque to store the health index history
health_index_history = deque(maxlen=10)


def get_hardware_info():
    # Code for getting hardware information
    # ...
    pass


def calculate_component_state(value, warning_threshold, critical_threshold):
    if value >= critical_threshold:
        return "red", "Critical"
    elif value >= warning_threshold:
        return "orange", "Warning"
    else:
        return "white", "Okay"


def calculate_health_index(cpu_usage, gpu_usage, ram_usage, disk_usage, hardware_info):
    # Code for calculating health index
    # ...
    pass


def system_health_monitor():
    # Code for monitoring system health
    # ...

    # Update dynamic visualizations
    cpu_ax.clear()
    cpu_ax.plot([cpu_value], 'o-', color='white')
    cpu_canvas.draw()

    gpu_ax.clear()
    gpu_ax.plot([gpu_value], 'o-', color='white')
    gpu_canvas.draw()

    return f"{health_index} / 100"


def get_last_restart():
    # Code for getting last restart time
    # ...
    pass


def timer_from_start_of_program():
    # Code for calculating timer from start of program
    # ...
    pass


def update_labels():
    # Code for updating labels
    # ...

    window.after(1000, update_labels)


# Pack the widgets and start the main loop
time_label.place(relx=0.5, rely=0.4, anchor='center')
date_label.place(relx=0.5, rely=0.5, anchor='center')
health_label.place(relx=0.5, rely=0.2, anchor='center')
legend_label.place(relx=0.5, rely=0.1, anchor='center')
info_label.place(relx=0.5, rely=0.8, anchor='center')

update_labels()
window.mainloop()
