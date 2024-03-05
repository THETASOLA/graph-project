import networkx as nx
import matplotlib.pyplot as plt

def horizontal_header(data):
    print(" \t", end="")
    for i in range(len(data)):
        print(chr(65+i), end="\t")
    print()

def generateGraph(data):
    horizontal_header(data)
    for i in range(len(data)):
        print(chr(65+i), end="\t")
        for j in range(len(data)):
            print(chr(65+i) if chr(65+j) in data[i][chr(65+i)] else "*", end="\t")
        print()
        
def drawGraph(data, directed=False):
    G = nx.Graph()
    if directed:
        G = nx.DiGraph()
        
    for i in range(len(data)):
        G.add_node(chr(65+i))
        for j in range(len(data)):
            if chr(65+j) in data[i][chr(65+i)]:
                if directed:
                    G.add_edge(chr(65+i), chr(65+j))
                else:
                    G.add_edge(chr(65+j), chr(65+i))
                
    pos = nx.spring_layout(G)
    
    nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=directed)
    plt.show()
