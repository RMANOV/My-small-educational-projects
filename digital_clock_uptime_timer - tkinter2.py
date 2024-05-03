import datetime
import tkinter as tk
import os
import re

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
info_label = tk.Label(
    window, text="", font=("Calibri", 14), bg="black", fg="white", bd=0
)

# Get the time of start of the program
time_of_start = datetime.datetime.now().strftime("%H:%M:%S")
date_of_start = datetime.datetime.now().strftime("%d.%m.%Y")

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

    # Calculate the uptime in days and hours
    if last_r:
        uptime = f'{(datetime.datetime.now() - datetime.datetime.strptime(last_r[0], "%d.%m.%Y")).days} days, {(datetime.datetime.now() - datetime.datetime.strptime(last_r[1], "%H:%M:%S")).seconds // 3600} hours'
    else:
        uptime = "Uptime data not available"

    # Update the labels
    time_label.config(text=current_time)
    date_label.config(text=f"Date: {current_date}\nDay: {current_day_name}")
    info_label.config(text=f"Uptime: {uptime}\nTimer from start: {timer1}")

    # Schedule the function to run again after 1 second
    window.after(1000, update_time)

# Call the update_time function to start updating the label text
update_time()

# Pack the label widgets into the window
date_label.pack(side=tk.TOP, fill=tk.X)
time_label.pack(expand=True)
info_label.pack(side=tk.BOTTOM, fill=tk.X)

# Run the main loop
window.mainloop()
