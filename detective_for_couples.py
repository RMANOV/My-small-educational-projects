import datetime
from collections import defaultdict
import pandas as pd

def detective(user):
    # Read data from file and convert to dictionary
    def read_excel_data("C:/Users/r.manov/Desktop/xxx.xlsx"):
        df = pd.read_excel(C:/Users/r.manov/Desktop/xxx.xlsx)
        return df.values.tolist()

    
    # with open("C:/Users/r.manov/Desktop/Data.txt", "r") as f:
    #     data = [line.strip().split() for line in f]
    #     data = [
    #         {
    #             k: v
    #             for k, v in zip(
    #                 ["ip", "mac", "user", "first", "last", "count", "active"], row
    #             )
    #         }
    #         for row in data
    #     ]
    #     for i in data:
    #         i['first'] = datetime.datetime.strptime(i['first'], "%d.%m.%Y %H:%M:%S")
    #         # convert the first date to datetime object
    #         # i[f"first"] = datetime.datetime.strptime(i[f"first"], "%d.%m.%Y %H:%M:%S")
    #         i["last"] = datetime.datetime.strptime(i["last"], "%d.%m.%Y %H:%M:%S")
    #         i["count"] = int(i["count"])

    # Create a dictionary of paired devices
    paired_devices = defaultdict(list)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if (
                data[i]["mac"] != data[j]["mac"]
                and abs((data[i]["first"] - data[j]["last"]).total_seconds()) <= 420
            ):
                paired_devices[data[i]["mac"]].append(data[j])
                paired_devices[data[j]["mac"]].append(data[i])

    # Count the number of times each pair of devices are detected together
    count_dict = defaultdict(int)
    for dev, paired in paired_devices.items():
        for pair in paired:
            count_dict[tuple(sorted([dev, pair["mac"]]))] += 1

    # Sort the pairs by the number of times they are detected together
    sorted_pairs = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

    # Create a list of devices that are connected and disconnected more than 3 times together
    together = []
    for pair, count in sorted_pairs:
        if count >= 3:
            together.extend(pair)

    # Sort the list of devices by the number of times they are connected and disconnected together
    together = sorted(set(together), key=lambda x: together.count(x), reverse=True)

    # Create a list of all devices that have been detected and their pairing information
    paired_info = []
    for dev in data:
        paired_with = [
            pair for pair in paired_devices[dev["mac"]] if pair["user"] != dev["user"]
        ]
        if paired_with:
            paired_info.append(
                [
                    dev["user"],
                    dev["first"],
                    dev["last"],
                    dev["count"],
                    dev["mac"],
                    dev["ip"],
                    paired_with,
                ]
            )

    # Create a list of devices that are connected and disconnected more than 3 times together with the given device owner
    detected_devices = [
        info
        for info in paired_info
        if info[0] == user and any(pair["user"] == user for pair in info[6])
    ]
    return detected_devices, together


def main():
    # Read data from Excel file
    data = read_excel_data("C:/Users/r.manov/Desktop/xxx.xlsx")
    # Get the list of devices that are connected and disconnected more than 3 times together with the given device owner
    detected_devices, together = detective("user")
    # Print the list of devices that are connected and disconnected more than 3 times together with the given device owner
    print(*detected_devices, sep="\n")
    # Print the list of devices that are connected and disconnected more than 3 times together
    print(*together, sep="\n")
    # Print the number of times the devices are connected and disconnected together
    print(len(together))

if __name__ == "__main__":
    main()
