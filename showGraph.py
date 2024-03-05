import networkx as nx
import matplotlib.pyplot as plt

def horizontal_header(data):
    print(" \t", end="")
    for node in data.keys():
        print(node, end="\t")
    print()

def generateGraph(data):
    horizontal_header(data)
    for node in data.keys():
        print(node, end="\t")
        for node2 in data.keys():
            found = "*"
            for neighbor in data[node]:
                if neighbor == node2:
                    found = neighbor
            print(found, end="\t")
        print()


def drawGraph(data, directed=False):
    G = nx.Graph()
    if directed:
        G = nx.DiGraph()

    for node in data.keys():
        G.add_node(node)
        for neighbor in data[node]:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G)

    if directed:
        nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=True, arrowstyle='-|>')
    else:
        nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=False)

    plt.show()