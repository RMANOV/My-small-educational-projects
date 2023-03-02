import datetime
from collections import defaultdict


def read_data(file_path):
    data = []
    with open(file_path, "r") as f:
        device = {}
        for line in f:
            line = line.strip()
            if line.startswith("==="):
                if device:
                    data.append(device)
                    device = {}
            elif line:
                key, value = line.split(":", 1)
                device[key.strip()] = value.strip()
        if device:
            data.append(device)
    for row in data:
        row["first"] = datetime.datetime.strptime(row["first"], "%d.%m.%Y %H:%M:%S")
        row["last"] = datetime.datetime.strptime(row["last"], "%d.%m.%Y %H:%M:%S")
        row["count"] = int(row["count"])
    return data


def get_paired_devices(data):
    paired_devices = defaultdict(list)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if (
                data[i]["mac"] != data[j]["mac"]
                and abs((data[i]["first"] - data[j]["last"]).total_seconds()) <= 420
            ):
                paired_devices[data[i]["mac"]].append(data[j])
                paired_devices[data[j]["mac"]].append(data[i])
    return paired_devices


def count_device_pairs(paired_devices):
    count_dict = defaultdict(int)
    for dev, paired in paired_devices.items():
        for pair in paired:
            count_dict[tuple(sorted([dev, pair["mac"]]))] += 1
    return count_dict


def get_together_devices(count_dict):
    together = []
    for pair, count in count_dict.items():
        if count >= 3:
            together.extend(pair)
    together = sorted(set(together), key=lambda x: together.count(x), reverse=True)
    return together


def get_paired_info(data, paired_devices):
    paired_info = []
    for dev in data:
        paired_with = [
            pair for pair in paired_devices[dev["mac"]] if pair["user"] != dev["user"]
        ]
        if paired_with:
            paired_info.append(
                (
                    dev["user"],
                    dev["first"],
                    dev["last"],
                    dev["count"],
                    dev["mac"],
                    dev["ip"],
                    paired_with,
                )
            )
    return paired_info


def detective(user):
    data = read_data("C:/Users/r.manov/Desktop/Data.txt")
    paired_devices = get_paired_devices(data)
    count_dict = count_device_pairs(paired_devices)
    together = get_together_devices(count_dict)
    paired_info = get_paired_info(data, paired_devices)
    detected_devices = [
        (user, first, last, count, mac, ip, paired)
        for user, first, last, count, mac, ip, paired in paired_info
        if user == user and any(pair["user"] == user for pair in paired)
    ]
    return detected_devices, together


def main():
    detected_devices, together = detective("JULIA")
    for user, first, last, count, mac, ip, paired in detected_devices:
        print(user, first, last, count, mac, ip, [pair["user"] for pair in paired])
    print(*together, sep="\n")
    print(len(together))


if __name__ == "__main__":
    main()
