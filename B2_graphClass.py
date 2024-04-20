import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = {}
        self.rank = -1

    def add_neighbor(self, neighbor, weight):
        self.neighbors[neighbor.name] = weight

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return f"Node_{self.name}"

class Graph:
    def __init__(self):
        self.nodes = []

    def get_node_from_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node
        return None

    def check_node(self, node_name):
        return any(node.name == node_name for node in self.nodes)

    def add_node(self, node):
        if not self.check_node(node.name):
            self.nodes.append(node)

    def add_edge(self, node1, node2, dist):
        if self.check_node(node1.name) and self.check_node(node2.name):
            node1.add_neighbor(node2, dist)

    def is_cyclic(self):
        def dfs(start_node, visited, parent):
            visited.add(start_node.name)
            for neighbor in start_node.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                if neighbor.name not in visited:
                    if dfs(neighbor, visited, start_node):
                        return True
                elif parent is not None and parent.name == neighbor.name:
                    return True
            return False

        visited = set()
        for node in self.nodes:
            if node.name not in visited:
                if dfs(node, visited, None):
                    return True
        return False

    def get_previous(self, node, done=None):
        if done is None:
            done = []
        previous = []
        for n in self.nodes:
            for neighbor in n.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                if neighbor.name == node.name and n.name not in done:
                    previous.append(n)
        return previous

    def verif_rang(self):
        return all(node.rank != -1 for node in self.nodes)

    def verif_poids(self):
        for node in self.nodes:
            for value in node.neighbors.values():
                if value < 0:
                    return False
        return True

    def get_rank(self, start):
        cpt_rank = 0
        done = []
        if self.check_node(start):
            for node in self.nodes:
                if self.get_previous(node, done) == []:
                    node.rank = cpt_rank
                    cpt_rank += 1
                    done.append(node.name)
            if self.verif_rang():
                print("\nRangs assigné avec succès\n")
            else:
                print("\nRangs non assigné avec succès\n")
                for nodes in self.nodes:
                    nodes.rank = -1
        return None

    def get_start_node(self):
        start_nodes = self.find_nodes_without_predecessors()
        if len(start_nodes) == 1:
            return self.get_node_from_name(start_nodes[0])
        elif len(start_nodes) > 1:
            # Créer un nouveau nœud 'E'
            new_start_node = Node('E')
            self.add_node(new_start_node)
            # Ajouter des arêtes de 'E' vers tous les nœuds de début avec un poids de 0
            for start_node in start_nodes:
                start_node_obj = self.get_node_from_name(start_node)
                new_start_node.add_neighbor(start_node_obj, 0)
            return new_start_node
        else:
            raise ValueError("Il n'y a pas de nœud de départ dans le graphe.")


    def get_end_node(self):
        end_nodes = self.find_nodes_without_successors()
        if len(end_nodes) == 1:
            return self.get_node_from_name(end_nodes[0])
        elif len(end_nodes) > 1:
            # Créer un nouveau nœud 'S'
            new_end_node = Node('S')
            self.add_node(new_end_node)
            # Ajouter des arêtes de tous les nœuds de fin vers 'S' avec un poids de 0
            for end_node in end_nodes:
                end_node_obj = self.get_node_from_name(end_node)
                end_node_obj.add_neighbor(new_end_node, 0)
            return new_end_node
        else:
            raise ValueError("Il n'y a pas de nœud d'arrivée dans le graphe.")

    # search_pred : cette fonction renvoie un tableau des prédécesseurs du nœud mis en paramètre
    def search_pred(self, node):
        return [neighbor.name for neighbor in self.nodes if node.name in neighbor.neighbors.keys()]

    # search_succ : cette fonction renvoie un tableau des successeurs du nœud mis en paramètre
    def search_succ(self, node):
        return [neighbor.name for neighbor in self.nodes if node.name in neighbor.neighbors]

    # find_nodes_without_successors : cette fonction renvoie un tableau des nœuds sans successeurs
    def find_nodes_without_successors(self):
        nodes_without_successors = []
        for node in self.nodes:
            if not node.neighbors:
                nodes_without_successors.append(node.name)
        return nodes_without_successors

    # find_nodes_without_predecessors : cette fonction renvoie un tableau des nœuds sans prédécesseurs
    def find_nodes_without_predecessors(self):
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

    # get_total_weight : cette fonction renvoie la somme des poids des nœuds mis en paramètres
    def get_total_weight(self, path):
        total_weight = 0
        for i in range(len(path) - 1):
            node1 = path[i]
            node2 = path[i + 1]
            total_weight += node1.neighbors[node2.name]
        return total_weight

    # get_path : cette fonction renvoie un tableau de nœud qui sont nécessaire au parcours du graph d'un nœud d'entré à un nœud de sortie placé en paramètre
    def get_path(self, start_node, end_node):
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
        if not self.verif_poids():
            print("Il y a un poids négatif")
            return

        # Récupérer les successeurs de tous les nœuds
        successors = {node.name: self.search_succ(node) for node in self.nodes}
        print("\nSuccesseurs de tous les nœuds :")
        for node, succ in successors.items():
            print(f"{node} : {succ}")

        # Récupérer les prédécesseurs de tous les nœuds
        predecessors = {node.name: self.search_pred(node) for node in self.nodes}
        print("\nPrédécesseurs de tous les nœuds :")
        for node, pred in predecessors.items():
            print(f"{node} : {pred}")

        # Récupérer tous les chemins possibles pour aller du nœud start_node au nœud end_node
        all_paths = self.get_path(start_node, end_node)
        print(f"\nTous les chemins possibles pour aller du nœud {start_node.name} au nœud {end_node.name} :")
        for path in all_paths:
            print([node.name for node in path])

        # Récupérer le poids total de chaque chemin possible pour aller du nœud start_node au nœud end_node
        path_weights = [self.get_total_weight(path) for path in all_paths]
        print(f"\nPoids total de chaque chemin possible pour aller du nœud {start_node.name} au nœud {end_node.name} :")
        for weight in path_weights:
            print(weight)

        # Afficher les informations sous forme de tableau dans la console
        print(f"\nInformations sur tous les chemins possibles pour aller du nœud {start_node.name} au nœud {end_node.name} :")
        for path, weight in zip(all_paths, path_weights):
            print(f"Chemin : {[node.name for node in path]}, Poids total : {weight}")

        # Trouver le chemin le plus court et le chemin le plus long
        min_weight = min(path_weights)
        max_weight = max(path_weights)
        min_path = all_paths[path_weights.index(min_weight)]
        max_path = all_paths[path_weights.index(max_weight)]

        # Afficher les résultats
        print(f"\nLe chemin le plus court est de {min_weight} en passant par : {' -> '.join([node.name for node in min_path])}")
        print(f"Le chemin le plus long est de {max_weight} en passant par : {' -> '.join([node.name for node in max_path])}")

    def print_graph(self):
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
        G = nx.DiGraph()

        for node in self.nodes:
            for neighbor in node.neighbors.keys():
                neighbor = self.get_node_from_name(neighbor)
                G.add_edge(node.name, neighbor.name, weight=node.neighbors[neighbor.name])

        pos = nx.spring_layout(G)

        # Définir les couleurs des nœuds
        node_colors = []
        first_node = self.nodes[0].name
        last_node = self.nodes[-1].name

        for node in G.nodes():
            if node == 'E':
                node_colors.append('green')
            elif node == 'S':
                node_colors.append('red')
            else:
                node_colors.append('white')

        # Dessiner les nœuds avec les couleurs définies
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)

        # Dessiner les arêtes avec les poids en tant que labels
        edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
        nx.draw_networkx_edges(G, pos, edge_color='black', arrows=True, arrowstyle='-|>')
        nx.draw_networkx_labels(G, pos, font_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')

        plt.show()
