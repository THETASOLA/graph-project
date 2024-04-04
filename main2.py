
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.rang = -1

    def add_neighbor(self, neighbor, weight):
        self.neighbors[neighbor.name] = weight

    #I'm not sure if we should use this method, but I leave it there, it could be useful
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __str__(self):
        return "Node_"+self.name


class Graph:
    def __init__(self):
        self.nodes = []
    
    def get_node_from_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def check_node(self, nodeName):
        for node in self.nodes:
            if node.name == nodeName:
                return True
        return False

    def add_node(self, node):
        if not self.check_node(node.name):
            self.nodes.append(node)

    def add_edge(self, node1, node2, dist):
        if self.check_node(node2.name) and self.check_node(node1.name):
            node1.add_neighbor(node2.name, dist)

    def is_cyclic(self):
        def dfs(start_node, visited, parent):
            visited.add(start_node.name)
            for neighbor in start_node.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                if neighbor.name not in visited:
                    if dfs(neighbor, visited, start_node):
                        return True
                elif parent != neighbor:
                    return True
            return False

        visited = set()
        for node in self.nodes:
            if node.name not in visited:
                if dfs(node, visited, None):
                    return True
        return False

    def get_previous(self, node, done=[]):
        previous = []
        for n in self.nodes:
            for neighbor in n.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                if neighbor.name == node.name and n.name not in done:
                    previous.append(n)
        return previous

    def verif_rang(self):
        for node in self.nodes:
            if node.rang== -1:
                return False
        return True

    def verif_poids(self):
        for node in self.nodes:
            for values in node.neighbors.values():
                if int(values)<0:
                    print(node.name, "a un poids négatif")
                    return False
        return True

    def get_rank(self,start):
        cpt_rank = 0
        done=[]
        if self.check_node(start)==True:
            for node in self.nodes:
                if self.get_previous(node,done)==[]:
                    node.rang=cpt_rank
                    cpt_rank+=1
                    done.append(node.name)
                    print(node.name, node.rang, done)
            if self.verif_rang()==True:
                print("Les rangs ont été attribué avec succès")
            else:
                print("Les rangs n'ont pas été attribués")
                for nodes in self.nodes:
                    nodes.rang=-1
        return None


    def print_graph(self):

        print(" \t", end="")
        for node in self.nodes:
            print(node.name, end="\t")
        print()

        for node in self.nodes:
            print(node.name, end="\t")
            for node2 in self.nodes:
                found = "*"
                for neighbor in node.neighbors.keys():
                    neighbor = self.get_node_from_name(neighbor)
                    if neighbor.name == node2.name:
                        found = node.neighbors[neighbor.name]
                print(found, end="\t")
            print()
            

    def draw(self):

        G = nx.DiGraph()

        for node in self.nodes:
            for neighbor in node.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                G.add_edge(node.name, neighbor.name)

        pos = nx.spring_layout(G)

        nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=True, arrowstyle='-|>')

        plt.show()


nodes = {name: Node(name) for name in "ABCDEH"}
nodes["A"].add_neighbor(nodes["B"], 5)
nodes["A"].add_neighbor(nodes["C"], 5)
nodes["A"].add_neighbor(nodes["D"], 5)
nodes["A"].add_neighbor(nodes["E"], 5)
nodes["B"].add_neighbor(nodes["C"], 5)
nodes["B"].add_neighbor(nodes["D"], 5)
nodes["B"].add_neighbor(nodes["E"], 5)
nodes["C"].add_neighbor(nodes["D"], 5)
nodes["C"].add_neighbor(nodes["E"], 5)
nodes["D"].add_neighbor(nodes["E"], 5)
"""
nodes["A"].add_neighbor(nodes["B"], 5)
nodes["A"].add_neighbor(nodes["C"], 5)
nodes["A"].add_neighbor(nodes["D"], 5)
nodes["A"].add_neighbor(nodes["E"], 5)
nodes["A"].add_neighbor(nodes["F"], 5)
nodes["A"].add_neighbor(nodes["G"], 5)
nodes["A"].add_neighbor(nodes["H"], 5)
nodes["B"].add_neighbor(nodes["C"], 5)
nodes["B"].add_neighbor(nodes["D"], 5)
nodes["B"].add_neighbor(nodes["E"], 5)
nodes["C"].add_neighbor(nodes["F"], 5)
nodes["C"].add_neighbor(nodes["G"], 5)
nodes["D"].add_neighbor(nodes["E"], 5)
nodes["E"].add_neighbor(nodes["D"], 5)
nodes["E"].add_neighbor(nodes["G"], 5)
nodes["F"].add_neighbor(nodes["C"], 5)
nodes["F"].add_neighbor(nodes["H"], 5)
nodes["G"].add_neighbor(nodes["C"], 5)
nodes["G"].add_neighbor(nodes["E"], 5)
nodes["H"].add_neighbor(nodes["F"], 5)"""




graph = Graph()
graph.directed = True

for node in nodes.values():
    graph.add_node(node)

graph.get_rank("A")
graph.verif_poids()

"affiche infos sur les noeuds"
for i in graph.nodes:
    print(i.name)
    print(i.neighbors.keys())
    print(i.rang)
    print("\n")


if graph.is_cyclic():
    print("The graph contains a cycle.")
else:
    print("The graph does not contain a cycle.")

# Draw the graph
graph.print_graph()
graph.draw()