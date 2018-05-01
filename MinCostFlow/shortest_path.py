
import matplotlib.pyplot as plt
from Flow import *
def calED(G) :

    E = []
    D = []
    for i in G.node :
        if G.node[i]['balance'] > 0 :
            E.append(i)
        elif G.node[i]['balance'] < 0 :
            D.append(i)
    return E,D
if __name__ == "__main__" :
    path = './test3.txt'
    G = read_data(path)
    #nx.min_cost_flow(G,demand = 'balance', capacity='u',weight='c')
    """-----------Init----------"""
    E,D = calED(G)
    while E :
        k,l = E[0],D[0]
        P = nx.shortest_path(G,k,l,weight='c')
        cost_along_path = [G[P[i]][P[i+1]]['u'] - G[P[i]][P[i+1]]['f'] for i in range(len(P)-1)]
        delta = min(G.node[k]['e'],-G.node[l]['e'],min(cost_along_path))
        #update
        update_G(G,P,delta)
        if G.node[k]['e'] == 0 :
            E.pop(0)
        if G.node[l]['e'] == 0 :
            D.pop(0)

    cost_flow = 0
    for edge in G.edges :
        if G[edge[0]][edge[1]]['reverse_edge']:
            cost_flow += (G[edge[0]][edge[1]]['f'] * -G[edge[0]][edge[1]]['c'] )
    print("Min cost flow : %d" % cost_flow)
    draw_network(G)
