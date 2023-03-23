# Read lines from a file and parse them into a list of dictionaries
# Each dictionary represents a device
# The list of dictionaries is returned
# The data file is expected to have the following format without duplicates:
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
# Old implementation of the function
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
# The file should not have a trailing line separator
# The file should not contain duplicates
# The file should not contain empty lines
# The file should not contain lines with only whitespace
# The file should not contain lines with only whitespace and a newline
# New implementation of the function - using apriori algorithm
# Calculate the number of times each device was seen with another device
# Return a list of devices that were seen together connect and disconnect at least 3 times,
# sorted by the number of times they were seen together - +/- X minutes intersection in the time of connection or disconnection
# The list should be sorted by the number of times the device was seen with another device
# Every record in the list should be a treated as a transaction in aprirori algorithm
# Aprirori algorithm should be used to find the most frequent itemsets of devices that were seen together
# The result is 2 lists of itemsets - owners and seen together - 
# difference is in the number of times they were seen together and shortest time interval between 
# the first and last time they were seen together
 







import datetime
import logging
from apyori import apriori
import itertools
from collections import defaultdict, Counter


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
    # create a set where each element is a tuple of (device MAC address, device first detection time)
    devices = {(device["mac"], device["first"]) for device in data}

    # create a dictionary where the key is the device MAC address and the value is a set of other device "user text"
    # that were seen together at least 3 times within +/- 5 minutes
    together = defaultdict(set)
    for device1 in devices:
        for device2 in devices:
            if device1 == device2:
                continue
            if abs((device1[1] - device2[1]).total_seconds()) <= 600:
                if len(together[device1[0]]) < 5 and len(together[device2[0]]) < 5:
                    together[device1[0]].add(device2[0]) # add the other device MAC address to the set
                    together[device2[0]].add(device1[0]) # add the other device MAC address to the set

    # create a dictionary where the key is the owner name and the value is a set of device MAC addresses
    # that the owner owns, based on the first and last detection times of each device
    owners = defaultdict(set)
    for device in data:
        if not device["user"]:
            continue
        for other_device in data:
            if device["mac"] == other_device["mac"]:
                continue
            if device["user"] == other_device["user"]:
                continue
            if abs((device["first"] - other_device["first"]).total_seconds()) <= 100:
                if abs((device["last"] - other_device["last"]).total_seconds()) <= 100:
                    # owners[device["user"]].add(device["mac"])
                    owners[device["user"]].add(other_device["user"])








    # count how many times each device was seen with other devices
    device_counts = Counter(device for devices in together.values() for device in devices)

    # sort the devices by the number of other devices they were seen with
    sorted_devices = sorted(devices, key=lambda device: device_counts[device[0]], reverse=True)

    # sort the owners by the number of devices they own that were seen with other devices
    owners = sorted(owners.items(), key=lambda owner: sum(device_counts[device] for device in owner[1]), reverse=True)

    return together, owners



    # implementation of Apriori algorithm - values of the dictionaries treat like transactions to find frequent itemsets
def get_unique_groups_together_apriory(together):
    transactions = list(together.values())
    results = list(apriori(transactions, min_support=0.02, min_confidence=0.9))
    unique_groups_together2 = []

    for itemset in results:
        devices = tuple(sorted([device for device in itemset.items]))
        if not any(devices in group for group in unique_groups_together2):
            unique_groups_together2.append(devices)

    # create a set from every tuple in the list
    # check if the current set have 2/3  or more same elements with another set - if yes - join the sets, if not - continue
    # remove all empty sets
    for i in range(len(unique_groups_together2)):
        for j in range(len(unique_groups_together2)):
            if i != j:
                if (
                    len(
                        set(unique_groups_together2[i]).intersection(
                            set(unique_groups_together2[j])
                        )
                    )
                    >= len(unique_groups_together2[i]) * 0.7
                ):
                    unique_groups_together2[i] = set(unique_groups_together2[i]).union(
                        set(unique_groups_together2[j])
                    )
                    unique_groups_together2[j] = set()
                else:
                    continue
    # remove all empty sets
    unique_groups_together2 = [x for x in unique_groups_together2 if x]

    return unique_groups_together2


def get_unique_groups_owners_apriory(owners):
    transactions = list(owners.values())
    results = list(apriori(transactions, min_support=0.02, min_confidence=0.9))
    unique_groups_owners2 = []

    for itemset in results:
        devices = tuple(sorted([device for device in itemset.items]))
        if not any(devices in group for group in unique_groups_owners2):
            unique_groups_owners2.append(devices)

    # create a set from every tuple in the list
    # check if the current set have 2/3  or more same elements with another set - if yes - join the sets, if not - continue
    # remove all empty sets
    for i in range(len(unique_groups_owners2)):
        for j in range(len(unique_groups_owners2)):
            if i != j:
                if (
                    len(
                        set(unique_groups_owners2[i]).intersection(
                            set(unique_groups_owners2[j])
                        )
                    )
                    >= len(unique_groups_owners2[i]) * 0.7
                ):
                    unique_groups_owners2[i] = set(unique_groups_owners2[i]).union(
                        set(unique_groups_owners2[j])
                    )
                    unique_groups_owners2[j] = set()
                else:
                    continue

    # remove all empty sets
    unique_groups_owners2 = [x for x in unique_groups_owners2 if x]

    return unique_groups_owners2

def create_unique_groups_of_devices_seen_together(together, data):
    counts = {}
    for k, v in together.items():
        # replace every "mac" with "user" - in the v and k
        pair = frozenset([device["user"] for device in data if device["mac"] == k] + [device["user"] for device in data if device["mac"] in v])
        # pair = frozenset([k] + list(v))
        counts[pair] = counts.get(pair, 0) + 1
        


    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    unique_groups_together = [x[0] for x in sorted_counts]

    # # check if the current set have 2/3  or more same elements with another set - if yes - join the sets, if not - continue
    # for i in range(len(unique_groups_together)):
    #     for j in range(len(unique_groups_together)):
    #         if i != j:
    #             if (
    #                 len(
    #                     set(unique_groups_together[i]).intersection(
    #                         set(unique_groups_together[j])
    #                     )
    #                 )
    #                 >= len(unique_groups_together[i]) * 0.95
    #             ):
    #                 unique_groups_together[i] = set(unique_groups_together[i]).union(
    #                     set(unique_groups_together[j])
    #                 )
    #                 unique_groups_together[j] = set()
    #             else:
    #                 continue

    # remove all empty sets
    unique_groups_together = [x for x in unique_groups_together if x]

    return unique_groups_together


def create_unique_groups_of_devices_owned_by_same_person(owners, data):
    # create a list of tuples - each tuple is a group of devices owned by the same person
    unique_groups_owners = []
    # for each owner create set of all the devices owned by him
    for owner in owners:
        # create an empty set
        # add the owner to the set
        # add all the devices owned by the owner to the set
        # add the set to the list
        # remove old record from the list
        # from  this ('ALEX XXX', {'JESSIKA', 'TANIO XXX', 'ALEX SOYKOVA LI4EN NOV XXX'})
        # create this frozenset ('ALEX XXX', 'JESSIKA', 'TANIO XXX', 'ALEX SOYKOVA LI4EN NOV XXX')
        # and add it to the list
        unique_groups_owners.append( frozenset([owner[0]] + list(owner[1])) )

   
    # check if the current set have 2/3  or more same elements with another set - if yes - join the sets, if not - continue
    # remove all empty sets
    # for i in range(len(unique_groups_owners)):
    #     for j in range(len(unique_groups_owners)):
    #         if i != j:
    #             if (
    #                 len(
    #                     set(unique_groups_owners[i]).intersection(
    #                         set(unique_groups_owners[j])
    #                     )
    #                 )
    #                 >= len(unique_groups_owners[i]) * 0.95
    #             ):
    #                 unique_groups_owners[i] = set(unique_groups_owners[i]).union(
    #                     set(unique_groups_owners[j])
    #                 )
    #                 unique_groups_owners[j] = set()
    #             else:
    #                 continue

    # remove all empty sets
    unique_groups_owners = [x for x in unique_groups_owners if x]


    

    


    return unique_groups_owners



def write_together(file_path, data, unique_groups_together, unique_groups_owners):
    with open(file_path, "w") as f:
        print(f"==========================================================")
        f.write(f"==========================================================")
        number_of_group = len(unique_groups_together)
        for group in unique_groups_together:
            print(
                f" Group {number_of_group} of {len(unique_groups_together)} --{len(group)} devices  together\n"
            )
            # print every element of this frozenset({'ALEX SOYKOVA PC', 'BOBY', 'DAMIANOV PC'}) in a new line
            for element in group:
                print(element)
                f.write(element + " ")

            # print(
            #     f" *** { group[0]} *** - {len(group[1:])} devices \n" + f"{group[1:]}\n" 
                    
            # )
            print(f"********************")

            # write it in File
            # f.write(f" Group {number_of_group} -- together")
            # # print every element of the tuple in a new line
            # f.write(
            #     f" *** { group[0]} *** - {len(group[1:])} devices \n" + f"{group[1:]}\n"
            # )
            # f.write(f"********************")
            number_of_group -= 1
        print(f"==========================================================")
        # f.write(f"==========================================================")

        owners_group = len(unique_groups_owners)
        for group in unique_groups_owners:
            print(f" Group {owners_group} of {len(unique_groups_owners)} -- {len(group)} owners")
            # print every element of the tuple in a new line
            # print every element in a new line - {'TANIO XXX', 'JESSIKA', 'ALEX SOYKOVA LI4EN NOV XXX', 'ALEX XXX'}
            # TANIO XXX
            # JESSIKA
            # ALEX SOYKOVA LI4EN NOV XXX
            # if frozenset - print in one line
            for element in group:
                print(element)
                f.write(element + " ")
            print(f"********************")
            # write it in File
            # f.write(f" Group { owners_group} -- owners")
            # # print every element of the tuple in a new line
            # f.write(
            #     f" *** { group[0]} *** - {len(group[1:])} devices \n" + f"{group[1:]}\n"
            # )
            # f.write(f"********************")
            owners_group -= 1


def write_together2(file_path, data, unique_groups_together2, unique_groups_owners2):
    with open(file_path, "w") as f:
        print(f"==========================================================")
        f.write(f"==========================================================")
        number_of_group = len(unique_groups_together2)
        for group in unique_groups_together2:
            print(
                f" Group {number_of_group} of {len(unique_groups_together2)} -- together - apriori"
            )
            # list with dictionaries, that content sets -  print every set in a new line
            print(*group, sep="\n")
            print(f"********************")
            number_of_group -= 1
            # write it in File
            # f.write(f" Group {number_of_group} -- together - apriori")
            # print every element of the tuple in a new line
            # f.write(*group, sep="\n")
            # f.write(f"********************")

        print(f"==========================================================")
        f.write(f"==========================================================")

        owners_group = len(unique_groups_owners2)
        for group in unique_groups_owners2:
            print(
                f" Group {owners_group} of {len(unique_groups_owners2)} -- owners - apriori"
            )
            print(*group, sep="\n")
            print(f"********************")
            owners_group -= 1
            # write it in File


def main():
    data = read_data("devices.txt")
    together, owners = find_together(data)
    unique_groups_together = create_unique_groups_of_devices_seen_together(together, data)
    unique_groups_owners = create_unique_groups_of_devices_owned_by_same_person(owners, data)
    write_together("together.txt", data, unique_groups_together, unique_groups_owners)
    # apriory algorithm
    unique_groups_together2 = get_unique_groups_together_apriory(together)
    unique_groups_owners2 = get_unique_groups_owners_apriory(owners)
    write_together2(
        "together.txt", data, unique_groups_together2, unique_groups_owners2
    )


if __name__ == "__main__":
    main()
