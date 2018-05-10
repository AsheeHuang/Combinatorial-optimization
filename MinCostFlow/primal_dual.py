from Flow import *
import networkx as nx
from copy import deepcopy

def cal_potential(G) :
    length,path = nx.single_source_bellman_ford(G,'s',weight='c')

    for i in length :
        G.node[i]['potential'] = length[i]

def admissible_network(G) :
    ad_G = deepcopy(G)
    edge_remove = []
    for edge in ad_G.edges :
        i,j = edge[0], edge[1]
        if ad_G[i][j]['reduce_cost'] in ad_G[i][j] and ad_G[i][j]['reduce_cost'] != 0 :
            edge_remove.append((i,j))
    ad_G.remove_edges_from(edge_remove)
    return ad_G

def cal_potential_d(G) :
    length,path = nx.single_source_dijkstra(G,'s',weight='reduce_cost')
    for i in length :
        G.node[i]['potential'] = G.node[i]['potential'] - length[i]
def draw_network(G) :
    """----------Draw network-----"""
    pos = {1: ([0, 2]), 2: ([0, 0]), 3: ([2, 2]),
           4: ([2, 0]), 's': ([-1, 1]),'t' : ([3, 1]) ,5: ([3,1])}
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
if __name__ == "__main__" :
    path = './test200.txt'
    G = read_data(path)
    total_exflow = add_s_t(G)
    excess = 0

    cal_potential(G)
    cal_reduce_cost(G)
    repeat = True
    while repeat :
        cal_potential_d(G)
        cal_reduce_cost(G)
        ad_G = admissible_network(G)
        f,max_flow = nx.maximum_flow(ad_G,'s','t',capacity = 'u')
        update_Gx(G,max_flow)
        print(f)
        excess += f
        if excess == total_exflow :
            repeat = False
    """-------End of algo----------"""
    G.remove_nodes_from(['s','t'])
    cost_flow = 0
    for edge in G.edges:
        if G[edge[0]][edge[1]]['reverse_edge']:
            cost_flow += (G[edge[0]][edge[1]]['f'] * -G[edge[0]][edge[1]]['c'])
    print("Min cost flow : %d" % cost_flow)

    # draw_network(G)


