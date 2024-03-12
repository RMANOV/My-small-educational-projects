

import datetime
import time


def calculate_finish_time():
    lecture_hours = float(input("Enter lecture length (hours): "))
    lecture_minutes = float(input("Enter lecture length (minutes): "))

    total_minutes = (lecture_hours * 60) + lecture_minutes

    speed = 1.6  # default speed
    speed = float(
        input("What speed will you watch at? (press enter for default 1.6x): ") or speed)

    playback_minutes = total_minutes / speed

    current_time = datetime.datetime.now()
    finish_time = current_time + datetime.timedelta(minutes=playback_minutes)

    return finish_time.strftime("%H:%M")


finish_time = calculate_finish_time()
print('Now is :              ', datetime.datetime.now().strftime("%H:%M"))
print("Estimated finish time:", finish_time)
