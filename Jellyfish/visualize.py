import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from .utilities import *
# from utilities import *     # debug


def draw_topo_graph(topo_graph, outfile=None):
    """
    Uses matplotlib to draw the topology graph to the outfile. Uses different
    colors for the nodes if nodes have the attribute 'type' set to either
    'switch' or 'host'.

    Parameters
    ----------
    topo_graph: fnss.DatacenterTopology or networkx.Graph
      Input topology graph. Should be an object of type networkx.Graph OR fnss.DatacenterTopology
    outfile: string
      Path along with filename and extension to output the topology graph drawing

    Returns
    -------
    outfile: jpg, png, svg or pdf file depending on the file extension
      Draws the graph to the outfile.
    """

    switch_color = '#800000'
    host_color = '#808080'

    color_map = []
    for node, attributes in topo_graph.nodes.data():
        node_type = attributes.get('type')
        if node_type == 'switch':
            color_map.append(switch_color)
        elif node_type == 'host':
            color_map.append(host_color)

    if (len(color_map) > 0):
        nx.draw(topo_graph, node_color=color_map)
    else:
        nx.draw(topo_graph)
    if outfile:
        plt.savefig(outfile)

def draw_path_stat(fattree_14_10_means, jellyfish_686_10_means, outfile=None):
    fig, ax = plt.subplots(figsize=(10, 5))  # init figure with landscape aspect ratio

    x = []

    for k in fattree_14_10_means.keys():
        if k not in x:
            x.append(k)
    for k in jellyfish_686_10_means.keys():
        if k not in x:
            x.append(k)

    x = np.array(x)
    x = np.sort(x)

    fattree14_y = []
    jellyfish686_y = []

    for each in x:
        if each in fattree_14_10_means:
            fattree14_y.append(fattree_14_10_means[each])
        else:
            fattree14_y.append(0)
        if each in jellyfish_686_10_means:
            jellyfish686_y.append(jellyfish_686_10_means[each])
        else:
            jellyfish686_y.append(0)

    bar_width = 0.3

    # Bars for fattree
    ax.bar(x + bar_width, fattree14_y, label='Fat-tree', align='center',
           edgecolor='black', width=0.3, linewidth=1, hatch="xx",
           color="white")

    # Bars for jellyfish
    ax.bar(x, jellyfish686_y, label='Jellyfish', align='center',
           edgecolor='black', width=0.3, linewidth=1,
           color="#00008B")

    plt.xlabel('Path length', fontsize=15)
    plt.ylabel('Fraction of Server Pairs', fontsize=15)

    # y ranges from 0.0 to 1.0
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.1))
    plt.ylim(0, 1)

    plt.grid(linestyle=':')

    plt.xticks(x + bar_width / 2, x)
    plt.legend(fontsize=15)

    if outfile:
        plt.savefig(outfile)

def plot_normalized_bi_bw(outfile=None):
    fig, ax = plt.subplots(figsize=(16, 8))

    plt.grid(linestyle=':')

    # Fat-tree N=720, k=24
    fattree24_x, fattree24_y = fattree_normalized_bisection_bw(N=720, k=24)
    fattree24_x /= 1000
    ax.scatter(fattree24_x, fattree24_y, marker='^', c='black', s=200, label='Fat-tree;N=720;k=24')

    # Fat-tree N=1280, k=32
    fattree32_x, fattree32_y = fattree_normalized_bisection_bw(N=1280, k=32)
    fattree32_x /= 1000
    ax.scatter(fattree32_x, fattree32_y, marker='o', c='grey', s=200, label='Fat-tree;N=1280;k=32')

    # Fat-tree N=2880, k=48
    fattree48_x, fattree48_y = fattree_normalized_bisection_bw(N=2880, k=48)
    fattree48_x /= 1000
    ax.scatter(fattree48_x, fattree48_y, marker='s', c='red', s=200, label='Fat-tree;N=2880;k=48')

    # Jellyfish N=720, k=24
    jellyfish24_x = []
    jellyfish24_y = []
    for r in range(10, 22):  # obtain r from figure 2 (a). r ranges from [11, 20]
        x, y = jellyfish_normalized_bisection_bw(720, 24, r)
        jellyfish24_x.append(x / 1000)
        jellyfish24_y.append(y)
    ax.plot(jellyfish24_x, jellyfish24_y, marker='^', markerfacecolor='none', label='Jellyfish;N=720;k=24')

    # Jellyfish N=1280, k=32
    jellyfish32_x = []
    jellyfish32_y = []
    for r in range(13, 28):  # obtain r from figure 2 (a). r ranges from [14,26]
        x, y = jellyfish_normalized_bisection_bw(1280, 32, r)
        jellyfish32_x.append(x / 1000)
        jellyfish32_y.append(y)
    ax.plot(jellyfish32_x, jellyfish32_y, marker='o', c='r', markerfacecolor='none', label='Jellyfish;N=1280;k=32')

    # Jellyfish N=2880, k=48
    jellyfish48_x = []
    jellyfish48_y = []
    for r in range(20, 41):  # obtain r from figure 2 (a). r ranges from [21, 39]
        x, y = jellyfish_normalized_bisection_bw(2880, 48, r)
        jellyfish48_x.append(x / 1000)
        jellyfish48_y.append(y)
    ax.plot(jellyfish48_x, jellyfish48_y, marker='s', c='b', markerfacecolor='none', label='Jellyfish;N=2880;k=48')

    plt.legend(fontsize=15)

    plt.xlabel('Number of Servers in Thousands', fontsize=15)
    plt.ylabel('Normalized Bisection Bandwidth', fontsize=15)

    ax.axis(xmin=0, xmax=80)
    ax.axis(ymin=0.2, ymax=1.6)

    if outfile:
        plt.savefig(outfile)

def plot_normalized_bi_bw_using_res(res, outfile=None):
    fig, ax = plt.subplots(figsize=(16, 8))

    plt.grid(linestyle=':')

    # Fat-tree N=720, k=24
    fattree24_x, fattree24_y = res['fattree24_x'], res['fattree24_y']
    ax.scatter(fattree24_x, fattree24_y, marker='^', c='black', s=200, label='Fat-tree;N=720;k=24')

    # Fat-tree N=1280, k=32
    fattree32_x, fattree32_y = res['fattree32_x'], res['fattree32_y']
    ax.scatter(fattree32_x, fattree32_y, marker='o', c='grey', s=200, label='Fat-tree;N=1280;k=32')

    # Fat-tree N=2880, k=48
    fattree48_x, fattree48_y = res['fattree48_x'], res['fattree48_y']
    ax.scatter(fattree48_x, fattree48_y, marker='s', c='red', s=200, label='Fat-tree;N=2880;k=48')

    # Jellyfish N=720, k=24
    jellyfish24_x, jellyfish24_y = res['jellyfish24_x'], res['jellyfish24_y']
    ax.plot(jellyfish24_x, jellyfish24_y, marker='^', markerfacecolor='none', label='Jellyfish;N=720;k=24')

    # Jellyfish N=1280, k=32
    jellyfish32_x, jellyfish32_y = res['jellyfish32_x'], res['jellyfish32_y']
    ax.plot(jellyfish32_x, jellyfish32_y, marker='o', c='r', markerfacecolor='none', label='Jellyfish;N=1280;k=32')

    # Jellyfish N=2880, k=48
    jellyfish48_x, jellyfish48_y = res['jellyfish48_x'], res['jellyfish48_y']
    ax.plot(jellyfish48_x, jellyfish48_y, marker='s', c='b', markerfacecolor='none', label='Jellyfish;N=2880;k=48')

    plt.legend(fontsize=15)

    plt.xlabel('Number of Servers in Thousands', fontsize=15)
    plt.ylabel('Normalized Bisection Bandwidth', fontsize=15)

    ax.axis(xmin=0, xmax=80)
    ax.axis(ymin=0.2, ymax=1.6)

    if outfile:
        plt.savefig(outfile)

def plot_equipment_cost(outfile=None):
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.grid(linestyle=':')

    # jellyfish 24 ports
    k = 24
    r = 19
    jellyfish24_x = [0, 80]
    jellyfish24_y = []
    for x in jellyfish24_x:
        jellyfish24_y.append(k / (k - r) * x)
    ax.plot(jellyfish24_x, jellyfish24_y, c='#770077', label='Jellyfish;24 ports')

    # jellyfish 32 ports
    k = 32
    r = 25
    jellyfish32_x = [0, 80]
    jellyfish32_y = []
    for x in jellyfish32_x:
        jellyfish32_y.append(k / (k - r) * x)
    ax.plot(jellyfish32_x, jellyfish32_y, c='#008800', linewidth=5, label='Jellyfish;32 ports')

    # jellyfish 48 ports
    k = 48
    r = 36
    jellyfish48_x = [0, 80]
    jellyfish48_y = []
    for x in jellyfish48_x:
        jellyfish48_y.append(k / (k - r) * x)
    ax.plot(jellyfish48_x, jellyfish48_y, c='#333399', linestyle=":", label='Jellyfish;48 ports')

    # jellyfish 64 ports
    k = 64
    r = 47
    jellyfish64_x = [0, 80]
    jellyfish64_y = []
    for x in jellyfish64_x:
        jellyfish64_y.append(k / (k - r) * x)
    ax.plot(jellyfish64_x, jellyfish64_y, c='#FF6600', linewidth=5, label='Jellyfish;64 ports')

    # Fat-tree {24,32,48,64} ports
    ports = [24, 32, 48, 64]
    fattree_x = []
    fattree_y = []
    for k in ports:
        fattree_x.append(k ** 3 / 4 / 1000)
        fattree_y.append(k ** 3 * 5 / 4 / 1000)
    ax.scatter(fattree_x, fattree_y, marker='o', c='#CC3333', s=300, label='Fat-tree;{24,32,48,64} ports')

    # arrow "Increasing port-count"
    plt.arrow(70, 350, 0, -150, shape='full', length_includes_head=True, linewidth=5, head_width=1, head_length=15,
              color='black')
    plt.text(60, 170, 'Increasing port-count', fontsize=20)

    plt.legend(loc="upper left", fontsize=20)

    plt.xlabel('Number of Servers in Thousands', fontsize=20)
    plt.ylabel('Equipment Cost [#Ports in Thousands]', fontsize=20)

    ax.axis(xmin=0, xmax=80)
    ax.axis(ymin=0, ymax=400)

    if outfile:
        plt.savefig(outfile)

def plot_equipment_cost_using_res(res, outfile=None):
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.grid(linestyle=':')

    # jellyfish 24 ports
    jellyfish24_x, jellyfish24_y = res['jellyfish24_x'], res['jellyfish24_y']
    ax.plot(jellyfish24_x, jellyfish24_y, c='#770077', label='Jellyfish;24 ports')

    # jellyfish 32 ports
    jellyfish32_x, jellyfish32_y = res['jellyfish32_x'], res['jellyfish32_y']
    ax.plot(jellyfish32_x, jellyfish32_y, c='#008800', linewidth=5, label='Jellyfish;32 ports')

    # jellyfish 48 ports
    jellyfish48_x, jellyfish48_y = res['jellyfish48_x'], res['jellyfish48_y']
    ax.plot(jellyfish48_x, jellyfish48_y, c='#333399', linestyle=":", label='Jellyfish;48 ports')

    # jellyfish 64 ports
    jellyfish64_x, jellyfish64_y = res['jellyfish64_x'], res['jellyfish64_y']
    ax.plot(jellyfish64_x, jellyfish64_y, c='#FF6600', linewidth=5, label='Jellyfish;64 ports')

    # Fat-tree {24,32,48,64} ports
    fattree_x, fattree_y = res['fattree_x'], res['fattree_y']
    ax.scatter(fattree_x, fattree_y, marker='o', c='#CC3333', s=300, label='Fat-tree;{24,32,48,64} ports')

    # arrow "Increasing port-count"
    plt.arrow(70, 350, 0, -150, shape='full', length_includes_head=True, linewidth=5, head_width=1, head_length=15,
              color='black')
    plt.text(60, 170, 'Increasing port-count', fontsize=20)

    plt.legend(loc="upper left", fontsize=20)

    plt.xlabel('Number of Servers in Thousands', fontsize=20)
    plt.ylabel('Equipment Cost [#Ports in Thousands]', fontsize=20)

    ax.axis(xmin=0, xmax=80)
    ax.axis(ymin=0, ymax=400)

    if outfile:
        plt.savefig(outfile)

def plot_distinct_paths(graph, outfile=None):
    hosts_set = []
    switches_set = []
    for n in graph.nodes:
        if "h" in n:
            hosts_set.append(n)
        if 's' in n:
            switches_set.append(n)

    edge_path_stat = {}
    methods = ['k_shortest_paths_8', 'ecmp_paths_8', 'ecmp_paths_64']
    for edge in graph.edges:
        if 'h' in edge[0] or 'h' in edge[1]:
            continue
        edge_path_stat[(edge[0], edge[1])] = {m: 0 for m in methods}
        edge_path_stat[(edge[1], edge[0])] = {m: 0 for m in methods}

    traffic_permutation = random_permutation(len(hosts_set))

    count_paths(graph, traffic_permutation, edge_path_stat)

    method_count_stat = {}
    for m in methods:
        method_count_stat[m] = []
    for _, v in edge_path_stat.items():
        for m in methods:
            method_count_stat[m].append(v[m])

    x = list(range(len(edge_path_stat)))
    for m in methods:
        method_count_stat[m] = sorted(method_count_stat[m])

    # plot
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.grid(linestyle=':')

    ax.plot(x, method_count_stat['k_shortest_paths_8'], label='8 Shortest Paths', c='#333399', linewidth=5)
    ax.plot(x, method_count_stat['ecmp_paths_8'], label='8-way ECMP', c='#00A000')
    ax.plot(x, method_count_stat['ecmp_paths_64'], label='64-way ECMP', c='#CC3333', linestyle=":", linewidth=2)

    ax.axis(xmin=0, xmax=3000)
    ax.axis(ymin=0, ymax=18)

    plt.legend(loc="upper left", fontsize=20)

    plt.xlabel('Rank of Link', fontsize=20)
    plt.ylabel('Distinct Paths Link is on', fontsize=20)

    if outfile:
        plt.savefig(outfile)

def plot_distinct_paths_using_res(res, outfile=None):

    x, method_count_stat = res['x'], res['method_count_stat']

    # plot
    fig, ax = plt.subplots(figsize=(16, 8))
    plt.grid(linestyle=':')

    ax.plot(x, method_count_stat['k_shortest_paths_8'], label='8 Shortest Paths', c='#333399', linewidth=5)
    ax.plot(x, method_count_stat['ecmp_paths_8'], label='8-way ECMP', c='#00A000')
    ax.plot(x, method_count_stat['ecmp_paths_64'], label='64-way ECMP', c='#CC3333', linestyle=":", linewidth=2)

    ax.axis(xmin=0, xmax=3000)
    ax.axis(ymin=0, ymax=18)

    plt.legend(loc="upper left", fontsize=20)

    plt.xlabel('Rank of Link', fontsize=20)
    plt.ylabel('Distinct Paths Link is on', fontsize=20)

    if outfile:
        plt.savefig(outfile)
