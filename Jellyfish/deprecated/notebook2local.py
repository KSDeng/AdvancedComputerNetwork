import networkx as nx
import random
import matplotlib.pyplot as plt
import fnss
import numpy as np
from itertools import islice


def build_fattree_graph(k):
    """
    Uses the fnss library to build a fat tree topology with k-port switches

    Parameters
    ----------
    k: int
      Number of ports per fat tree switch

    Returns
    -------
    fnss.DatacenterTopology
    """
    return fnss.fat_tree_topology(k)

def str_gt(s1, s2):
    num1 = int(s1.lstrip('s'))
    num2 = int(s2.lstrip('s'))
    return num1 > num2

def build_jellyfish_graph(num_racks, switch_degree, num_hosts_per_rack):
    """
    Uses the networkx library to build a JellyFish topology with given parameters

    Parameters
    ----------
    num_racks: int
      Total number of racks. Also, equivalent to the number of switches
      Called "N" in the JellyFish paper

    switch_degree: int
      Total number of ports per switch
      Called "k" in the JellyFish paper

    num_hosts_per_rack: int
      Total number of hosts (servers) per rack
      Called "(k - r)" in the JellyFish paper

    Returns
    -------
    networkx.Graph
      A JellyFish topology graph. Each node is tagged with an attribute called 'type'.
      Possible values for 'type' are 'host' or 'switch'.
    """

    if num_racks * (switch_degree - num_hosts_per_rack) % 2 != 0:
        print("N * r must be even!")
        return None
    if not 0 <= switch_degree < num_racks:
        print("0 <= k < N must be satisfied!")
        return None
    if not 0 <= (switch_degree - num_hosts_per_rack) < num_racks:
        print("0 <= r < N must be satisfied!")
        return None

    # initialize
    graph = nx.Graph()

    # add switches and hosts
    switch_set = []
    for i in range(0, num_racks):
        switch_set.append('s%s' % i)
        graph.add_node('s%s' % i, type='switch')

    host_set = []
    for i in range(0, num_hosts_per_rack * num_racks):
        host_set.append('h%s' % i)
        graph.add_node('h%s' % i, type='host')

    # initialize switch set, using a dictionary. key: node. value: number of free ports.
    # remove k-v pair whose v=0
    switch_port_dict = {node: switch_degree - num_hosts_per_rack for node in graph.nodes if
                        graph.nodes[node].get('type') == 'switch'}
    #     print(switch_port_dict)

    switches = switch_port_dict.copy()
    while switches:
        # (x,y) -> (p1,x), (p2,y)
        if len(switches) == 1:
            node = list(switches.keys())[0]
            if switches[node] >= 2:
                choosable_switches = [s for s in switch_set if s != node]
                x = random.choice(choosable_switches)
                x_choosable_neighbors = [n for n in graph.neighbors(x) if
                                         n != node and graph.nodes[n].get('type') == 'switch']
                y = random.choice(x_choosable_neighbors)
                if str_gt(x, y):
                    x, y = y, x
                graph.remove_edge(x, y)
                if str_gt(x, node):
                    graph.add_edge(node, x)
                else:
                    graph.add_edge(x, node)
                if str_gt(y, node):
                    graph.add_edge(node, y)
                else:
                    graph.add_edge(y, node)
                switches[node] -= 2
                if switches[node] == 0:
                    switches.pop(node)
                continue

        # randomly choose two switches and link them
        # restart the whole process when no switch-switch edge can be added to reduce the num of free ports
        restart = False
        while True:
            s1 = random.choice(list(switches.keys()))
            choosable_switches = [s for s in switches.keys() if s != s1 and s not in graph.neighbors(s1)]
            if not choosable_switches:
                restart = True
                for sw1 in switches.keys():
                    for sw2 in switches.keys():
                        if sw1 != sw2:
                            if sw2 not in graph.neighbors(sw1):
                                restart = False
                if restart:
                    break
            else:
                break

        if restart:
            switches = switch_port_dict.copy()
            graph.clear_edges()
            continue

        s2 = random.choice(choosable_switches)
        if str_gt(s1, s2):
            s1, s2 = s2, s1
        graph.add_edge(s1, s2)
        switches[s1] -= 1
        switches[s2] -= 1
        if switches[s1] == 0:
            switches.pop(s1)
        if switches[s2] == 0:
            switches.pop(s2)

    # add edge between switches and hosts
    for i in range(0, num_racks):
        for j in range(0, num_hosts_per_rack):
            graph.add_edge('s%s' % (i), 'h%s' % (i * num_hosts_per_rack + j))

    # add edge between switches and hosts
    while switch_set:
        sw = switch_set.pop(0)
        for _ in range(num_hosts_per_rack):
            host = host_set.pop(0)
            graph.add_edge(sw, host)

    return graph


def build_jellyfish_graph_identical_equipment_as_fattree(num_racks, num_racks_with_hosts, switch_degree,
                                                         num_hosts_per_rack):
    """
    Uses the networkx library to build a JellyFish-like(same equipment as fat tree) topology with given parameters

    Parameters
    ----------
    num_racks: int
      Total number of racks. Also, equivalent to the number of switches
      Called "N" in the JellyFish paper

    num_racks_with_hosts: int
      Number of racks whose neighbors include hosts

    switch_degree: int
      Total number of ports per switch
      Called "k" in the JellyFish paper

    num_hosts_per_rack: int
      Total number of hosts (servers) per rack
      Called "(k - r)" in the JellyFish paper

    Returns
    -------
    networkx.Graph
      A JellyFish topology graph. Each node is tagged with an attribute called 'type'.
      Possible values for 'type' are 'host' or 'switch'.
    """
    if (num_racks_with_hosts * (switch_degree - num_hosts_per_rack) + (
            num_racks - num_racks_with_hosts) * switch_degree) % 2 != 0:
        print("N * r must be even!")
        return None
    if not 0 <= switch_degree < num_racks:
        print("0 <= k < N must be satisfied!")
        return None
    if not 0 <= (switch_degree - num_hosts_per_rack) < num_racks:
        print("0 <= r < N must be satisfied!")
        return None

    # initialize
    graph = nx.Graph()

    # add switches and hosts
    switch_set = []
    for i in range(0, num_racks):
        switch_set.append('s%s' % i)
        graph.add_node('s%s' % i, type='switch')

    host_set = []
    for i in range(0, num_hosts_per_rack * num_racks_with_hosts):
        host_set.append('h%s' % i)
        graph.add_node('h%s' % i, type='host')

    # initialize switch set, using a dictionary. key: node. value: number of free ports.
    # remove k-v pair whose v=0
    switch_port_dict = {node: switch_degree - num_hosts_per_rack for node in graph.nodes if
                        graph.nodes[node].get('type') == 'switch'}

    # randomly choose (num_racks - num_racks_with_hosts) switches without edges to hosts
    switches_no_hosts = random.sample(switch_set, num_racks - num_racks_with_hosts)
    for sw in switches_no_hosts:
        switch_port_dict[sw] = switch_degree
    #     print(switch_port_dict)

    switches = switch_port_dict.copy()
    while switches:
        # (x,y) -> (p1,x), (p2,y)
        if len(switches) == 1:
            node = list(switches.keys())[0]
            if switches[node] >= 2:
                choosable_switches = [s for s in switch_set if s != node]
                x = random.choice(choosable_switches)
                x_choosable_neighbors = [n for n in graph.neighbors(x) if
                                         x != node and graph.nodes[n].get('type') == 'switch']
                y = random.choice(x_choosable_neighbors)
                if str_gt(x, y):
                    x, y = y, x
                graph.remove_edge(x, y)
                if str_gt(x, node):
                    graph.add_edge(node, x)
                else:
                    graph.add_edge(x, node)
                if str_gt(y, node):
                    graph.add_edge(node, y)
                else:
                    graph.add_edge(y, node)
                switches[node] -= 2
                if switches[node] == 0:
                    switches.pop(node)
                continue

        # randomly choose two switches and link them
        # restart the whole process when no switch-switch edge can be added to reduce the num of free ports
        restart = False
        while True:
            s1 = random.choice(list(switches.keys()))
            choosable_switches = [s for s in switches.keys() if s != s1 and s not in graph.neighbors(s1)]
            if not choosable_switches:
                restart = True
                for sw1 in switches.keys():
                    for sw2 in switches.keys():
                        if sw1 != sw2:
                            if sw2 not in graph.neighbors(sw1):
                                restart = False
                if restart:
                    break
            else:
                break

        if restart:
            switches = switch_port_dict.copy()
            graph.clear_edges()
            continue

        s2 = random.choice(choosable_switches)
        if str_gt(s1, s2):
            s1, s2 = s2, s1
        graph.add_edge(s1, s2)
        switches[s1] -= 1
        switches[s2] -= 1
        if switches[s1] == 0:
            switches.pop(s1)
        if switches[s2] == 0:
            switches.pop(s2)

    # add edge between switches and hosts
    while switch_set:
        sw = switch_set.pop(0)
        if sw not in switches_no_hosts:
            for _ in range(num_hosts_per_rack):
                host = host_set.pop(0)
                graph.add_edge(sw, host)

    return graph







# figure 1(a)
fat_tree_4 = build_fattree_graph(4)
draw_topo_graph(fat_tree_4, 'figure1(a).png')

g = build_jellyfish_graph(16, 4, 1)

# figure 1(b)
jellyfish_like = build_jellyfish_graph_identical_equipment_as_fattree(20, 16, 4, 1)
draw_topo_graph(jellyfish_like, "figure1(b).png")

# one graph path distribution
fat_tree_14 = build_fattree_graph(14)
path_distribution_ft14 = path_length_stat(fat_tree_14)
print(path_distribution_ft14)

jellyfish_686 = build_jellyfish_graph_identical_equipment_as_fattree(245, 230, 14, 3)
path_distribution_jf686 = path_length_stat(jellyfish_686)
print(path_distribution_jf686)

# 10 graphs path distribution
fattree_14_10_means = path_length_stat_10_means(build_fattree_graph, k=14)
print(fattree_14_10_means)

jellyfish_686_10_means = path_length_stat_10_means(build_jellyfish_graph_identical_equipment_as_fattree,
                                                   num_racks=245, num_racks_with_hosts=230,
                                                   switch_degree=14, num_hosts_per_rack=3)
print(jellyfish_686_10_means)

# figure 1(c)
draw_path_stat(fattree_14_10_means, jellyfish_686_10_means, "figure1(c).png")

# figure 2(a) bisection bandwidth
fattree_normalized_bisection_bw(N=720, k=32)

jellyfish_normalized_bisection_bw(2880, 64, 47)

plot_normalized_bi_bw('figure2(a).png')

# figure 2(b) equipment cost
plot_equipment_cost("figure2(b).png")

# figure 9 distinct path
jellyfish686 = build_jellyfish_graph_identical_equipment_as_fattree(245, 230, 14, 3)
plot_distinct_paths(jellyfish686, "figure 9.png")
