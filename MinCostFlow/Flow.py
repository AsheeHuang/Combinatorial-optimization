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
        G.add_edge(start,end,f = 0,u = u,c = c,reverse_edge = False)
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
def cal_reduce_cost(G) :
    for edge in G.edges :
        i,j = edge[0],edge[1]
        if G[i][j]['reverse_edge'] == False :
            G[i][j]['reduce_cost'] = G[i][j]['c'] - G.node[i]['potential'] + G.node[j]['potential']
        else :
            G[i][j]['reduce_cost'] = -G[i][j]['c'] + G.node[i]['potential'] - G.node[j]['potential']
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
            next = list(max_flow[cur_node].keys())[0]
            path.append(next)
            if cur_node == next :
                return
            cur_node = next

        flow_along_path = [max_flow[path[i]][path[i+1]] for i in range(len(path)-1)]
        bottleneck = min(flow_along_path)
        update_G(G,path,bottleneck) #augment bottleneck flow
        for i in range(len(path)-1) :
            max_flow[path[i]][path[i+1]] -= bottleneck
            if max_flow[path[i]][path[i+1]] == 0 :
                del max_flow[path[i]][path[i+1]]
            # if not max_flow[path[i]] :
            #     del max_flow[path[i]]
def set_potential(G,value = 0) :

    for node in G.nodes :
        G.nodes[node]['potential'] = value
def draw_network(G,fix = True) :
    """----------Draw network-----"""
    pos = {1: ([0, 2]), 2: ([0, 0]), 3: ([1, 0.8]),
            4: ([2, 2]), 5: ([2, 0]), 's' :([-1,1]), 't' : ([3,1])}
    if fix == False :
        pos = nx.spring_layout(G, scale=100) #no fix
    # nx.draw_networkx(G, pos, with_labels=True)
    nx.draw_networkx_nodes(G, pos)
    node_labels = nx.get_node_attributes(G, 'e')
    nx.draw_networkx_labels(G, pos,labels=node_labels)
    cal_reduce_cost(G)
    for edge in G.edges:
        start, end = edge[0], edge[1]
        G[start][end]['f_u_c'] = [None for i in range(4)]
        G[start][end]['f_u_c'][0] = int(G[start][end]['f'])
        G[start][end]['f_u_c'][1] = G[start][end]['u']
        G[start][end]['f_u_c'][2] = G[start][end]['c']
        G[start][end]['f_u_c'][3] = G[start][end]['reduce_cost']

    R, F = classify_reverse(G)
    nx.draw_networkx_edges(G, pos, R, edge_color='blue', style='dashed')
    nx.draw_networkx_edges(G, pos, F, edge_color='black', alpha=0.5, width=4)
    edge_labels = nx.get_edge_attributes(G, 'f_u_c')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()