import datetime
import tkinter as tk
import os
import re
import psutil

# Main window setup
window = tk.Tk()
window.title("System Information Screensaver")
window.state('zoomed')
window.configure(background='black')

# Initialize labels with some default values to ensure they appear
labels = {
    "time": tk.Label(window, text="Loading Time...", font=("Calibri", 400), bg="black", fg="white"),
    "date": tk.Label(window, text="Loading Date...", font=("Calibri", 24), bg="black", fg="white"),
    "uptime": tk.Label(window, text="Calculating Uptime...", font=("Calibri", 24), bg="black", fg="white"),
    "health": tk.Label(window, text="Calculating Health...", font=("Calibri", 60), bg="black", fg="white"),
    "legend": tk.Label(window, text="Checking System...", font=("Calibri", 40), bg="black", fg="white"),
    "info": tk.Label(window, text="Gathering Info...", font=("Calibri", 14), bg="black", fg="white"),
    "cpu": tk.Label(window, text="Checking CPU...", font=("Calibri", 14), bg="black", fg="white"),
    "ram": tk.Label(window, text="Checking RAM...", font=("Calibri", 14), bg="black", fg="white"),
    "disk": tk.Label(window, text="Checking Disk...", font=("Calibri", 14), bg="black", fg="white"),
    "network": tk.Label(window, text="Checking Network...", font=("Calibri", 14), bg="black", fg="white"),
    "temperature": tk.Label(window, text="Temperature: N/A", font=("Calibri", 14), bg="black", fg="white")
}

# Positioning labels
labels['date'].pack(side=tk.TOP, fill=tk.X)
labels['uptime'].pack(side=tk.TOP, fill=tk.X)
labels['time'].pack(expand=True)
labels['health'].pack(side=tk.TOP, fill=tk.X)
labels['legend'].pack(side=tk.TOP, fill=tk.X)
labels['cpu'].place(relx=1.0, rely=0.0, anchor='ne')
labels['ram'].place(relx=1.0, rely=0.05, anchor='ne')
labels['disk'].place(relx=1.0, rely=0.1, anchor='ne')
labels['network'].place(relx=1.0, rely=0.15, anchor='ne')
labels['temperature'].place(relx=1.0, rely=0.2, anchor='ne')
labels['info'].pack(side=tk.BOTTOM, fill=tk.X)

def get_system_uptime():
    # Calculate system uptime
    try:
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_string = str(datetime.timedelta(seconds=int(uptime_seconds)))
        return f"System Uptime: {uptime_string}"
    except Exception as e:
        return "System Uptime: Unavailable"

def update_labels():
    # Get current data
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%d.%m.%Y")
    current_day_name = datetime.datetime.now().strftime("%A")
    system_uptime = get_system_uptime()
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_usage = psutil.net_io_counters().bytes_sent + \
        psutil.net_io_counters().bytes_recv

    # Update labels with current data
    labels['time'].config(text=current_time)
    labels['date'].config(text=f"Date: {current_date}\nDay: {current_day_name}")
    labels['uptime'].config(text=system_uptime)
    labels['health'].config(text=f"System Health Index: Calculating...", fg="white")
    labels['legend'].config(text=f"System running with minimal issues", fg="white")
    labels['cpu'].config(text=f"CPU Usage: {cpu_usage}%", fg="white")
    labels['ram'].config(text=f"RAM Usage: {ram_usage}%", fg="white")
    labels['disk'].config(text=f"Disk Usage: {disk_usage}%", fg="white")
    labels['network'].config(text=f"Network Usage: {network_usage / 1024 / 1024:.2f} MB/s", fg="white")
    labels['temperature'].config(text=f"Temperature: N/A", fg="white")

    # Schedule next update
    window.after(1000, update_labels)

# Call the update function initially to start the loop
update_labels()

# Disable window resizing to prevent flickering
window.resizable(False, False)

# Run the main loop
window.mainloop()
