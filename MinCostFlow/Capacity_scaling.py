from Flow import *
import networkx as nx
import matplotlib.pyplot as plt
from math import pow,log2,floor
def cal_gamma(e) :
    b_max = max(e.values())
    gamma = pow(2,floor(log2(b_max)))
    return gamma
def select_s(G,gamma) : #select the node which excess flow greater than gamma
    ex = nx.get_node_attributes(G,'e')
    for node in ex :
        if ex[node] >= gamma :
            return  node
    return False
def select_t(G,gamma) : #select the node which excess flow smaller than -gamma
    ex = nx.get_node_attributes(G,'e')
    for node in ex :
        if ex[node] <= gamma :
            return  node
    return False
if __name__ == "__main__" :
    path = "./test200.txt"
    G = read_data(path)
    gamma = cal_gamma(nx.get_node_attributes(G,'e'))
    while all(nx.get_node_attributes(G,'e').values()) ==0 :
    # for _ in range(1) :
        s = select_s(G,gamma)
        t = select_t(G,-gamma)

        if s and t :
            P = nx.shortest_path(G,s,t,weight = 'c')
            cost_along_path = [G[P[i]][P[i + 1]]['u'] - G[P[i]][P[i + 1]]['f'] for i in range(len(P) - 1)]
            delta = min(G.node[s]['e'], -G.node[t]['e'], min(cost_along_path))
            update_G(G,P,delta)
            continue #re-select s,t
        if gamma >= 1 :
            gamma /= 2
        else :
            break
    """-------End of algo----------"""
    cost_flow = 0
    for edge in G.edges:
        if  G[edge[0]][edge[1]]['reverse_edge']:
            cost_flow += (G[edge[0]][edge[1]]['f'] * -G[edge[0]][edge[1]]['c'])
    print("Min cost flow : %d" % cost_flow)

    # draw_network(G,fix = False)