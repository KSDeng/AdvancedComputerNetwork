from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

def str_gt(s1, s2):
    num1 = int(s1.lstrip('s'))
    num2 = int(s2.lstrip('s'))
    return num1 > num2



def path_length_stat(graph):
    host_set = list()
    other_set = list()
    for k,v in graph.nodes.data():
        if v['type'] == 'host':
            host_set.append(k)
        else:
            other_set.append(k)
    p = nx.shortest_path_length(graph, host_set[0])
    for node in other_set:
        p.pop(node)
    stat = defaultdict(lambda: 0)
    for _, v in p.items():
        stat[v] += 1
    for k, v in stat.items():
        stat[k] = v / len(host_set)
#         print(f"{k}: {v}")
    return stat