import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    #I'm not sure if we should use this method, but I leave it there, it could be useful
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name

    def __str__(self):
        return "Node_"+self.name


class Graph:
    def __init__(self):
        self.nodes = []
        self.directed = False
    
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

    def add_edge(self, node1, node2):
        if self.check_node(node2.name) and self.check_node(node1.name):
            node1.add_neighbor(node2.name)

    def is_cyclic(self):
        def dfs(start_node, visited, parent):
            visited.add(start_node.name)
            for neighbor in start_node.neighbors:
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

    def print_graph(self):

        print(" \t", end="")
        for node in self.nodes:
            print(node.name, end="\t")
        print()

        for node in self.nodes:
            print(node.name, end="\t")
            for node2 in self.nodes:
                found = "*"
                for neighbor in node.neighbors:
                    if neighbor.name == node2.name:
                        found = node.name
                print(found, end="\t")
            print()
            

    def draw(self):
        G = nx.Graph()
        if self.directed:
            G = nx.DiGraph()

        for node in self.nodes:
            for neighbor in node.neighbors:
                G.add_edge(node.name, neighbor.name)

        pos = nx.spring_layout(G)

        if self.directed:
            nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=True, arrowstyle='-|>')
        else:
            nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=False)

        plt.show()