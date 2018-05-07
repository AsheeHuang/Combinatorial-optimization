from Flow import *
import networkx as nx
import matplotlib.pyplot as plt
def find_b_flow(G) :

    G.add_nodes_from(['s','t'],e = 0)
    for i in G.node :
        if G.node[i]['e'] > 0 :
            G.add_edge('s',i,u = G.node[i]['e'], f = 0)
            G.node[i]['e'] = 0
        elif G.node[i]['e'] < 0 :
            G.add_edge(i, 't', u=-G.node[i]['e'],f = 0)
            G.node[i]['e'] = 0

    A = nx.maximum_flow(G,'s','t',capacity='u')
    flow = A[1]
    for k in flow :
        for l in flow[k] :
            if flow[k][l] > 0 and k != 's' and k != 't' and l != 's' and l != 't' :
                G[k][l]['f'] += flow[k][l]
                G.add_edge(l,k,f = flow[k][l], u=G[k][l]['u'],c=-G[k][l]['c'],reverse_edge = True)
                if G[k][l]['f'] == G[k][l]['u'] :
                    G.remove_edge(k,l)
    G.remove_nodes_from(['s','t'])
def residual_along_path(G,C) :
    res = []
    for i in range(len(C)-1):
        if G[C[i]][C[i+1]]['reverse_edge'] == True :
            res.append(G[C[i]][C[i+1]]['u'])
        else :
            res.append(G[C[i]][C[i + 1]]['u'] - G[C[i]][C[i+1]]['f'])
    return res
def update_G(G,P,delta) :
    print(P,delta)
    G.node[P[0]]['e'] -= delta
    G.node[P[-1]]['e'] += delta
    for i in range(len(P) - 1):
        G[P[i]][P[i + 1]]['f'] += delta*is_reverse(G[P[i]][P[i+1]])
        if  not G.has_edge(P[i+1],P[i]) :
            G.add_edge(P[i + 1], P[i], f=G[P[i]][P[i + 1]]['f'], u=G[P[i]][P[i + 1]]['u'], c=-G[P[i]][P[i + 1]]['c'])
            G[P[i + 1]][P[i]]['reverse_edge'] = not G[P[i]][P[i + 1]]['reverse_edge']
        else:
            G[P[i+1]][P[i]]['f'] += delta
        if G[P[i]][P[i + 1]]['f'] == G[P[i]][P[i + 1]]['u']:
            G.remove_edge(P[i], P[i + 1])
    return G
def is_reverse(edge):
    if edge['reverse_edge'] == True :
        return -1
    else :
        return 1
if __name__ == "__main__" :
    G = read_data("test.txt")
    # a= nx.min_cost_flow(G,demand = 'balance',capacity='u',weight='c')
    find_b_flow(G)

    while True:
        min_c,C = min_cycle(G)
        if min_c < 0:
            capacity_along_path = residual_along_path(G,C)
            update_G(G,C,min(capacity_along_path))
        else :
            break
    cost_flow = 0
    for edge in G.edges :
        if G[edge[0]][edge[1]]['reverse_edge'] :
            cost_flow += (G[edge[0]][edge[1]]['f'] *- G[edge[0]][edge[1]]['c'] )
    print("Min cost flow : %d" % cost_flow)

    draw_network(G)