# Read lines from a file and parse them into a list of dictionaries
# Each dictionary represents a device
# The list of dictionaries is returned
# The file is expected to have the following format:
# ===
# IP Address:
# Device Name:
# MAC Address:
# Network Adapter Company:
# User Text:
# First Detected On:
# Last Detected On:
# Detection Count:
# Active:
# ===
# Calculate the number of times each device was seen with another device
# Return a list of devices that were seen together connect and disconnect at least 3 times,
# sorted by the number of times they were seen together - +/- X minutes intersection in the time of connection or disconnection
# The list should be sorted by the number of times the device was seen with another device
# If two devices were seen together the same number of times, sort them by the user_text
# Store the result in a file called "together.txt"
# The file should have the following format:
# ===
# User Text: - Device Name: - MAC Address: - IP Address:
# User Text: - Device Name: - MAC Address: - IP Address:
# ===
# The file should be sorted by the number of times the device was seen with another device - for every device in the list of devices
# If two devices were seen together the same number of times, sort them by the user_text
# The file should be encoded in UTF-8
# The file should have Unix line endings
# The file should not have a trailing newline
# The file should not have a trailing space
# The file should not have a trailing TabError()
# The file should not have a trailing carriage return
# The file should not have a trailing carriage return line feed
# The file should not have a trailing line feed
# The file should not have a trailing form feed
# The file should not have a trailing vertical TabError()
# The file should not have a trailing next line
# The file should not have a trailing no-break space
# In the next run of the program, the file should be suplemented with the new data and new results
# The file should not contain duplicates
# The file should not contain empty lines
# The file should not contain lines with only whitespace
# The file should not contain lines with only whitespace and a newline


import datetime
from collections import defaultdict
import logging


logging.basicConfig(filename="log.txt", level=logging.DEBUG)


def read_data(file_path):
    data = []
    with open("C:/Users/r.manov/Desktop/Data.txt", "r") as f:
        device = {
            "user": "",
            "first": "",
            "last": "",
            "count": 0,
            "mac": "",
            "ip": "",
            "company": [],
            "active": False,
            "name": "",
        }
        # count the number of lines in the file
        line_count = sum(1 for line in f)
        # reset the file pointer to the beginning of the file
        f.seek(0)
        # iterate over the lines in the file_path

        for line in f:
            # ['\x00', 'I', '\x00', 'P', '\x00', ' ', '\x00', 'A', '\x00', 'd', '\x00', 'd', '\x00', 'r', ...]
            # ['я', 'ю', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', '=', ...]
            # ['I', 'P', ' ', 'A', 'd', 'd', 'r', 'e', 's', 's', ' ', ' ', ' ', ' ', ...]
            # remove the 'я' and 'ю' character from the line - it is not a valid character

            # line = [ char for char in line if char != "я" ]
            # line = [ char for char in line if char != "ю" ]
            # convert the list of characters to a string
            # line = "".join(line)
            line = [char for char in line if char != "\x00"]
            # line = list(line.strip(" "))
            line_lenght = len(line)
            if line_lenght < 3 or line_lenght > 80:
                # line.pop()
                line_count -= 1
                continue
            # skip lines that start with '==='
            if line[0] == "=" or line[1] == "=" or line[2] == "=":
                # line.pop()
                line_count -= 1
                continue

            line = "".join(line)
            # 'IP Address        : 192.168.1.35\n'
            # strip the newline character from the end of the line
            line = line.strip("\n")
            # convert the line to a list with the separator ':'
            line = line.split(":")

            if "First Detected On" in line[0] or "Last Detected On" in line[0]:
                # 'First Detected On : 04.03.2023 3\x04. 05:57:14'
                # 'Last Detected On  : 04.03.2023 3\x04. 05:57:14'
                # remove the '3\x04.' from the line
                # remove the trailing whitespace from the line
                line[1] = line[1].replace("3\x04.", " ")
                line[1] = line[1].strip()

                # separate date
                date = line[1].split(" ")
                # ['', '04.03.2023', '3\x04.', '05']
                # get only the date in index 1
                date = date[0]
                if date == "":
                    continue
                # convert to a datetime object
                day, month, year = date.split(".")  # ['04', '03', '2023']
                # convert the date to a datetime object
                date = datetime.datetime(int(year), int(month), int(day))

                # separate time from line '['First Detected On ', '04.03.2023   05', '57', '14']' - '05:57:14'
                line[1] = line[1].strip()
                # time is a last 6 digits in the line
                # seconds = 14
                # minutes = 57
                # hours = 05
                # convert the line to a string and get the last 6 digits - seconds, minutes and hours
                line_string = "".join(line)
                hours = line_string[-6:-4]
                minutes = line_string[-4:-2]
                seconds = line_string[-2:]
                # convert the time to a datetime object
                time = datetime.datetime(
                    1, 1, 1, int(hours), int(minutes), int(seconds)
                )
                # combine the date and time to a datetime object
                line[1] = datetime.datetime.combine(date, time.time())
                # add the datetime object to the device dictionary
                if "First Detected On" in line[0]:
                    device["first"] = line[1]
                elif "Last Detected On" in line[0]:
                    device["last"] = line[1]
                continue

            # split the line into key and value and strip any whitespace
            if "IP Address" in line[0]:
                device["ip"] = line[1].strip()
            elif "Device Name" in line[0]:
                device["name"] = line[1].strip()
            elif "MAC Address" in line[0]:
                device["mac"] = line[1].strip()
            elif "Network Adapter Company" in line[0]:
                device["company"] = line[1].strip()
            elif "User Text" in line[0]:
                device["user"] = line[1].strip()
            elif "First Detected On" in line[0]:
                device["first"] = line[1].strip()
            elif "Last Detected On" in line[0]:
                device["last"] = line[1].strip()
            elif "Detection Count" in line[0]:
                device["count"] = int(line[1].strip())
            elif "Active" in line[0]:
                device["active"] = line[1].strip()
                data.append(device)
                device = {}  # reset the device dictionary
            else:
                continue
        # if "first" or "last" is missing - remove the device from the list
        data = [device for device in data if "first" in device and "last" in device]
        return data


def find_together(data):
    # create a dictionary where the key is the device and the value is a list of other devices that were seen together -
    # connect and disconnect at least 3 times, in intersection of +/- X minutes
    # the list should be sorted by the number of times the device was seen with another device
    # 1.Iterate over the list of devices
    # check if the device is not the same as the other device - by comparing mac addresses
    # check if the devices date of first detection are the same
    #   check if connecting is within the +/- X minutes - if so - set counter +=1 and add the device to the list of other devices
    #   check if disconnecting is within the +/- X minutes - if so - set counter +=1 and add the device to the list of other devices
    # check if the devices date of last detection are the same
    #   check if connecting is within the +/- X minutes - if so - set counter +=1 and add the device to the list of other devices
    #   check if disconnecting is within the +/- X minutes - if so - set counter +=1 and add the device to the list of other devices
    # Add the device and the list of other devices to the dictionary and the counter for each other device
    # 2. In the end - sort the dictionary by the number of times the device was seen with another device - by the counter
    # 3. If two devices were seen together the same number of times, sort them by the user_text

    together = defaultdict(list)

    # If "first"  - minutes - is the same for more than 5 devices - ignore that 'first' - it is the start of scaning
    # count how many devices have the same 'first' and 'last' - if more than 5 - ignore that 'first' and 'last' - it is the start of scaning and the end of scaning
    # iterate over the list of devices and check if the 'first' and 'last' are the same for more than 5 devices - create a set of 'first' and 'last' and check the length of the set
    # if so - ignore that 'first' and 'last' - it is the start of scaning and the end of scaning
    first_set = set()
    last_set = set()
    for device in data:
        devices_with_same_first = 0
        devices_with_same_last = 0
        for other_device in data:

            if (
                not device["first"]
                or not other_device["first"]
                or not device["last"]
                or not other_device["last"]
            ):
                continue
            try:
                if device["first"] == other_device["first"]:
                    devices_with_same_first += 1
                if device["last"] == other_device["last"]:
                    devices_with_same_last += 1
            except KeyError:
                continue

        if devices_with_same_first > 5:
            first_set.add(device["first"])
            continue
        if devices_with_same_last > 5:
            last_set.add(device["last"])
            continue

    # if the 'first' and 'last' is same - the owner is one person - create a dictionary where the key is the user of the device and the value is a list of other devices that were seen together
    owners = defaultdict(list)

    for device in data:
        if device["first"] in first_set:
            continue
        if device["last"] in last_set:
            continue
        for other_device in data:
            if device["mac"] == other_device["mac"]:
                continue
            if device["first"] == other_device["first"]:
                if (device["first"] - other_device["first"]).total_seconds() <= 30:
                    together[device["user"]].append(other_device["user"])
            if device["last"] == other_device["last"]:
                if (
                    device["last"] - other_device["last"]
                ).total_seconds() <= 30:  # cheks if the difference between the last detection is less than 5 minutes
                    together[device["user"]].append(other_device["user"])
                if (device["first"] - other_device["first"]).total_seconds() <= 10 and (
                    device["last"] - other_device["last"]
                ).total_seconds() <= 10:  # cheks if the difference between the first and last detection is less than 5 minutes
                    owners[device["user"]].append(other_device["user"])

    # sort the dictionary by the number of times the device was seen with another device
    owners = {
        k: sorted(v, key=lambda x: together[x], reverse=True) for k, v in owners.items()
    }
    # remove devices without first and last detection
    owners = {k: v for k, v in owners.items() if v}


    # sort the list by the length of the sets
    # unique_owners = sorted(unique_owners, key=len, reverse=True)
    # check if the current set is the subset or superset of the sets in the list
    # if the current set is the subset or superset of the sets in the list - remove the sets from the list
    # if the current set is not the subset or superset of the sets in the list - continue
    # for current_set in unique_owners:
    #     for other_set in unique_owners:
    #         if current_set == other_set:
    #             continue
    #         if current_set.issubset(other_set) or current_set.issuperset(other_set):
    #             unique_owners.remove(other_set)
    #         else:
    #             continue

    # Create a new set if there is a intersection between the current set and the sets in the list -
    # from the result of intersection - create a new set - remove result from the current set and the other set
    # if there is no intersection between the current set and the sets in the list - continue
    # Loop until there is only one set in the list
    # while len(unique_owners) > 1:
    #     # Keep track of whether we created a new set in this iteration
    #     created_new_set = False
    #     # Iterate over all pairs of sets
    #     for i, current_set in enumerate(unique_owners):
    #         for j, other_set in enumerate(unique_owners):
    #             if i == j:
    #                 # Don't compare a set to itself
    #                 continue
    #             # Find the intersection between the sets
    #             intersection = current_set.intersection(other_set)
    #             if intersection:
    #                 # If there is a intersection, create a new set and remove
    #                 # the intersection from the current and other sets
    #                 new_set = intersection
    #                 current_set.difference_update(new_set)
    #                 other_set.difference_update(new_set)
    #                 unique_owners.append(new_set)
    #                 created_new_set = True
    #                 print(*new_set, sep="\n")
    #                 print("*************")
    #     if not created_new_set:
    #         # If no new set was created in this iteration, there is no more
    #         # intersection to be found, so we can stop
    #         break

        # number_of_sets -= 1
        # for current_set in unique_owners:
        #     for other_set in unique_owners:
        #         if current_set == other_set:
        #             continue
        #         if current_set.symmetric_difference(other_set):
        #             new_set = current_set.symmetric_difference(other_set) # create a new set
        #             current_set.difference_update(new_set) # remove result from the current set
        #             other_set.difference_update(new_set) # remove result from the other set
        #             unique_owners.append(new_set) # add the new set to the list
        #             print(*new_set, sep="\n")
        #             print('*************')
        #             # wait 1 second to see the result
        #             # time.sleep(1)
        #         else:
        #             continue

    # check if the current set have more same elements with another set
    # if the current set have 2 or more same elements with another set - join the sets
    # if the current set have less than 2 same elements with another set - continue
    # for current_set in unique_owners:
    #     for other_set in unique_owners:
    #         if current_set == other_set:
    #             continue
    #         if (
    #             len(current_set.intersection(other_set)) >= len(current_set) * 0.9
    #         ):  # if the current set have 90% or more same elements with another set - join the sets
    #             current_set.update(other_set)
    #             unique_owners.remove(other_set)
    #         else:
    #             continue

    # first_set = set()
    # last_set = set()
    # for device in data:
    #     try:
    #         first_set.add(device["first"])
    #         last_set.add(device["last"])
    #     except KeyError:
    #         continue
    #     devices_with_same_first = 0
    #     devices_with_same_last = 0
    #     for other_device in data:
    #         try:
    #             if device["first"] == other_device["first"]:
    #                 devices_with_same_first += 1
    #             if device["last"] == other_device["last"]:
    #                 devices_with_same_last += 1
    #         except KeyError:
    #             continue

    #     if devices_with_same_first > 5:
    #         continue
    #     if devices_with_same_last > 5:
    #         continue

    # for device in data:
    #     for other_device in data:
    #         if device["mac"] != other_device["mac"]:
    #             # if first or last of one of the devices is missing - skip
    #             if "first" not in device or "first" not in other_device:
    #                 continue
    #             # if the first detection of the device is not in the set of all the first detections of the devices - skip
    #             try:
    #                 if device["first"] not in first_set:
    #                     continue
    #                 if device["last"] not in last_set:
    #                     continue

    #                 if device["first"] == other_device["first"]:
    #                     if device["last"] == other_device["last"]:
    #                         together[device["mac"]].append(other_device["mac"])
    #                     else:
    #                         continue
    #                 else:
    #                     continue
    #             except KeyError:
    #                 continue

    # for device in data:
    #     for other_device in data:
    #         if device["mac"] != other_device["mac"]:
    #             # if first or last of one of the devices is missing - skip
    #             if "first" not in device or "first" not in other_device:
    #                 continue

    #             # if the first detection of the device is not in the set of all the first detections of the devices - skip
    #             if device["first"] not in first_set:
    #                 continue
    #             # if the last detection of the device is not in the set of all the last detections of the devices - skip
    #             if device["last"] not in last_set:
    #                 continue

    #             # if the first detection of the device is the same as the first detection of the other device
    #             if device["first"] == other_device["first"]:
    #                 # check if the intersection between the first detection of the device and the first detection of the other device is less than 5 minutes
    #                 if abs(
    #                     device["first"] - other_device["first"]
    #                 ) <= datetime.timedelta(
    #                     minutes=5
    #                 ):
    #                     together[device["mac"]].append(other_device["mac"])
    #             # if the last detection of the device is the same as the last detection of the other device
    #             if device["last"] == other_device["last"]:
    #                 # check if the intersection between the last detection of the device and the last detection of the other device is less than 5 minutes
    #                 if abs(device["last"] - other_device["last"]) <= datetime.timedelta(
    #                     minutes=5
    #                 ):
    #                     together[device["mac"]].append(other_device["mac"])
    #             # if the first detection of the device is the same as the last detection of the other device
    #             if device["first"] == other_device["last"]:
    #                 # check if the intersection between the first detection of the device and the last detection of the other device is less than 5 minutes
    #                 if abs(device["first"] - other_device["last"]) <= datetime.timedelta(
    #                     minutes=5
    #                 ):
    #                     together[device["mac"]].append(other_device["mac"])
    #             # if the last detection of the device is the same as the first detection of the other device
    #             if device["last"] == other_device["first"]:
    #                 # check if the intersection between the last detection of the device and the first detection of the other device is less than 5 minutes
    #                 if abs(device["last"] - other_device["first"]) <= datetime.timedelta(
    #                     minutes=5
    #                 ):
    #                     together[device["mac"]].append(other_device["mac"])

    # return together

    # for device in data:
    #     for other_device in data:
    #         if device["mac"] != other_device["mac"]:
    #             # if first or last of one of the devices is missing - skip
    #             if "first" not in device or "first" not in other_device:
    #                 continue

    #             if device["first"] == other_device["first"]:
    #                 if abs(
    #                     device["first"] - other_device["first"]
    #                 ) <= datetime.timedelta(
    #                     minutes=5
    #                 ):  # check if the intersection between the first detection of the device and the first detection of the other device is less than 5 minutes
    #                     together[device["mac"]].append(other_device["mac"])
    #             if device["last"] == other_device["last"]:
    #                 if abs(device["last"] - other_device["last"]) <= datetime.timedelta(
    #                     minutes=5
    #                 ):  # check if the intersection between the last detection of the device and the last detection of the other device is less than 5 minutes
    #                     together[device["mac"]].append(other_device["mac"])
    # sort the dictionary by the number of times the device was seen with another device - by the counter
    together = {
        k: v
        for k, v in sorted(
            together.items(), key=lambda item: len(item[1]), reverse=True
        )
    }

    # Filter the dictionary to contain only devices that were seen together at least 3 times
    together = {k: v for k, v in together.items() if len(v) >= 3}


    # from every pair key-value in the dictionary - create a set of the key and the value
    # check if the current set is same as the sets in the list
    # if the current set is not the same as the sets in the list - add it to the list
    # if the current set is the same as the sets in the list - continue
    unique_owners = []
    for k, v in owners.items():
        current_set = set()
        current_set.add(k)
        current_set.update(v)
        if current_set not in unique_owners:
            unique_owners.append(current_set)
        else:
            continue

    unique_sets_together = []
    for k, v in together.items():
        current_set = set()
        current_set.add(k)
        current_set.update(v)
        if current_set not in unique_sets_together:
            unique_sets_together.append(current_set)
        else:
            continue

    
    # check if the set of unique devices is subset or superset of another set of unique devices
    # if it is - remove the set, in not - continue
    # for i in range(len(unique_sets_together)):
    #     for j in range(len(unique_sets_together)):
    #         if i != j:
    #             if unique_sets_together[i].issubset(unique_sets_together[j]):
    #                 unique_sets_together[i] = set()
    #             elif unique_sets_together[i].issuperset(unique_sets_together[j]):
    #                 unique_sets_together[j] = set()
    #             else:
    #                 continue

    # Create a new set if there is a intersection between the current set and the sets in the list -
    # from the result of simmetric intersection - create a new set - remove result from the current set and from other set -
    # add the result to the new set
    # if there is no intersection between the current set and the sets in the list - continue
    # Loop until there is only one set in the list
    # while len(unique_sets_together) > 1:
    #     # Keep track of whether we created a new set in this iteration
    #     created_new_set = False
    #     # Iterate over all pairs of sets
    #     for i, set1 in enumerate(unique_sets_together):
    #         for j, set2 in enumerate(unique_sets_together):
    #             if i == j:
    #                 # Don't compare a set to itself
    #                 continue
    #             # Find the intersection between the sets
    #             intersections = set1.intersection(set2)
    #             if intersections:
    #                 # If there is a intersection, create a new set and remove
    #                 # the intersection from set1 and set2 and add the result to the new set
    #                 new_set = intersections
    #                 unique_sets_together[i] = set1.intersection(new_set)
    #                 unique_sets_together[j] = set2.intersection(new_set)
    #                 unique_sets_together.append(new_set)
    #                 created_new_set = True
    #                 print(*new_set, sep="\n")
    #                 print("*************")
    #     if not created_new_set:
    #         # If no new set was created in this iteration, there is no more
    #         # intersection to be found, so we can stop
    #         break

    # check if the current set have 2 or more same elements with another set
    # if the current set have half or more same elements with another set - join the sets
    # if the current set have less than 2 same elements with another set - continue
    # for i in range(len(unique_sets_together)):
    #     for j in range(len(unique_sets_together)):
    #         if i != j:
    #             if (
    #                 len(unique_sets_together[i].intersection(unique_sets_together[j]))
    #                 >= len(unique_sets_together[i]) * 0.9
    #             ):
    #                 unique_sets_together[i] = unique_sets_together[i].union(
    #                     unique_sets_together[j]
    #                 )
    #                 unique_sets_together[j] = set()
    #             else:
    #                 continue

    # remove all empty sets
    unique_sets_together = [x for x in unique_sets_together if x]

    return unique_sets_together, unique_owners


# replace all mac addresses to user text in the dictionary and write the result to a file together.txt and print the result to the console
def write_together(unique_sets_together, file_path, data, unique_owners):
    with open(file_path, "w") as f:
        # print every set of unique devices and the number of times they were seen together
        # set1
        # device1
        # device2
        # device3
        # devicex
        # **************
        # set2
        # device1
        # device2

        print(f"==========================================================")
        f.write(f"==========================================================")
        number_of_group = 0
        for group in unique_sets_together:
            number_of_group += 1

            print(
                f"{number_of_group} group together - number of devices is {len(group)}"
            )
            f.write(f"{number_of_group}")
            for device in group:
                print(f"{device}")
                f.write(f"{device}")
            print(f"**********************")
            f.write(f"**********************")

        # print every set of unique owners and the number of times they were seen together
        # set1
        # device1
        # device2
        # device3
        # devicex
        # **************
        # set2
        # device1
        # device2

        print(f"==========================================================")
        f.write(f"==========================================================")
        number_of_group = 0
        for group in unique_owners:
            number_of_group += 1

            print(f"{number_of_group} owners - number of devices is {len(group)}")
            f.write(f"{number_of_group}")
            for device in group:
                print(f"{device}")
                f.write(f"{device}")
            print(f"**********************")
            f.write(f"**********************")

        # for device, other_devices in together.items():
        #     for other_device in other_devices:
        #         for d in data:
        #             if d["mac"] == device:
        #                 device = d["user"]
        #             if d["mac"] == other_device:
        #                 other_device = d["user"]
        #     f.write(f"{device} - {other_device} - {len(other_devices)}\r")
        #     print(f"{device} - {other_device} - {len(other_devices)}\r")
        #     print(f'**********************')
        # print(f'==========================================================')

        # for owner, devices in owners.items():
        #     # replace mac addresses to user text
        #     # write the result to a file together.txt and print the result to the console
        #     # owner
        #     # device1, device2, device3, device4, device5 etc.

        #     f.write(f'{owner}\r')
        #     print(f'{owner}\r')
        #     # replace mac addresses to user text in the dictionary
        #     devices_names = [d["user"] for d in data if d["mac"] in devices]
        #     for device in devices_names:
        #         f.write(f'{device}\r')
        #         print(f'{device}\r')
        #     print(f'**********************')
        #     f.write(f'**********************\r')
        # print(f'==========================================================')


def main():
    data = read_data("devices.txt")
    unique_sets_together, unique_owners = find_together(data)
    write_together(unique_sets_together, "together.txt", data, unique_owners)


if __name__ == "__main__":
    main()


# def read_data(file_path):
#     data = []
#     with open(file_path, "r") as f:
#         device = {
#             "user": "",
#             "first": "",
#             "last": "",
#             "count": 0,
#             "mac": "",
#             "ip": "",
#             "company": [],
#             "active": False,
#             "name": "",
#         }
#         # count the number of lines in the file
#         line_count = sum(1 for line in f)
#         # reset the file pointer to the beginning of the file
#         f.seek(0)
#         # iterate over the lines in the file_path

#         for line in f:
#             # strip any whitespace from the line
#             line = list(line.strip(" "))
#             line_lenght = len(line)
#             if line_lenght < 3:
#                 line.pop()
#                 line_count -= 1
#                 continue
#             # skip lines that start with '==='
#             if line[0] == "=" or line[1] == "=" or line[2] == "=":
#                 line.pop()
#                 line_count -= 1
#                 continue

#             # split the line into key and value and strip any whitespace
#             if "IP Address" in line:
#                 device["ip"] = line[1].strip()
#             elif "Device Name" in line:
#                 device["name"] = line.split(":")[1].strip()
#             elif "MAC Address" in line:
#                 device["mac"] = line.split(":")[1].strip()
#             elif "Network Adapter Company":
#                 device["company"].append(line[0].split(":")[1].strip())
#             elif "User Text":
#                 device["user"] = line.split(":")[1].strip()
#             elif "First Detected On":
#                 try:
#                     device["first"] = datetime.datetime.strptime(
#                         line.split(":")[1].strip(), "%d.%m.%Y г. %H:%M:%S"
#                     )
#                 except ValueError:
#                     logging.warning(
#                         f"Failed to parse 'First Detected On' field: {line}"
#                     )
#             elif "Last Detected On":
#                 try:
#                     device["last"] = datetime.datetime.strptime(
#                         line.split(":")[1].strip(), "%d.%m.%Y г. %H:%M:%S"
#                     )
#                 except ValueError:
#                     logging.warning(f"Failed to parse 'Last Detected On' field: {line}")
#             elif "Detection Count":
#                 try:
#                     device["count"] = int(line.split(":")[1].strip())
#                 except ValueError:
#                     logging.warning(f"Failed to parse 'Detection Count' field: {line}")
#             elif "Active":
#                 device["active"] = line.split(":")[1].strip() == "Yes"
#             else:
#                 logging.warning(f"Skipping unrecognized line: {line}")

#             # check if we have all the required fields for a device
#             if all(
#                 key in device
#                 for key in (
#                     "ip",
#                     "name",
#                     "mac",
#                     "company",
#                     "user",
#                     "first",
#                     "last",
#                     "count",
#                     "active",
#                 )
#             ):
#                 # add the device to the list and reset the device dict
#                 data.append(device)
#                 device = {}

#     return data

#     #     for line in f:
#     #         line = line.strip()
#     #         if "==="):
#     #             if device:
#     #                 data.append(device)
#     #                 device = {}
#     #         elif line:
#     #             key, value = line.split(":", 1)
#     #             device[key.strip()] = value.strip()
#     #     if device:
#     #         data.append(device)
#     # for row in data:
#     #     row["first"] = datetime.datetime.strptime(row["first"], "%d.%m.%Y %H:%M:%S")
#     #     row["last"] = datetime.datetime.strptime(row["last"], "%d.%m.%Y %H:%M:%S")
#     #     row["count"] = int(row["count"])
#     # return data


# def get_paired_devices(data):
#     paired_devices = defaultdict(list)
#     for i in range(len(data)):
#         for j in range(i + 1, len(data)):
#             if (
#                 data[i]["mac"] != data[j]["mac"]
#                 and abs((data[i]["first"] - data[j]["last"]).total_seconds()) <= 420
#             ):
#                 paired_devices[data[i]["mac"]].append(data[j])
#                 paired_devices[data[j]["mac"]].append(data[i])
#     return paired_devices


# def count_device_pairs(paired_devices):
#     count_dict = defaultdict(int)
#     for dev, paired in paired_devices.items():
#         for pair in paired:
#             count_dict[tuple(sorted([dev, pair["mac"]]))] += 1
#     return count_dict


# def get_together_devices(count_dict):
#     together = []
#     for pair, count in count_dict.items():
#         if count >= 3:
#             together.extend(pair)
#     together = sorted(set(together), key=lambda x: together.count(x), reverse=True)
#     return together


# def get_paired_info(data, paired_devices):
#     paired_info = []
#     for dev in data:
#         paired_with = [
#             pair for pair in paired_devices[dev["mac"]] if pair["user"] != dev["user"]
#         ]
#         if paired_with:
#             paired_info.append(
#                 (
#                     dev["user"],
#                     dev["first"],
#                     dev["last"],
#                     dev["count"],
#                     dev["mac"],
#                     dev["ip"],
#                     paired_with,
#                 )
#             )
#     return paired_info


# def detective(user):
#     data = read_data("C:/Users/r.manov/Desktop/Data.txt")
#     paired_devices = get_paired_devices(data)
#     count_dict = count_device_pairs(paired_devices)
#     together = get_together_devices(count_dict)
#     paired_info = get_paired_info(data, paired_devices)
#     detected_devices = [
#         (user, first, last, count, mac, ip, paired)
#         for user, first, last, count, mac, ip, paired in paired_info
#         if user == user and any(pair["user"] == user for pair in paired)
#     ]
#     return detected_devices, together


# def main():
#     detected_devices, together = detective("JULIA")
#     for user, first, last, count, mac, ip, paired in detected_devices:
#         print(user, first, last, count, mac, ip, [pair["user"] for pair in paired])
#     print(*together, sep="\n")
#     print(len(together))


# if __name__ == "__main__":
#     main()
