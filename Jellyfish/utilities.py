import networkx as nx
import random
import numpy as np
from itertools import islice

def str_gt(s1, s2):
    num1 = int(s1.lstrip('s'))
    num2 = int(s2.lstrip('s'))
    return num1 > num2

# Path length distribution
def path_length_stat(graph, return_percentage=True):
    host_set = list()
    other_set = list()
    for k, v in graph.nodes.data():
        if v['type'] == 'host':
            host_set.append(k)
        else:
            other_set.append(k)
    stat = {}
    for h in host_set:
        p = nx.single_source_shortest_path_length(graph, h)
        for node in other_set:
            p.pop(node)
        for _, v in p.items():
            if v not in stat:
                stat[v] = 0
            stat[v] += 1
    if 0 in stat:
        stat.pop(0)

    if return_percentage:
        s = 0
        for _, v in stat.items():
            s += v
        for k, v in stat.items():
            stat[k] = v / s
    return stat


def path_length_stat_10_means(build_graph, **kwargs):
    stat = {}
    for _ in range(10):
        graph = build_graph(**kwargs)
        one_graph_stat = path_length_stat(graph, return_percentage=False)
        for k, v in one_graph_stat.items():
            if k not in stat:
                stat[k] = 0
            stat[k] += v

    s = 0
    for _, v in stat.items():
        s += v
    for k, v in stat.items():
        stat[k] = v / s
    return stat

def normalized_bisection_bw(bisection_bw, line_rate_in_1_part):
    return bisection_bw / line_rate_in_1_part

def fattree_normalized_bisection_bw(N, k):
    num_edges = k ** 3 / 8
    num_hosts = k ** 3 / 4
    normalized_bi_bw = normalized_bisection_bw(num_edges, num_hosts / 2)
    return num_hosts, normalized_bi_bw

def jellyfish_normalized_bisection_bw(N, k, r):
    num_edges = N * (r / 4 - np.sqrt(r * np.log(2)) / 2)
    num_hosts = N * (k - r)
    normalized_bi_bw = normalized_bisection_bw(num_edges, num_hosts / 2)
    return num_hosts, normalized_bi_bw

def generateBisectionBandWidthDataForFigure2a():

    # Fat-tree N=720, k=24
    fattree24_x, fattree24_y = fattree_normalized_bisection_bw(N=720, k=24)
    fattree24_x /= 1000

    # Fat-tree N=1280, k=32
    fattree32_x, fattree32_y = fattree_normalized_bisection_bw(N=1280, k=32)
    fattree32_x /= 1000

    # Fat-tree N=2880, k=48
    fattree48_x, fattree48_y = fattree_normalized_bisection_bw(N=2880, k=48)
    fattree48_x /= 1000

    # Jellyfish N=720, k=24
    jellyfish24_x = []
    jellyfish24_y = []
    for r in range(10, 22):  # obtain r from figure 2 (a). r ranges from [11, 20]
        x, y = jellyfish_normalized_bisection_bw(720, 24, r)
        jellyfish24_x.append(x / 1000)
        jellyfish24_y.append(y)

    # Jellyfish N=1280, k=32
    jellyfish32_x = []
    jellyfish32_y = []
    for r in range(13, 28):  # obtain r from figure 2 (a). r ranges from [14,26]
        x, y = jellyfish_normalized_bisection_bw(1280, 32, r)
        jellyfish32_x.append(x / 1000)
        jellyfish32_y.append(y)

    # Jellyfish N=2880, k=48
    jellyfish48_x = []
    jellyfish48_y = []
    for r in range(20, 41):  # obtain r from figure 2 (a). r ranges from [21, 39]
        x, y = jellyfish_normalized_bisection_bw(2880, 48, r)
        jellyfish48_x.append(x / 1000)
        jellyfish48_y.append(y)

    res = {
        'fattree24_x': fattree24_x,
        'fattree24_y': fattree24_y,
        'fattree32_x': fattree32_x,
        'fattree32_y': fattree32_y,
        'fattree48_x': fattree48_x,
        'fattree48_y': fattree48_y,
        'jellyfish24_x': jellyfish24_x,
        'jellyfish24_y': jellyfish24_y,
        'jellyfish32_x': jellyfish32_x,
        'jellyfish32_y': jellyfish32_y,
        'jellyfish48_x': jellyfish48_x,
        'jellyfish48_y': jellyfish48_y
    }

    return res

def generateEquipmentCostDataForFigure2b():

    # jellyfish 24 ports
    k, r = 24, 19
    jellyfish24_x, jellyfish24_y = [0, 80], []
    for x in jellyfish24_x:
        jellyfish24_y.append(k / (k - r) * x)

    # jellyfish 32 ports
    k, r = 32, 25
    jellyfish32_x, jellyfish32_y = [0, 80], []
    for x in jellyfish32_x:
        jellyfish32_y.append(k / (k - r) * x)

    # jellyfish 48 ports
    k, r = 48, 36
    jellyfish48_x, jellyfish48_y = [0, 80], []
    for x in jellyfish48_x:
        jellyfish48_y.append(k / (k - r) * x)

    # jellyfish 64 ports
    k, r = 64, 47
    jellyfish64_x, jellyfish64_y = [0, 80], []
    for x in jellyfish64_x:
        jellyfish64_y.append(k / (k - r) * x)

    # Fat-tree {24,32,48,64} ports
    ports = [24, 32, 48, 64]
    fattree_x, fattree_y = [], []
    for k in ports:
        fattree_x.append(k ** 3 / 4 / 1000)
        fattree_y.append(k ** 3 * 5 / 4 / 1000)

    res = {
        'jellyfish24_x': jellyfish24_x,
        'jellyfish24_y': jellyfish24_y,
        'jellyfish32_x': jellyfish32_x,
        'jellyfish32_y': jellyfish32_y,
        'jellyfish48_x': jellyfish48_x,
        'jellyfish48_y': jellyfish48_y,
        'jellyfish64_x': jellyfish64_x,
        'jellyfish64_y': jellyfish64_y,
        'fattree_x': fattree_x,
        'fattree_y': fattree_y
    }

    return res

def generateDistinctPathDataForFigure9(graph):
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

    res = {'x': x, 'method_count_stat': method_count_stat}
    return res

def random_permutation(num):
    while True:
        p = list(range(num))
        random.shuffle(p)
        for i in range(num):
            if p[i] == i:
                break
        else:
            return tuple(p)


def ecmp_paths(paths, n):
    paths = list(paths)
    for i in range(n - 1):
        if i == len(paths) - 1:
            return paths
        if len(paths[i]) != len(paths[i + 1]):
            return paths[:i + 1]
    return paths[:n]

def add_distinct_paths_count(graph, stat, paths, method):
    for path in paths:
        for i in range(1, len(path) - 1):
            if 'h' in path[i] or 'h' in path[i + 1]:
                raise RuntimerError('found hosts')
            stat[(path[i], path[i + 1])][method] += 1

def count_paths(graph, traffic, stat):
    for depart, dest in enumerate(traffic):
        depart = f'h{depart}'
        dest = f'h{dest}'
        #         print(depart, dest)
        paths = list(islice(nx.shortest_simple_paths(graph, depart, dest), 64))
        k_shortest_paths_8 = [p[1: -1] for p in paths[:8]]
        ecmp_paths_8 = [p[1: -1] for p in ecmp_paths(paths, 8)]
        ecmp_paths_64 = [p[1:-1] for p in ecmp_paths(paths, 64)]

        add_distinct_paths_count(graph, stat, k_shortest_paths_8, 'k_shortest_paths_8')
        add_distinct_paths_count(graph, stat, ecmp_paths_8, 'ecmp_paths_8')
        add_distinct_paths_count(graph, stat, ecmp_paths_64, 'ecmp_paths_64')

