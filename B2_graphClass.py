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

    def get_path(self, start_node, end_node):
        # Vérifier que les nœuds de départ et d'arrivée existent dans le graphe
        if not self.check_node(start_node.name) or not self.check_node(end_node.name):
            print("Erreur : le nœud de départ ou le nœud d'arrivée n'existe pas dans le graphe")
            return None

        # Cas de base : si le nœud de départ est le même que le nœud d'arrivée, renvoyer un chemin avec un seul nœud
        if start_node.name == end_node.name:
            return [[start_node.name]]

        # Récupérer la liste des prédécesseurs du nœud d'arrivée
        predecessors = self.search_pred(end_node)

        # Initialiser une liste vide pour stocker tous les chemins possibles
        paths = []

        # Parcourir tous les prédécesseurs du nœud d'arrivée
        for predecessor in predecessors:
            # Récupérer le nœud prédécesseur
            pred_node = self.get_node_from_name(predecessor)

            # Récupérer la liste des chemins du nœud de départ au nœud prédécesseur
            pred_paths = self.get_path(start_node, pred_node)

            # Ajouter le nœud d'arrivée à chaque chemin du nœud prédécesseur
            for path in pred_paths:
                new_path = path + [end_node.name]
                paths.append(new_path)

        # Retourner la liste de tous les chemins possibles
        return paths
    
    def get_path_weight(self, path):
        # Vérifier que le chemin n'est pas vide
        if not path:
            print("Erreur : le chemin est vide")
            return None

        # Initialiser le poids total à 0
        total_weight = 0

        # Parcourir le chemin et ajouter les poids des arêtes entre chaque paire de nœuds consécutifs
        for i in range(len(path) - 1):
            current_node = self.get_node_from_name(path[i])
            next_node = self.get_node_from_name(path[i + 1])
            total_weight += current_node.neighbors[next_node.name]

        # Retourner le poids total du chemin
        return total_weight
     
    def get_task_ranks(self):
        start_node = self.get_start_node()
        # Vérifier que le graphe n'est pas cyclique
        if self.is_cyclic():
            print("Erreur : le graphe est cyclique")
            return None, None, None, None, None, None, None

        # Créer une liste vide pour stocker les rangs des tâches
        task_ranks = []

        # Créer une liste vide pour stocker les prédécesseurs de chaque tâche
        task_predecessors = []

        # Créer une liste vide pour stocker les successeurs de chaque tâche
        task_successors = []

        # Créer une liste vide pour stocker les chemins de chaque tâche
        task_paths = []

        # Créer une liste vide pour stocker les poids totaux des chemins de chaque tâche
        task_path_weights = []

        # Créer une liste vide pour stocker les dates au plus tôt de chaque tâche
        task_earliest_dates = []

        # Trier les nœuds du graphe par ordre croissant de rang
        sorted_nodes = sorted(self.nodes, key=lambda x: x.rank)

        # Parcourir la liste triée des nœuds et ajouter leur rang et leur nom à la liste des rangs des tâches
        for node in sorted_nodes:
            task_ranks.append(f"{node.rank}({node.name})")

            # Récupérer la liste des prédécesseurs de la tâche
            predecessors = self.search_pred(node)

            # Ajouter la liste des prédécesseurs à la liste des prédécesseurs de chaque tâche
            task_predecessors.append(predecessors)

            # Récupérer la liste des successeurs de la tâche
            successors = self.search_succ(node)

            # Ajouter la liste des successeurs à la liste des successeurs de chaque tâche
            task_successors.append(successors)

            # Récupérer tous les chemins du nœud de départ au nœud courant
            paths = self.get_path(start_node, node)

            # Ajouter la liste des chemins à la liste des chemins de chaque tâche
            task_paths.append(paths)

            # Calculer les poids totaux des chemins
            path_weights = []
            for path in paths:
                # Calculer le poids total du chemin
                path_weight = self.get_path_weight(path)

                # Ajouter le poids total du chemin à la liste des poids totaux des chemins de la tâche
                path_weights.append(path_weight)

            # Ajouter la liste des poids totaux des chemins à la liste des poids totaux des chemins de chaque tâche
            task_path_weights.append(path_weights)

            # Calculer la date au plus tôt pour la tâche
            earliest_date = max(path_weights)

            # Ajouter la date au plus tôt à la liste des dates au plus tôt de chaque tâche
            task_earliest_dates.append(earliest_date)

        # Créer une liste vide pour stocker les tâches et leurs longueurs associées
        tasks = []

        # Parcourir la liste triée des nœuds et ajouter leur nom et leur longueur à la liste des tâches et leurs longueurs associées
        for node in sorted_nodes:
            # Vérifier que le nœud a au moins un voisin entrant
            if node.neighbors:
                # Récupérer le poids de l'arête entrante
                incoming_edge = next(iter(node.neighbors.items()))
                incoming_weight = incoming_edge[1]

                # Ajouter le nom de la tâche et sa longueur à la liste des tâches et leurs longueurs associées
                tasks.append(f"{node.name}({incoming_weight})")
            else:
                # Ajouter le nom de la tâche avec une longueur de 0 à la liste des tâches et leurs longueurs associées
                tasks.append(f"{node.name}(0)")

        # Trouver la longueur maximale des dates au plus tôt
        max_earliest_date = max(task_earliest_dates)

        # Trouver le chemin correspondant à la date au plus tôt maximale
        max_earliest_date_index = task_earliest_dates.index(max_earliest_date)
        max_path = task_paths[max_earliest_date_index]
        max_path_str = '->'.join(str(node) for node in max_path)

        # Afficher le chemin le plus long et sa longueur
        print(f"\nLe chemin le plus long est de {max_earliest_date} en passant par {max_path_str}")

        # Retourner les listes des rangs des tâches, des tâches et leurs longueurs associées, des prédécesseurs et des successeurs de chaque tâche, des chemins et des poids totaux des chemins de chaque tâche, et des dates au plus tôt de chaque tâche
        return task_ranks, tasks, task_predecessors, task_successors, task_paths, task_path_weights, task_earliest_dates
    
    def print_table(self, task_ranks, tasks, task_predecessors, task_successors, task_paths, task_path_weights, task_earliest_dates):
            # Vérifier que les sept listes ont la même longueur
            if len(task_ranks) != len(tasks) or len(tasks) != len(task_predecessors) or len(task_predecessors) != len(task_successors) or len(task_successors) != len(task_paths) or len(task_paths) != len(task_path_weights) or len(task_path_weights) != len(task_earliest_dates):
                print("Erreur : les listes des rangs des tâches, des tâches et leurs longueurs associées, des prédécesseurs et des successeurs de chaque tâche, des chemins et des poids totaux des chemins de chaque tâche, et des dates au plus tôt de chaque tâche n'ont pas la même longueur")
                return

            # Imprimer l'en-tête du tableau
            print("Rang\tTâche et sa longueur\tPrédécesseurs\tSuccesseurs\tChemins\tPoids totaux des chemins\tDate au plus tôt")

            # Parcourir les listes des rangs des tâches, des tâches et leurs longueurs associées, des prédécesseurs et des successeurs de chaque tâche, des chemins et des poids totaux des chemins de chaque tâche, et des dates au plus tôt de chaque tâche
            for rank, task, predecessors, successors, paths, path_weights, earliest_date in zip(task_ranks, tasks, task_predecessors, task_successors, task_paths, task_path_weights, task_earliest_dates):
                # Imprimer le rang, la tâche et sa longueur associée, la liste des prédécesseurs, la liste des successeurs, la liste des chemins, la liste des poids totaux des chemins et la date au plus tôt de la tâche
                print(rank, "\t", task, "\t\t", predecessors, "\t\t", successors, "\t\t", paths, "\t\t", path_weights, "\t\t", earliest_date)

    def print_simplified_table(self, task_ranks, tasks, task_earliest_dates):
        # Vérifier que les trois listes ont la même longueur
        if len(task_ranks) != len(tasks) or len(tasks) != len(task_earliest_dates):
            print("Erreur : les listes des rangs des tâches, des tâches et leurs longueurs associées, et des dates au plus tôt de chaque tâche n'ont pas la même longueur")
            return

        # Imprimer l'en-tête du tableau
        print("Rang\tTâche\tDate au plus tôt")

        # Parcourir les listes des rangs des tâches, des tâches et leurs longueurs associées, et des dates au plus tôt de chaque tâche
        for rank, task, earliest_date in zip(task_ranks, tasks, task_earliest_dates):
            # Imprimer le rang, la tâche et la date au plus tôt de la tâche
            print(rank, "\t", task, "\t", earliest_date)
    
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
