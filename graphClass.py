import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

    def __str__(self):
        return self.name


class Graph:
    def __init__(self):
        self.nodes = {}
        self.directed = False

    def add_node(self, node):
        if node.name not in self.nodes:
            self.nodes[node.name] = node

    def add_edge(self, node1, node2):
        if node1.name in self.nodes and node2.name in self.nodes:
            self.nodes[node1.name].add_neighbor(node2.name)

    def is_cyclic(self):
        def dfs(start_node):
            visited = set()
            stack = [(start_node, None)]
            while stack:
                node, parent = stack.pop()
                visited.add(node)
                for neighbor in self.nodes[node].neighbors:
                    neighbor_name = neighbor.name
                    if neighbor_name == parent:
                        continue 
                    if neighbor_name in visited:
                        return True
                    stack.append((neighbor_name, node))
            return False

        for node_name in self.nodes.keys():
            if dfs(node_name):
                return True
        return False

    def draw(self):
        G = nx.Graph()
        if self.directed:
            G = nx.DiGraph()

        for node_name in self.nodes.keys():
            for neighbor_name in self.nodes[node_name].neighbors:
                G.add_edge(node_name, neighbor_name)

        pos = nx.spring_layout(G)

        if self.directed:
            nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=True, arrowstyle='-|>')
        else:
            nx.draw(G, pos, with_labels=True, font_weight='bold', arrows=False)

        plt.show()