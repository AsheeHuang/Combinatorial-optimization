from Flow import *
import networkx as nx
from random import randint
from math import floor,log2
def max_cost(cost) :
    C = max(cost.values())
    gamma = pow(2, floor(log2(C)))
    return gamma
def improve_approximation(G,epsilon) :
    edges = tuple(G.edges())
    cal_reduce_cost(G)
    for edge in edges :
        i,j = edge[0],edge[1]
        if G[i][j]['f'] > 0 :
            if G[i][j]['reverse_edge'] == False :
                if G[i][j]['reduce_cost'] > 0 :
                    flow = G[i][j]['f']
                    update_G(G,[i,j],-flow)
                elif G[i][j]['reduce_cost'] <= 0 :
                    flow = G[i][j]['u'] - G[i][j]['f']
                    update_G(G,[i,j],flow)


            # elif G[i][j]['reverse_edge'] == True :
            #     if G[i][j]['reduce_cost'] > 0 :
            #         flow = G[i][j]['f']
            #         update_G(G,[i,j],flow)
            #     elif G[i][j]['reduce_cost'] <= 0 :
            #         flow = G[i][j]['u'] - G[i][j]['f']
            #         # update_G(G, [i, j], -flow)
            #         G[i][j]['f'] += flow
            #         G.node[i]['e'] -= flow
            #         G.node[j]['e'] += flow

    active = get_active_node(G)
    while active :
        # print(active)
        # draw_network(G)
        active_node = active.pop(randint(0,len(active)-1))
        push_relabel(G,active_node,epsilon)


def get_active_node(G) :

    active = []
    for node in G.nodes :
        if G.nodes[node]['e'] > 0  :
            active.append(node)
    return active
def push_relabel(G,node,epsilon) :

    ad_node = has_admisssible(G,node,epsilon)

    if ad_node :
        j = ad_node[randint(0,len(ad_node)-1)]
        flow = min(G.nodes[node]['e'],G[node][j]['u'] - G[node][j]['f'] )

        update_G(G,[node,j],flow)
    else :
        G.nodes[node]['potential'] += epsilon/2
        cal_reduce_cost(G)
def has_admisssible(G,node,epsilon) :
    cal_reduce_cost(G)
    ad_node = []
    for edge in G.edges(node) :
        i,j = edge[0], edge[1]
        if -epsilon <= G[i][j]['reduce_cost'] <= 0 :
            ad_node.append(j)
    if ad_node :
        return ad_node
    return False


if __name__ == "__main__" :
    path = './test200.txt'
    G = read_data(path)
    set_potential(G,value=0)

    epsilon = max_cost(nx.get_edge_attributes(G,name='c'))
    add_s_t(G)
    f, max_flow = nx.maximum_flow(G, 's', 't', capacity='u')
    update_Gx(G, max_flow)

    G.remove_nodes_from(['s','t'])
    cal_reduce_cost(G)


    while epsilon >= 1/G.number_of_nodes() :
        improve_approximation(G,epsilon)
        # draw_network(G)
        epsilon = epsilon / 2
        # break
    """-------End of algo----------"""
    cost_flow = 0
    for edge in G.edges:
        if G[edge[0]][edge[1]]['reverse_edge']:
            cost_flow += (G[edge[0]][edge[1]]['f'] * -G[edge[0]][edge[1]]['c'])
    print("Min cost flow : %d" % cost_flow)
    # draw_network(G)