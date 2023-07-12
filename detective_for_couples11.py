## This is a help utility for the purpose of the project "Detective for couples".
# The utility is used to process the output of the NirSoft's Wireless Network Watcher. 
# Its purpose is to help - in a specific way - to identify the owners of the devices that connect to the networks. 
#  - identify the owner of several specific devices, 
#  - as well as to show which owners, with which of their devices, enter/exit the networks and 
#  - to determine the formed groups of owners connecting to the networks simultaneously - in sync.
# 
# This code reads in your data, creates a graph where nodes represent devices and edges represent relationships between devices, 
# then it applies two community detection algorithms (Louvain and Girvan-Newman) to find communities (or clusters) of devices that are closely related. 
# Finally, it prints out the results of the community detection for each algorithm.
# The Louvain method is a fast and accurate method for community detection in large networks, 
# but it's a heuristic method that might not find the globally optimal partition of your network. 
# The Girvan-Newman method is a more classical approach based on the concept of edge betweenness, 
# but it might be slower for large networks. For best results I am using both and comparing their results.





import datetime
import networkx as nx
import community as community_louvain
from networkx.algorithms import community

def read_data(file_path):
    devices = []
    with open(file_path, "r", encoding="utf-16") as f:
        device = {"User Text": "", "First Detected On": "", "Last Detected On": "", "IP Address": "", "MAC Address": "", "Network Adapter Company": "", "Detection Count": "", "Active": ""}
        
        # count lines in file
        lines = f.readlines()
        lines_count = len(lines)
        f.seek(0)


        # read line by line and comlete device dictionary - when line is empty - add device to devices list and create new device dictionary
        while True:
            line = f.readline()
            if not line:
                break
            


            # when line is '==================================================\n' - add device to devices list and create new device dictionary


            new_device_count = 0
            if line == "\n" or line == "\r\n" or line == '==================================================\n' or line == '==================================================\r\n':
                new_device_count += 1
                if new_device_count == 2:
                    devices.append(device)
                    device = {"User Text": "", "First Detected On": "", "Last Detected On": "", "IP Address": "", "MAC Address": "", "Network Adapter Company": "", "Detection Count": "", "Active": ""}
                    new_device_count = 0
                else:
                    device = {"User Text": "", "First Detected On": "", "Last Detected On": "", "IP Address": "", "MAC Address": "", "Network Adapter Company": "", "Detection Count": "", "Active": ""}

                continue
            # create a list from string - remove any white spaces and split by ":"
            line = line.strip()

            # divide line in two parts - before and after ":" - if after split - line didnt have 2 elements - continue
            line = line.split(":")

            # delete white spaces before ":" and after ":" in line
            line = [x.strip() for x in line]
            line = [x for x in line if x != '']
            if len(line) < 2:
                continue
            



            # delete white spaces before ":" in line - 'IP Address        : 192.168.1.116\n' ==> 'IP Address: and 192.168.1.116
            
            # line = ":".join(line[0:1]).strip() + ":" + line[1].strip()
            
            # delete white spaces after ":" in line - 'IP Address:
            # line = line.split(":")
            # if after split - line didnt have 2 elements - continue
            


            if line[0] == "User Text":
                device["User Text"] = line[1]
            elif line[0] == "First Detected On" or line[0] == "Last Detected On":
                # ['First Detected On', '07.07.2023 г. 12', '13', '38']
                # replace " г." with ""
                line[1] = line[1].replace(" г.", "")
                date, time = line[1].split(" ")
                day, month, year = date.split(".")
                second = line[3]
                minute = line[2]
                hour = time
                device[line[0]] = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
                date,time, day, month, year, second, minute, hour = "", "", "", "", "", "", "", ""

            elif line[0] == "IP Address":
                device["IP Address"] = line[1]
            elif line[0] == "MAC Address":
                device["MAC Address"] = line[1]
            elif line[0] == "Network Adapter Company":
                device["Network Adapter Company"] = line[1]
            elif line[0] == 'Detection Count':
                device["Detection Count"] = line[1]
            elif line[0] == 'Active':
                device["Active"] = line[1]
            else:
                devices.append(device)
                devices = [x for x in devices if x != {} or device["MAC Address"] == "" or device["First Detected On"] == "" or device["Last Detected On"] == ""]
                continue

        # remove devices that didnt have first and last detected on
        devices = [x for x in devices if x["First Detected On"] != "" and x["Last Detected On"] != ""]

    return devices

def create_graph(devices):
    G = nx.Graph()
    while True:
        if len(devices) == 0:
            break
        device = devices.pop(0)
        G.add_node(device["MAC Address"], attr_dict=device)
        for other_device in devices:
            first_difference = abs(device["First Detected On"] - other_device["First Detected On"])
            last_difference = abs(device["Last Detected On"] - other_device["Last Detected On"])
            if last_difference <= datetime.timedelta(minutes=5) or first_difference <= datetime.timedelta(minutes=5):
                if not G.has_node(other_device["MAC Address"]):
                    G.add_node(other_device["MAC Address"], attr_dict=other_device)
                if G.has_edge(device["MAC Address"], other_device["MAC Address"]):
                    G[device["MAC Address"]][other_device["MAC Address"]]["weight"] += 1
                else:
                    G.add_edge(device["MAC Address"], other_device["MAC Address"], weight=1)
    
    # use this code to find the best partition
    communities_generator = community.girvan_newman(G)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)

    # Convert communities into a partition
    partition1 = {node: i for i, community in enumerate(next_level_communities) for node in community}

    return G, partition1





devices = read_data("C:/Users/r.manov/OneDrive/Работен плот/data.txt")
devices_copy = devices.copy()
G, partition1 = create_graph(devices)
modularity = community_louvain.modularity(partition1, G)

closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

partition = community_louvain.best_partition(G)



def print_results(partition, closeness_centrality, betweenness_centrality, devices_copy):
        # print only devices that are in the same community
        # start community number from 1
        # replace mac adress with user text
        # print devices user text in community
        # use set to print only unique devices
        for community in set(partition.values()):
            print("Louvain Community number: ", community + 1)
            device_set = set()
            for device in devices_copy:
                if partition[device["MAC Address"]] == community:
                    # use set to print only unique devices
                    device_set.add(device["User Text"])
            for device in device_set:
                print(device)
            print("==================================================")

print_results(partition, closeness_centrality, betweenness_centrality, devices_copy)


def print_results1(partition1, devices_copy):
    communities = {}
    for node in partition1:
        if partition1[node] not in communities:
            communities[partition1[node]] = [node]
        else:
            communities[partition1[node]].append(node)

    for community in communities:
        print("Girvan_newman Community number: ", community + 1)
        device_set = set()
        for device in devices_copy:
            if device["MAC Address"] in communities[community]:
                # use set to print only unique devices
                device_set.add(device["User Text"])
        for device in device_set:
            print(device)
        print("==================================================")

print_results1(partition1, devices_copy)
