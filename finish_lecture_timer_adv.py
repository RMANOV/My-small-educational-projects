

import datetime
import time

lecture_hours = float(input("Enter lecture length (hours): "))
lecture_minutes = float(input("Enter lecture length (minutes): "))

total_minutes = (lecture_hours * 60) + lecture_minutes  

speed = 1.6 # default speed 
speed = float(input("What speed will you watch at? (press enter for default 1.6x): ") or speed)

playback_minutes = total_minutes / speed 

print("Starting lecture...")

while True:
    current_time = datetime.datetime.now().time()  
    print("Current time is:", current_time)

    current_hour = int(datetime.datetime.now().strftime("%H"))
    current_minute = int(datetime.datetime.now().strftime("%M"))

    finish_time_minutes = current_minute + playback_minutes
    finish_time_hours = current_hour

    if finish_time_minutes >= 60:
        finish_time_minutes -= 60
        finish_time_hours += 1

    finish_time = str(finish_time_hours) + ":" + str(round(finish_time_minutes)) 
    print("Estimated finish time:", finish_time)
    
    time.sleep(60)

print("Lecture finished!")