

# now is 19 h 51 m
# my lecture is 1h 30m long
# i watch it 1.6x faster
# when will it finish - 20 h 57 m

# If your lecture is 1h 30m long and you watch it 1.6x faster, then it will take you 1h 30m / 1.6 = 56m 15s to finish it.
# If you start watching it at 19 h 51 m, then it will finish at 19 h 51 m + 56 m 15 s = 20 h 47 m 15 s.

import datetime

current_time = datetime.datetime.now().time()
print("Current time:", current_time)

lecture_hours = float(input("Enter lecture length (hours): "))
lecture_minutes = float(input("Enter lecture length (minutes): "))

total_minutes = (lecture_hours * 60) + lecture_minutes

speed = float(input("What speed will you watch at? (1 = normal): "))

playback_minutes = total_minutes / speed

current_hour = int(datetime.datetime.now().strftime("%H"))
current_minute = int(datetime.datetime.now().strftime("%M"))

finish_time_minutes = current_minute + playback_minutes
finish_time_hours = current_hour

if finish_time_minutes >= 60:
    finish_time_minutes -= 60
    finish_time_hours += 1

finish_time = str(finish_time_hours) + ":" + str(round(finish_time_minutes))
print("You will finish at:", finish_time)

input("Press enter to exit")
