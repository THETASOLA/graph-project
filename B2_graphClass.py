import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.rank = -1

    def add_neighbor(self, neighbor, weight):
        """
        Add a neighbor to the node with a given weight
        :param neighbor:
        :param weight:
        :return:
        """
        self.neighbors[neighbor.name] = weight

    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"Node_{self.name}"

class Graph:
    def __init__(self):
        self.nodes = []

    def get_node_from_name(self, name):
        """
        Get a node from its name
        :param name:
        :return:
        """
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def check_node(self, node_name):
        """
        Check if a node exists in the graph
        :param node_name:
        :return:
        """
        return any(node.name == node_name for node in self.nodes)

    def add_node(self, node):
        """
        Add a node to the graph
        :param node:
        :return:
        """
        if not self.check_node(node.name):
            self.nodes.append(node)

    def add_edge(self, node1, node2, dist):
        """
        Add an edge between two nodes with a given distance
        :param node1:
        :param node2:
        :param dist:
        :return:
        """
        if self.check_node(node1.name) and self.check_node(node2.name):
            node1.add_neighbor(node2, dist)

    def is_cyclic(self, cpt=0, done=None):
        """
        Check if the graph is cyclic
        :param cpt: counter
        :param done: list of nodes already visited
        :return boolean: True if the graph is cyclic, False otherwise
        """
        if done is None:
            done = []
            cpt = 0
        if len(done) == len(self.nodes):
            return False

        if cpt > len(self.nodes):
            return True

        done_temp = []
        for node in self.nodes:
            if self.get_previous(node, done) == [] and node.name not in done:
                done_temp.append(node.name)
        for i in range(len(done_temp)):
            done.append(done_temp[i])
        return self.is_cyclic(cpt + 1, done)




    def verif_rank(self):
        """
        Check if all nodes have a rank
        :return:
        """
        for node in self.nodes:
            if node.rank == -1:
                return False
        return True

    def verif_poids(self):
        """
        Check if all weights are positive
        :return Bolean value:
        """
        for node in self.nodes:
            for values in node.neighbors.values():
                if int(values) < 0:
                    print(node.name, "a un poids négatif")
                    return False
        return True

    def get_previous(self, node, done=None):
        """
        Get the previous nodes of a given node
        :param node:
        :param done:
        :return:
        """
        previous = []
        for n in self.nodes:
            for neighbor in n.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                if neighbor.name == node.name and n.name not in done:
                    previous.append(n.name)
        return previous


    def get_rank(self, done=None, cpt_rank=0):
        """
        Assign ranks to all nodes if the graph is acyclic
        :return:
        """
        if done is None:
            done = []
            cpt_rank = 0
            if self.is_cyclic() == True:
                print("\nImpossible de donner un rang à un graphe cyclique\n")
                return None

        if self.verif_rank() == True:
            for node in self.nodes:
                print(f"Le noeud {node.name}, a un rang de {node.rank}")
            return None

        done_temp = []
        for node in self.nodes:
            if self.get_previous(node, done) == [] and node.name not in done:
                node.rank = cpt_rank
                done_temp.append(node.name)
        for i in range(len(done_temp)):
            done.append(done_temp[i])
        return self.get_rank(done, cpt_rank + 1)


    def get_start_node(self):
        """
        Get the start nodes of the graph
        :return:
        """
        start_nodes = self.find_nodes_without_predecessors()
        if len(start_nodes) == 1:
            return self.get_node_from_name(start_nodes[0])
        elif len(start_nodes) > 1:
            # Create a new node '0'
            new_start_node = Node('0')
            self.add_node(new_start_node)
            # Add edges from all start nodes to '0' with a weight of 0
            for start_node in start_nodes:
                start_node_obj = self.get_node_from_name(start_node)
                new_start_node.add_neighbor(start_node_obj, 0)
            return new_start_node
        else:
            raise ValueError("Il n'y a pas de nœud de départ dans le graphe.")



    def get_end_node(self):
        """
        Get the end nodes of the graph
        :return:
        """
        end_nodes = self.find_nodes_without_successors()
        if len(end_nodes) == 1:
            return self.get_node_from_name(end_nodes[0])
        elif len(end_nodes) > 1:
            # Create a new node 'S'
            #new_end_node = Node('S')
            # Create a new node with value of last node + 1
            last_node_value = max(map(int, (node.name for node in self.nodes)))
            new_end_node = Node(str(last_node_value + 1))
            self.add_node(new_end_node)
            # Add edges from all end nodes to the new node with a weight of 0
            for end_node in end_nodes:
                end_node_obj = self.get_node_from_name(end_node)
                end_node_obj.add_neighbor(new_end_node, 0)
            return new_end_node
        else:
            raise ValueError("Il n'y a pas de nœud d'arrivée dans le graphe.")
        
    def search_pred(self, node):
        """
        Get the predecessors of a given node
        :param node:
        :return neighbor.name:
        """
        return [neighbor.name for neighbor in self.nodes if node.name in neighbor.neighbors.keys()]

    def search_succ(self, node):
        """
        Get the successors of a given node
        :param node:
        :return neighbor.name
        """
        return [neighbor.name for neighbor in self.nodes if neighbor.name in node.neighbors]

    def find_nodes_without_successors(self):
        """
        Get the nodes without successors
        :return nodes_without_successors: return a list of nodes without successors
        """
        nodes_without_successors = []
        for node in self.nodes:
            if not node.neighbors:
                nodes_without_successors.append(node.name)
        return nodes_without_successors

    def find_nodes_without_predecessors(self):
        """
        Get the nodes without predecessors
        :return nodes_without_predecessors: return a list of nodes without predecessors
        """
        nodes_without_predecessors = []
        for node in self.nodes:
            has_predecessor = False
            for potential_predecessor in self.nodes:
                if node.name in potential_predecessor.neighbors:
                    has_predecessor = True
                    break
            if not has_predecessor:
                nodes_without_predecessors.append(node.name)
        return nodes_without_predecessors

    def get_total_weight(self, path):
        """
        Get the total weight of a path
        :param path:
        :return total_weight: return the total weight of the path
        """
        total_weight = 0
        for i in range(len(path) - 1):
            node1 = path[i]
            node2 = path[i + 1]
            total_weight += node1.neighbors[node2.name]
        return total_weight

    def get_path(self, start_node, end_node):
        """
        Get all possible paths from a start node to an end node
        :param start_node:
        :param end_node:
        :return paths: return all possible paths from start_node to end_node
        """
        paths = []
        stack = [(start_node, [start_node])]
        while stack:
            current_node, path = stack.pop()
            if current_node == end_node:
                paths.append(path)
            else:
                for neighbor in current_node.neighbors:
                    neighbor_node = self.get_node_from_name(neighbor)
                    if neighbor_node not in path:
                        new_path = path + [neighbor_node]
                        stack.append((neighbor_node, new_path))
        return paths

    def display_paths(self, start_node, end_node):
        """
        Display all possible paths from a start node to an end node
        :param start_node:
        :param end_node:
        :return:
        """
        if self.is_cyclic():
            print("\nLe graphe est cyclique impossible")
            return

        if not self.verif_poids():
            print("Il y a un poids négatif")
            return

        """
        # Get the successors of all nodes
        successors = {node.name: self.search_succ(node) for node in self.nodes}
        for node, succ in successors.items():
            print(f"{node} : {succ}")

        # Get the predecessors of all nodes
        predecessors = {node.name: self.search_pred(node) for node in self.nodes}
        print("\nPrédécesseurs de tous les nœuds :")
        for node, pred in predecessors.items():
            print(f"{node} : {pred}")"""

        # Get all possible paths from the start node to the end node
        all_paths = self.get_path(start_node, end_node)

        # Get the total weight of each possible path from start_node to end_node
        path_weights = [self.get_total_weight(path) for path in all_paths]

        # Display information in tabular form in the console
        print(
            f"\nInformations sur tous les chemins possibles pour aller du nœud {start_node.name} au nœud {end_node.name} :")
        for path, weight in zip(all_paths, path_weights):
            print(f"Chemin : {[node.name for node in path]}, Poids total : {weight}")

        # Find the shortest and longest paths
        min_weight = min(path_weights)
        max_weight = max(path_weights)
        min_paths = [path for path in all_paths if path_weights[all_paths.index(path)] == min_weight]
        max_paths = [path for path in all_paths if path_weights[all_paths.index(path)] == max_weight]

        # Calculate earliest start and finish times
        earliest_start = {node: 0 for node in self.nodes}
        earliest_finish = {node: 0 for node in self.nodes}
        latest_start = {node: 0 for node in self.nodes}
        latest_finish = {node: 0 for node in self.nodes}

        # Initialize start node
        earliest_start[start_node] = 0
        earliest_finish[start_node] = 0
        latest_start[start_node] = 0
        latest_finish[start_node] = 0

        # Calculate earliest start and finish times for other nodes
        for node in self.nodes:
            for neighbor in node.neighbors:
                neighbor_node = self.get_node_from_name(neighbor)
                earliest_start[neighbor_node] = max(earliest_start[neighbor_node], earliest_finish[node] + self.get_node_from_name(node.name).neighbors[neighbor])
                if neighbor in neighbor_node.neighbors:  # Check if neighbor is in neighbor_node's neighbors
                    earliest_finish[neighbor_node] = earliest_start[neighbor_node] + neighbor_node.neighbors[neighbor]
                else:
                    earliest_finish[neighbor_node] = earliest_start[neighbor_node]


        # Calculate latest start and finish times
        latest_finish[end_node] = earliest_finish[end_node]
        latest_start[end_node] = earliest_start[end_node]

        for node in reversed(self.nodes):
            for neighbor in node.neighbors:
                neighbor_node = self.get_node_from_name(neighbor)
                latest_finish[node] = max(latest_finish[node], latest_start[neighbor_node] - self.get_node_from_name(node.name).neighbors[neighbor])
                latest_start[node] = latest_finish[node] - self.get_node_from_name(node.name).neighbors[neighbor]

        # Calculate total and free margins
        total_margin = {node: latest_start[node] - earliest_start[node] for node in self.nodes}
        free_margin = {node: earliest_start[node] - latest_start[node] for node in self.nodes}
        """
        # Print margins
        print("\nMarge Totales:")
        for node, margin in total_margin.items():
            print(f"Node {node.name}: {margin}")

        print("\nMarge libres:")
        for node, margin in free_margin.items():
            print(f"Node {node.name}: {margin}")
        """
        # Display results
        print(f"\nLes chemins les plus courts sont de {min_weight} en passant par : ")
        for i, min_path in enumerate(min_paths):
            print(f"Chemin {i+1} : {' -> '.join([node.name for node in min_path])}")

        print(f"Les chemins les plus longs de {max_weight} en passant par : ")

        # Draw each max path
        for i, max_path in enumerate(max_paths):
            max_graph = Graph()
            for node in max_path:
                max_graph.add_node(node)
            for i in range(len(max_path) - 1):
                node1 = max_path[i]
                node2 = max_path[i + 1]
                max_graph.add_edge(node1, node2, self.get_node_from_name(node1.name).neighbors[node2.name])
            print(f"Chemin : {' -> '.join([node.name for node in max_path])}")
            self.draw_max_path(max_path)


    def draw_max_path(self, max_path):
        """
        Draw the graph with only the nodes and edges in the max path
        :param max_path: list of nodes in the max path
        :return: None
        """
        G = nx.DiGraph()

        for i in range(len(max_path) - 1):
            node1 = max_path[i]
            node2 = max_path[i + 1]
            G.add_node(node1.name)
            G.add_node(node2.name)
            G.add_edge(node1.name, node2.name, weight=node1.neighbors[node2.name])

        node_colors = ['green' if node == max_path[0].name else ('red' if node == max_path[-1].name else 'grey') for
                       node in G.nodes()]

        pos = nx.shell_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>')
        nx.draw_networkx_labels(G, pos, font_color='black')
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

        plt.show()

    def print_graph(self):
        """
        Print the graph in tabular form
        :return:
        """
        print(f"\nVotre graphe {', '.join([node.name for node in self.nodes])} a bien été pris en compte\n")
        for node in self.nodes:
            successors = ", ".join(neighbor for neighbor in node.neighbors.keys())
            weights = list(node.neighbors.values())

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
        """
        Draw the graph
        :return:
        """
        G = nx.DiGraph()

        for node in self.nodes:
            for neighbor in node.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                G.add_edge(node.name, neighbor.name, weight=node.neighbors[neighbor.name])
        
        pos = nx.shell_layout(G)

        # Définir les couleurs des nœuds
        node_colors = []

        for node in G.nodes():
            #if node == '0':
            if node == str(self.get_start_node().name):
                node_colors.append('green')
            #elif node == 'S':
            elif node == str(self.get_end_node().name):
                node_colors.append('red')
            else:
                node_colors.append('grey')

        # Dessiner les nœuds avec les couleurs définies
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)

        # Dessiner les arêtes avec les poids en tant que labels
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>')
        nx.draw_networkx_labels(G, pos, font_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

        plt.show()

    def number_of_edges(self):
        """
        Get the number of edges in the graph
        :return:
        """
        return sum(len(node.neighbors) for node in self.nodes)
