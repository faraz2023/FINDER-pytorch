import networkx as nx
import numpy as np
import random
import os

data_path = os.path.join("..", "..", "data", 'real')
#data_name = ['ba_space_100']
data_name = ['modified-morPOP-NL-day20.txt']
save_dir = os.path.join("..", "..", "data", 'real', 'cost')


cost_type = 'degree'

for i in range(len(data_name)):
    data = os.path.join(data_path , data_name[i])
    g = nx.read_edgelist(data)

    nodes = g.nodes()
    nodes_l = list(nodes)
    nodes_l_map = map(int, nodes_l)
    nodes_l_int = list(nodes_l_map)
    nodes_l_int.sort()

    nodes_l_map = map(str, nodes_l_int)
    nodes_l = list(nodes_l_map)

    new_node_labels = {}
    for k in range(len(nodes_l)):
        new_node_labels[nodes_l[k]] = str(k)

    g = nx.relabel_nodes(g, new_node_labels)

    ### degree weight
    if cost_type == 'degree':
        degree = nx.degree(g)
        maxDegree = max(dict(degree).values())
        weights = {}
        for node in g.nodes():
            weights[node] = degree[node] / maxDegree

    elif cost_type == 'degree_noise':
        degree = nx.degree(g)
        median_val = np.median(list(dict(degree).values()))
        weights = {}
        for node in g.nodes():
            episilon = 0.5 * median_val * np.random.normal(0, 1)
            weights[node] = 0.5 * degree[node] + episilon
            if weights[node] < 0.0:
                weights[node] = - weights[node]
        max_weight = np.max(list(weights.values()))
        for node in g.nodes():
            weights[node] = weights[node] / max_weight

    elif cost_type == 'random':
    # ### random weight
        weights = {}
        for node in g.nodes():
            weights[node] = random.uniform(0, 1)

    nx.set_node_attributes(g, weights, 'weight')
    save_dir_g = '%s/%s_%s.gml' % (save_dir, data_name[i], cost_type)
    nx.write_gml(g, save_dir_g)


    f_weight = open(os.path.join(save_dir, '%s_%s_weight.txt'%(data_name[i], cost_type)), 'w')
    for j in range(nx.number_of_nodes(g)):
        f_weight.write('%.8f\n'%weights[str(j)])
        f_weight.flush()
    f_weight.close()

    print ('Data %s is finished!'%data_name[i])
