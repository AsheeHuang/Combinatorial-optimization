from copy import deepcopy

def read_graph() :

    G = {0:{1:10,2:10},
         1:{2:2,3:4,4:8},
         2:{4:9},
         3:{5:10},
         4:{3:6,5:10},
         5:{}}

    return G,len(G),9

def residule_graph(G,G_f) :
    residule_G = deepcopy(G)
    for i in range(len(G)) :
        for j in G[i] :
            residule_G[i][j] -= G_f[i][j]
    # print(residule_G)
    return residule_G


def get_level_graph (G,G_f) :
    #using BFS to get level graph
    G_r = residule_graph(G,G_f)

    visited = [False]*n
    level = [0] * n
    level_graph = {key : {} for key in range(n)}
    queue = [0]

    while queue :
        v = queue.pop(0) #deque
        for i in G_r[v] :
            index, flow= i,G_r[v][i]
            if flow != 0 and visited[index] == False :
                queue.append(index)
                visited[index] = True
                level[index] = level[v] + 1
        for i in G_r[v]:
            index, flow = i, G_r[v][i]
            if level[index] > level[v] :
                level_graph[v][index] = flow
    # print(level_graph)
    return level_graph

def find_path(level_graph, source) :
    v = source #start from source
    min_flow = float('inf') #big number
    path = [source]
    while v != n-1 and level_graph[v]:
        # print(level_graph.keys(level_graph.values()),)
        # print(level_graph.items())
        # print(list(level_graph.keys())[0])
        next_v,flow = list(level_graph[v].keys())[0],list(level_graph[v].values())[0]
        path.append(next_v)
        v = next_v
        if flow < min_flow :
            min_flow = flow

    return path,min_flow if v == n-1 else False
def update_graph(level_graph,G_f,aug_path,min_flow) :
    for i in range(len(aug_path)-1) :
        v = aug_path[i]
        j = aug_path[i+1]

        level_graph[v][j] -= min_flow
        G_f[v][j] += min_flow
        if level_graph[v][j] == 0 :
            del level_graph[v][j]

    return level_graph



if __name__ == "__main__" :
    G,n,m = read_graph() #graph, # of vertices , # of edges
    G_f = deepcopy(G)

    for i in range(len(G_f)) :
        for j in G_f[i]:
            G_f[i][j] = 0

    total_flow = 0
    for _ in range(m) :
        level_graph= get_level_graph(G,G_f)
        while 1 :
            aug_path,min_flow = find_path(level_graph,0)
            total_flow += min_flow
            level_graph = update_graph(level_graph,G_f,aug_path,min_flow)
            if min_flow == False :  #blocking flow
                break
    print("Max Flow : ",total_flow)



