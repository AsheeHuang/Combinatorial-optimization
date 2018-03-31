import networkx as nx
import random

def Data_Gen(n,density,UB,file) :
    G = nx.gnp_random_graph(n, density, directed=True)
    DAG = nx.DiGraph([(u, v, {'weight': random.randint(-10, 10)}) for (u, v) in G.edges() if u < v])
    f.write(str(n)+"\n")
    f.write(str(DAG.number_of_edges())+"\n")
    for i in DAG.edges :
        c = random.randint(1,UB)
        f.write(str(i[0])+"  "+str(i[1])+"  "+str(c)+"\n")

if __name__ == "__main__" :

    for n in range(1000,10001,1000) :
        density = 0.01
        UB = 100
        name = str(n)#+"_"+str(density)
        path = "./Data/"+name+".txt"

        f = open(path,"w")
        Data_Gen(n = n,density = density,UB = UB,file = f)
        f.close()
        print("Finished")