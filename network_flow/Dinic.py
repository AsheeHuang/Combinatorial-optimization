from copy import deepcopy

def read_graph(path) :
    # #
    # G = {0:{1:10,2:10},
    #      1:{2:2,3:4,4:8},
    #      2:{4:9},
    #      3:{5:10},
    #      4:{3:6,5:10},
    #      5:{}}
    #
    # return G,len(G)
    data = open(path,"r")
    lines = data.read().splitlines()
    n = int(lines[0])
    m = int(lines[1])
    G = {i:{} for i in range(n)}

    for line in lines[2:] :
        arc = line.split("  ")

        arc[2] = "{:.0f}".format(float(arc[2]))
        v = int(arc[0])
        u = int(arc[1])
        capacity = int(arc[2])
        # print(v,u,capacity)
        try :
            G[u][v]
        except KeyError :
            G[v][u] = capacity
    # print(G)
    return G,n

def residual_graph(G,G_f) :
    residule_G = deepcopy(G)
    for i in range(len(G)) :
        for j in G[i] :
            residule_G[i][j] -= G_f[i][j]
    # print(residule_G)
    return residule_G


def get_level_graph (G,G_f) :
    #using BFS to get level graph
    G_r = residual_graph(G,G_f)
    n = len(G)
    visited = [False]*n
    level = [0] * n
    level_graph = {}
    queue = [0]
    connect = [[] for _ in range(n)]
    while queue :
        v = queue.pop(0) #deque
        for i in G_r[v] :
            index, flow= i,G_r[v][i]
            if flow != 0 and visited[index] == False :
                queue.append(index)
                visited[index] = True
                level[index] = level[v] + 1
        if v == n - 1:
            try :
                del level_graph[level[v]+1]
            except KeyError :
                pass
            break
        for i in G_r[v]:
            index, flow = i, G_r[v][i]
            if level[index] > level[v] :
                try :
                    level_graph[level[v]+1][index] = flow
                except KeyError :
                    level_graph[level[v]+1] = {index:flow}
                connect[v].append(index)

    return level_graph,connect

def find_path(level_graph ,connect, source=0) :

    path = []

    stack = [(source,[source])]
    visited = set()
    while stack :
        (vertex,path) = stack.pop()
        if vertex not in visited :
            if vertex == n-1 :
                return path
            for i in connect[vertex] :
                stack.append((i,path+[i]))
    return path
def find_min_flow(path) :
    min_flow = float('inf') #big number
    if path[len(path) - 1] == n - 1  :
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            flow = G[u][v] - G_f[u][v]
            if flow < min_flow :
                min_flow = flow
        return  min_flow
    else :
        return False
def update_graph(level_graph, G_f, aug_path, min_flow, connect):
    for i in range(1,len(aug_path)):
        v = aug_path[i-1]
        j = aug_path[i]

        G_f[v][j] += min_flow
        if G_f[v][j] ==  G[v][j]:
            # del level_graph[i][j]
            connect[v].remove(j)

    return level_graph


if __name__ == "__main__":
    # read_graph("./Data/elist1440.txt")
    G, n = read_graph("./Data/karzanov_example2.txt")  # graph, # of vertices , # of edges
    G_f = deepcopy(G)

    for i in range(len(G_f)):
        for j in G_f[i]:
            G_f[i][j] = 0

    total_flow = 0
    prev_flow = 0
    while 1 :
        level_graph,connect= get_level_graph(G,G_f)
        for i in level_graph :
            print(i,level_graph[i])
        prev_flow = total_flow
        while 1 :
            aug_path = find_path(level_graph,connect)
            min_flow = find_min_flow(aug_path)
            print(aug_path,min_flow)
            total_flow += min_flow
            if min_flow == False :  #blocking flow
                break
            level_graph = update_graph(level_graph,G_f,aug_path,min_flow,connect)

        if prev_flow == total_flow :
            break

    print("Max Flow : ",total_flow)



