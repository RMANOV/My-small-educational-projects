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
# sorted by the number of times they were seen together - +/- X minutes difference in the time of connection or disconnection
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
import datetime

logging.basicConfig(filename="log.txt", level=logging.DEBUG)


def read_data(file_path):
    data = []
    with open(file_path, "r") as f:
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
            # strip any whitespace from the line
            line = list(line.strip(" "))
            line_lenght = len(line)
            if line_lenght < 3:
                line.pop()
                line_count -= 1
                continue
            # skip lines that start with '==='
            if line[0] == "=" or line[1] == "=" or line[2] == "=":
                line.pop()
                line_count -= 1
                continue

            # split the line into key and value and strip any whitespace
            if "IP Address" in line:
                device["ip"] = " ".join(iterable=line).split(":")[1].strip()
            elif "Device Name" in line:
                device["name"] = " ".join(iterable=line).split(":")[1].strip()
            elif "MAC Address" in line:
                device["mac"] = " ".join(iterable=line).split(":")[1].strip()
            elif "Network Adapter Company" in line:
                device["company"] = " ".join(iterable=line).split(":")[1].strip()
            elif "User Text" in line:
                device["user"] = " ".join(iterable=line).split(":")[1].strip()
            elif "First Detected On" in line:
                device["first"] = " ".join(iterable=line).split(":")[1].strip()
            elif "Last Detected On" in line:
                device["last"] = " ".join(iterable=line).split(":")[1].strip()
            elif "Detection Count" in line:
                device["count"] = int(" ".join(iterable=line).split(":")[1].strip())
            elif "Active" in line:
                device["active"] = " ".join(iterable=line).split(":")[1].strip()
                data.append(device)
                device = {} # reset the device dictionary
            else:
                continue
    return data


def get_together(data):
    # create a dictionary where the key is the device and the value is a list of other devices that were seen together - 
    # connect and disconnect at least 3 times, in difference of +/- X minutes
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
    for device in data:
        for other_device in data:
            if device["mac"] != other_device["mac"]:
                if device["first"] == other_device["first"]:
                    if abs(device["first"] - other_device["first"]) <= datetime.timedelta(minutes=5): # check if the difference between the first detection of the device and the first detection of the other device is less than 5 minutes
                        together[device["mac"]].append(other_device["mac"])
                if device["last"] == other_device["last"]:
                    if abs(device["last"] - other_device["last"]) <= datetime.timedelta(minutes=5): # check if the difference between the last detection of the device and the last detection of the other device is less than 5 minutes
                        together[device["mac"]].append(other_device["mac"])
    # sort the dictionary by the number of times the device was seen with another device - by the counter
    together = {k: v for k, v in sorted(together.items(), key=lambda item: len(item[1]), reverse=True)}
    return together



def write_together(together, file_path):
    with open(file_path, "w") as f:
        for device, other_devices in together.items():
            f.write(f"{device} - {other_devices}") # write the device and other devices to the file

def main():
    data = read_data("devices.txt")
    together = get_together(data)
    write_together(together, "together.txt")

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
#                 device["ip"] = " ".join(iterable=line).split(":")[1].strip()
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
