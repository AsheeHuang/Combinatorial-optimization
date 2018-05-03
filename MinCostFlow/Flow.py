import networkx as nx
import matplotlib.pyplot as plt
def read_data(path) :
    f = open(path,'r')
    n = int(f.readline())
    m = int(f.readline())
    G = nx.DiGraph()
    lines = f.read().splitlines()
    for i in range(n) :
        lines[i] = lines[i].split(' ')
        n,b = int(lines[i][0]),int(lines[i][1])
        G.add_node(n,balance= b,e = b)
    for i in range(n,n+m) :
        lines[i] = lines[i].split(' ')
        start,end,u,c = int(lines[i][0]), int(lines[i][1]),int(lines[i][2]),int(lines[i][3])
        G.add_edge(start,end,f = 0,u = u,c = c,r = u,reverse_edge = False)
    return G
# def update_G(G,P,delta) :
#     print(P,delta)
#     G.node[P[0]]['e'] -= delta
#     G.node[P[-1]]['e'] += delta
#     for i in range(len(P) - 1):
#         G[P[i]][P[i + 1]]['f'] += delta
#         if  not G.has_edge(P[i+1],P[i]) :
#             G.add_edge(P[i + 1], P[i], f=G[P[i]][P[i + 1]]['f'], u=G[P[i]][P[i + 1]]['u'], c=-G[P[i]][P[i + 1]]['c'])
#             G[P[i + 1]][P[i]]['reverse_edge'] = not G[P[i]][P[i + 1]]['reverse_edge']
#         else:
#             G[P[i+1]][P[i]]['f'] += delta
#         if G[P[i]][P[i + 1]]['f'] == G[P[i]][P[i + 1]]['u']:
#             G.remove_edge(P[i], P[i + 1])
#     return G
def update_G(G,P,delta) :
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
def classify_reverse(G) :
    R = []
    F = []
    for edge in G.edges :
        if G[edge[0]][edge[1]]['reverse_edge'] == True :
            R.append(edge)
        else :
            F.append(edge)

    return R,F
def min_cycle(G) :
    cycles = nx.simple_cycles(G)

    min = 999999999
    min_path = []
    for cycle in cycles :
        cycle.append(cycle[0])
        weights = nx.get_edge_attributes(G,'c')
        sumw = sum([weights[(cycle[i - 1], cycle[i])] for i in range(1, len(cycle))])
        if sumw < min :
            min = sumw
            min_path = cycle
    return min,min_path
def draw_network(G) :
    """----------Draw network-----"""
    # pos = {1: ([0, 2]), 2: ([0, 0]), 3: ([1, 0.8]),
    #        4: ([2, 2]), 5: ([2, 0])}

    pos = nx.spring_layout(G, scale=100) #no fix
    # nx.draw_networkx(G, pos, with_labels=True)
    nx.draw_networkx_nodes(G, pos)
    # node_labels = nx.get_node_attributes(G, 'balance')
    nx.draw_networkx_labels(G, pos)
    for edge in G.edges:
        start, end = edge[0], edge[1]
        G[start][end]['f_u_c'] = [None for i in range(3)]
        G[start][end]['f_u_c'][0] = int(G[start][end]['f'])
        G[start][end]['f_u_c'][1] = G[start][end]['u']
        G[start][end]['f_u_c'][2] = G[start][end]['c']

    R, F = classify_reverse(G)
    nx.draw_networkx_edges(G, pos, R, edge_color='blue', style='dashed')
    nx.draw_networkx_edges(G, pos, F, edge_color='black', alpha=0.5, width=4)
    edge_labels = nx.get_edge_attributes(G, 'f_u_c')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()

