from Flow import *
import matplotlib.pyplot as plt
import networkx as nx
from random import randint
from copy import deepcopy
def set_potential(G,value = 0) :

    for node in G.nodes :
        G.nodes[node]['potential'] = value
def draw_network(G) :
    """----------Draw network-----"""
    pos = {1: ([0, 2]), 2: ([0, 0]), 3: ([1, 0.8]),
            4: ([2, 2]), 5: ([2, 0]), 's' :([-1,1]), 't' : ([3,1])}
    # pos = {1: ([0, 2]), 2: ([0, 0]), 3: ([1, 0.8]),4: ([2, 2]), 5: ([2, 0])}
    # pos = nx.spring_layout(G, scale=100) #no fix
    # nx.draw_networkx(G, pos, with_labels=True)

    node_labels = nx.get_node_attributes(G, name='potential')
    nx.draw_networkx_nodes(G, pos, label=node_labels)
    nx.draw_networkx_labels(G, pos, label=node_labels)
    for edge in G.edges:
        start, end = edge[0], edge[1]
        G[start][end]['f_u_c'] = [None for i in range(3)]
        G[start][end]['f_u_c'][0] = int(G[start][end]['f'])
        G[start][end]['f_u_c'][1] = G[start][end]['u']
        G[start][end]['f_u_c'][2] = G[start][end]['c']

    R, F = classify_reverse(G)
    nx.draw_networkx_edges(G, pos, R, edge_color='blue', style='dashed')
    nx.draw_networkx_edges(G, pos, F, alpha=0.5, width=2)
    edge_labels = nx.get_edge_attributes(G, 'f_u_c')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
def cal_outofkilter(G) :
    out_of_kilter = []
    for edge in G.edges :
        i,j = edge[0], edge[1]
        if G[i][j]['reverse_edge'] == False :
            if G[i][j]['f'] == 0 and G[i][j]['reduce_cost'] < 0 :
                out_of_kilter.append((i,j))
            elif 0< G[i][j]['f'] < G[i][j]['u'] and G[i][j]['reduce_cost'] != 0:
                out_of_kilter.append((i,j))
            elif G[i][j]['f'] == G[i][j]['u'] and G[i][j]['reduce_cost'] > 0:
                out_of_kilter.append((i,j))
    return out_of_kilter
def G_without_pq(G,p,q) :
    Gn = deepcopy(G)
    if Gn.has_edge(q,p) :
        Gn.remove_edge(q,p)
    return Gn
def cal_dist(Gn,q,p) :
    for edge in G.edges :
        i,j = edge[0],edge[1]
        G[i][j]['length'] = max (G[i][j]['reduce_cost'],0)
    length, path = nx.single_source_bellman_ford(G, q, weight='length')
    for i in length:
        G.node[i]['potential'] = G.node[i]['potential'] - length[i]

    return path[p]
def residual_along_path(G,C) :
    res = []
    for i in range(len(C)-1):
        if G[C[i]][C[i+1]]['reverse_edge'] == True :
            res.append(G[C[i]][C[i+1]]['u'])
        else :
            res.append(G[C[i]][C[i + 1]]['u'] - G[C[i]][C[i+1]]['f'])
    return res
if __name__ == '__main__' :
    path = './test200.txt'
    G = read_data(path)
    add_s_t(G)
    set_potential(G)
    f, max_flow = nx.maximum_flow(G, 's', 't', capacity='u')
    update_Gx(G, max_flow)
    cal_reduce_cost(G)
    kilter = cal_outofkilter(G)
    while kilter :
        arc = kilter.pop(randint(0,len(kilter)-1))
        p,q = arc[0], arc[1]
        Gn = G_without_pq(G,p,q)
        path = cal_dist(Gn,q,p)

        if G[p][q]['reduce_cost'] < 0 :
            path.append(q)
            r_along_path = residual_along_path(G,path)
            update_G(G,path,min(r_along_path))
        cal_reduce_cost(G)
        kilter = cal_outofkilter(G)


    """-------End of algo----------"""
    G.remove_nodes_from(['s','t'])
    cost_flow = 0
    for edge in G.edges:
        if G[edge[0]][edge[1]]['reverse_edge']:
            cost_flow += (G[edge[0]][edge[1]]['f'] * -G[edge[0]][edge[1]]['c'])
    print("Min cost flow : %d" % cost_flow)



    draw_network(G)