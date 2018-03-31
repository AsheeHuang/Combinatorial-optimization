from copy import deepcopy
from time import time
global balanced
max_num = 1000000
def read_graph(path) :

    data = open(path, "r")
    lines = data.read().splitlines()
    n = int(lines[0])

    G = {i: {} for i in range(n)}
    G_b = {i:{} for i in range(n)} #graph for backward

    for line in lines[2:]:
        arc = line.split("  ")

        arc[2] = "{:.0f}".format(float(arc[2]))
        v = int(arc[0])
        u = int(arc[1])
        capacity = int(arc[2])
        # print(v,u,capacity)
        try:
            G[u][v]
        except KeyError:
            G[v][u] = capacity
            G_b[u][v] = capacity
    # print(G)
    return G,G_b, n

def residual_graph(G,G_f) :
    residual_G = deepcopy(G)
    for i in range(len(G)) :
        for j in G[i] :
            residual_G[i][j] -= G_f[i][j]
    # print(residual_G)
    return residual_G
def init_G_f(G) :
    G_f = deepcopy(G)
    for i in range(len(G_f)) :
        G_f[i]['inflow'] = 0
        G_f[i]['outflow'] = 0
        for j in G_f[i]:
            G_f[i][j] = 0
    G_f[0]['inflow'] = max_num
    G_f[len(G_f)-1]['outflow'] = max_num
    return G_f
def top_order(G) :
    stack = []
    top = {}
    counter = 1
    count = [0 for i in range(len(G))]

    for i in G :
        for j in G[i] :
            count[j] += 1
    for i in range(len(G)):
        if count[i] == 0:
            stack.append(i)

    top[0] = [0]
    for _ in range(len(G)) :
        changed = False
        top[counter] = []
        if not stack :
            return "error"
        else :
            v = stack.pop()
            for i in G[v] :
                count[i] -= 1
                if count[i] == 0 :
                    changed = True
                    stack.append(i)
                    top[counter].append(i)
        if changed :
            counter += 1
    del top[counter] #delete last one

    return top
def forward_step(G,G_f,top,blocked):
    for layer in top :
        for v in top[layer]:
            for node in G[v]:
                if balanced[node] == False:
                    if G_f[v]['inflow'] > G_f[v]['outflow'] :
                        flow = min(G_f[v]['inflow'] - G_f[v]['outflow'], G[v][node])
                        G_f[v]['outflow'] += flow-G_f[v][node]
                        G_f[node]['inflow'] += flow-G_f[v][node]
                        G_f[v][node] = flow
                    elif blocked[v] != 0 : #balance blocked node
                        for node in G[v] :
                            flow = min(G_f[v]['outflow'] - G_f[v]['inflow'],G[v][node]-G_f[v][node])
                            G_f[v][node] -= flow
                            G_f[v]['outflow'] -= flow
                            G_f[node]['inflow'] -= flow
                        if G_f[v]['inflow'] == G_f[v]['outflow'] :
                            balanced[v] = True
                            break
            if(G_f[v]['inflow'] > G_f[v]['outflow'] and v != 0 and v !=  len(G)-1) :
                blocked[v] = 1 #PF_blocked
    return G_f

def backward_step(G_b,G_f,top,blocked):
    for layer in range(len(top)-1,0,-1) :
        for v in top[layer] :
            for node in G_b[v]:
                if balanced[node] == False :
                    if G_f[v]['inflow'] < G_f[v]['outflow'] :
                            flow = min(G_f[v]['outflow']-G_f[v]['inflow'] , G_b[v][node])
                            G_f[node]['outflow'] += flow-G_f[node][v]
                            G_f[v]['inflow'] += flow-G_f[node][v]
                            G_f[node][v] = flow
                    elif blocked[v] != 0 : #balance blocked node
                        for node in G_b[v] :
                            flow = min(G_f[v]['inflow'] - G_f[v]['outflow'],G_b[v][node]-G_f[node][v])
                            G_f[node][v] -= flow
                            G_f[v]['inflow'] -= flow
                            G_f[node]['outflow'] -= flow
                        if G_f[v]['inflow'] == G_f[v]['outflow'] :
                            balanced[v] = True
                            break
            if (G_f[v]['inflow'] < G_f[v]['outflow'] and v != 0 and v != len(G) - 1):
                blocked[v] = -1  # BF_blocked
    return G_f
if __name__ == "__main__" :
    file = [i*1000 for i in  range(1,11)]

    for v_num in file :
        data_path = "./Data/"+str(v_num)+".txt"
        start = time()
        G,G_b,n = read_graph(data_path) #graph,#graph from backward ,and num of vertices

        G_f = init_G_f(G) #init the flow in G
        top = top_order(G) #get topological order of G
        blocked = [0 for i in range(n)] #0 for unblocked, 1 for PF blocked ,-1 for BF blocked
        balanced = [False] * n #every node is not yet balanced

        for i in range(int(v_num/100)):
        # while any(i == False for i in balanced[1:n-1]): #when every node is balanced, then stop
            G_f = forward_step(G,G_f,top,blocked) #forward step
            G_f = backward_step(G_b,G_f,top,blocked) #backward step

        # for i in G_f :
        #     print(i,G_f[i])

        # for i in range(n) :
            # print(balanced[i],blocked[i])
        print("Number of vertice :" ,v_num)
        print("Time cost : %.8f" % (time() - start))
        print("-------------------------------------------")

