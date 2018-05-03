from Flow import *
import networkx as nx
from copy import deepcopy
def add_s_t(G) :
    G.add_nodes_from(['s','t'],e = 0)
    ex = 0
    for i in G.node :
        if G.node[i]['e'] > 0 :
            G.add_edge('s',i,u = G.node[i]['e'], f = 0,c = 0,reverse_edge = False)
            # G.node['s']['e'] += G.node[i]['e']
            ex += G.node[i]['e']
            G.node[i]['e'] = 0
        elif G.node[i]['e'] < 0 :
            G.add_edge(i, 't', u=-G.node[i]['e'],f = 0,c = 0,reverse_edge = False)
            # G.node['t']['e'] -= G.node[i]['e']
            G.node[i]['e'] = 0
    return ex
def cal_potential(G) :
    length,path = nx.single_source_bellman_ford(G,'s',weight='c')

    for i in length :
        G.node[i]['potential'] = length[i]
def cal_reduce_cost(G) :
    for edge in G.edges :
        i,j = edge[0],edge[1]
        G[i][j]['reduce_cost'] = G[i][j]['c'] + G.node[i]['potential'] - G.node[j]['potential']
def admissible_network(G) :
    ad_G = deepcopy(G)
    edge_remove = []
    for edge in ad_G.edges :
        i,j = edge[0], edge[1]
        if ad_G[i][j]['reduce_cost'] in ad_G[i][j] and ad_G[i][j]['reduce_cost'] != 0 :
            edge_remove.append((i,j))
    ad_G.remove_edges_from(edge_remove)
    return ad_G
def update_Gx(G,max_flow) :
    delete = []
    for i in max_flow :
        for j in max_flow[i] :
            if max_flow[i][j] == 0 :
                delete.append((i,j))
    for i,j in delete :
        del max_flow[i][j]
    #find flow
    while any(max_flow['s'].values()) != 0 :
        cur_node = 's'
        path = ['s']
        while cur_node != 't' :
            print(cur_node,max_flow[cur_node])
            next = list(max_flow[cur_node].keys())[0]
            path.append(next)
            if cur_node == next :
                return
            cur_node = next

        flow_along_path = [max_flow[path[i]][path[i+1]] for i in range(len(path)-1)]
        bottleneck = min(flow_along_path)
        update_G(G,path,bottleneck) #augment bottleneck flow
        print(path)
        for i in range(len(path)-1) :
            max_flow[path[i]][path[i+1]] -= bottleneck
            if max_flow[path[i]][path[i+1]] == 0 :
                del max_flow[path[i]][path[i+1]]
            # if not max_flow[path[i]] :
            #     del max_flow[path[i]]
def cal_potential_d(G) :
    length,path = nx.single_source_dijkstra(G,'s',weight='reduce_cost')
    for i in length :
        G.node[i]['potential'] = G.node[i]['potential'] + length[i]
def draw_network(G) :
    """----------Draw network-----"""
    # pos = {1: ([0, 2]), 2: ([0, 0]), 3: ([2, 2]),
    #        4: ([2, 0]), 's': ([-1, 1]),'t' : ([3, 1]) ,'5': ([3,1])}

    pos = nx.spring_layout(G, scale=100) #no fix
    # nx.draw_networkx(G, pos, with_labels=True)

    node_labels = nx.get_node_attributes(G, 'potential')
    nx.draw_networkx_nodes(G, pos, label=node_labels)
    nx.draw_networkx_labels(G, pos, labels=node_labels)
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
    path = './test.txt'
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

        excess += f
        if excess == total_exflow :
            break
    """-------End of algo----------"""

    cost_flow = 0
    for edge in G.edges:
        if G[edge[0]][edge[1]]['reverse_edge']:
            cost_flow += (G[edge[0]][edge[1]]['f'] * -G[edge[0]][edge[1]]['c'])
    print("Min cost flow : %d" % cost_flow)
    G.remove_edges_from(['s','t'])
    draw_network(G)


