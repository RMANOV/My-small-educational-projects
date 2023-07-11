import datetime
import networkx as nx
import community as community_louvain

def read_data(file_path):
    data = []
    with open(file_path, "r", encoding="utf-16") as f:
        device = {}
        for line in f:
            line = line.strip()
            if "==================================================" in line:
                if device == {}:
                    device = {"User Text": "", "First Detected On": datetime.datetime.now(), "Last Detected On": datetime.datetime.now()}
                if "==================================================" in line:
                    if device:
                        data.append(device)
                    device = {"User Text": "", "First Detected On": datetime.datetime.now(), "Last Detected On": datetime.datetime.now()}
                else:
                    if "User Text:" in line:
                        device["User Text"] = line.split(":")[1].strip()
                    elif "First Detected On:" in line:
                        device["First Detected On"] = datetime.datetime.strptime(line.split(":")[1].strip(), "%d.%m.%Y %H:%M:%S")
                    elif "Last Detected On:" in line:
                        device["Last Detected On"] = datetime.datetime.strptime(line.split(":")[1].strip(), "%d.%m.%Y %H:%M:%S")
    return data

def create_graph(data):
    G = nx.Graph()
    while data:
        device = data.pop()
        G.add_node(device["User Text"])
        for other_device in data:
            if device["User Text"] != other_device["User Text"]:
                if device["First Detected On"] <= other_device["Last Detected On"] and device["Last Detected On"] >= other_device["First Detected On"]:
                    G.add_edge(device["User Text"], other_device["User Text"])



    return G

data = read_data("C:/Users/r.manov/OneDrive/Работен плот/data.txt")

G = create_graph(data)

closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

partition = community_louvain.best_partition(G)


# print results
def print_results(partition, closeness_centrality, betweenness_centrality):
    for community in set(partition.values()):
        print("Community", community)
        for node in partition:
            if partition[node] == community:
                print(node, closeness_centrality[node], betweenness_centrality[node])
        print()

print_results(partition, closeness_centrality, betweenness_centrality)
