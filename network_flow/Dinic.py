from copy import deepcopy
def read_graph() :
    # G = [[0,10,10,0,0,0], #s
    #      [0,0,2,4,8,0],   #1
    #      [0,0,0,0,9,0],   #2
    #      [0,0,0,0,0,10],  #3
    #      [0,0,0,6,0,10],  #4
    #      [0,0,0,0,0,0]]   #t
    G = [[[1,10],[2,10]],     #0
         [[2,2],[3,4],[4,8]], #1
         [[4,9]],             #2
         [[5,10]],            #3
         [[3,6],[5,10]],      #4
         []]                  #5

    return G,len(G),9

def residule_graph(G,G_f) :
    residule_G = list(G)
    for i in range(len(G)) :
        for j in range(len(G[i])) :
            residule_G[i][j][1] -= G_f[i][j][1]
    return residule_G


def get_level_graph (G,G_f) :
    #using BFS to get level graph
    G_r = residule_graph(G,G_f)



    visited = [False]*n
    level = [0] * n
    level_count = 1
    queue = [0]

    while queue :
        v = queue.pop(0) #deque

        for i in range(len(G_r[v])) :
            if G_r[v][i][1] != 0 and visited[G_r[v][i][0]] == False :
                queue.append(G_r[v][i][0])
                visited[G_r[v][i][0]] = True
                level[G_r[v][i][0]] = level[v] + 1


    return level


if __name__ == "__main__" :
    G,n,m = read_graph() #graph, # of vertices , # of edges
    G_f = deepcopy(G)
    for i in range(len(G_f)) :
        for j in range(len(G_f[i])) :
            G_f[i][j][1] = 0

    while(1) :
        level = get_level_graph(G,G_f)
        print(level)
        break
