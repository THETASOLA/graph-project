from B2_graphClass import Node, Graph
import os
import contextlib

def input_file():
    """
    Ask the user to choose a constraint table
    :return num_file: the number of the file to read
    """
    num_file = 0
    while num_file < 1 or num_file > 14:
        num_file = int(input("Veuillez choisir une table de contrainte de "
                             "1 à 14 en inscrivant le numéro de la table : "))
        if num_file < 1 or num_file > 14:
            print("Veuillez entrer un numéro de table valide")

    return num_file

def read_file(filename):
    """
    Read file, remove backslash n, and return a list of steps from the constraint table
    :param filename: the name of the file
    :return steps: a list of steps from the constraint table
    """
    with open(filename, 'r') as f:
        data = f.readlines()

        # removing backslash n from the end of the line
        for i in range(0, len(data)):
            data[i] = remove_backslashn(data[i])

        # splitting the line by comma
        steps = []
        for i in range(0, len(data)):
            steps.append(data[i].split(','))
            # splitting each steps by space
            steps[i] = steps[i][0].split(' ')
            # removing empty string
            if steps[i][len(steps[i])-1] == '':
                steps[i].pop(len(steps[i])-1)

    # converting the second element (weight) of each step to int
    for i in range(0, len(steps)):
        steps[i][1] = int(steps[i][1])

    return steps

def remove_backslashn(step):
    """
    Remove backslash n from the end of line
    :param step: The line with a backslash n
    :return step: The line without backslash n
    """
    if step[-1] == "\n":
        step = step[:-1]
    return step



def graph_initialization(num_file):
    """
    Initialize the graph with the constraint table
    :param num_file: number of the file to read
    :return nodes, graph, start_node, end_node:
    """
    # read file
    constraint_table = read_file("./B2_test_file/table " + str(num_file) + ".txt")
    # initialize nodes
    nodes = {element[0]: Node(element[0]) for element in constraint_table}

    # add neighbors to nodes
    for element in constraint_table:
        if len(element) > 2:
            for i in range(2, len(element)):
                nodes[element[i]].add_neighbor(nodes[element[0]], constraint_table[int(element[i]) - 1][1])

    graph = Graph()
    graph.directed = True

    for node in nodes.values():
        graph.add_node(node)

    # get start and end node
    start_node = graph.get_start_node()
    end_node = graph.get_end_node()

    return nodes, graph, start_node, end_node

def traces_execution():
    """
    Test all the functions and write all the result in txt file
    :param: None
    """
    # Check if the directory contain all the test files : to know if the file traces.txt already exists
    # path of the directory
    path = "B2_traces_execution"
    # Check if the directory exists
    if not os.path.exists(path):
        os.makedirs(path)
    # Getting the list of directories
    dir_traces = os.listdir(path)
    # Checking if the list of directories contains all the test files
    if len(dir_traces) < 14:

        # Running the function for each file
        for num_file in range(1, 15):
            nodes, graph, start_node, end_node = graph_initialization(num_file)
            with open("B2_traces_execution/B2_trace_graph_" + str(num_file) + ".txt", "w", encoding="utf-8") as f:
                f.write("----------- Etape 1 : Lecture de la table de contrainte et création des nœuds -----------\n")
                # Number of nodes
                highest_node_value = max(map(int, (node.name for node in graph.nodes)))
                if start_node.name == "0" and end_node.name == str(highest_node_value):
                    f.write(f"Nombre de sommets : {len(nodes) + 2}\n")
                elif start_node.name == "0" or end_node.name == str(highest_node_value):
                    f.write(f"Nombre de sommets : {len(nodes) + 1}\n")
                else:
                    f.write(f"Nombre de sommets : {len(nodes)}\n")

                # Number of edges
                f.write(f"Nombre d'arcs : {graph.number_of_edges()}\n\n")

                # Description of the node neighbors and their weights
                f.write("Node --> successor : weight\n")
                # If start_node is "0", write it to the file
                if start_node.name == "0":
                    for neighbor, weight in start_node.neighbors.items():
                        f.write(f"{start_node.name} --> {neighbor} : {weight}\n")

                for node in nodes.values():
                    for neighbor, weight in node.neighbors.items():
                        f.write(f"{node.name} --> {neighbor} : {weight}\n")

                f.write("\n----------- Etape 2 : Matrice des valeurs -----------\n")
                # Redirect the std output to the file
                with contextlib.redirect_stdout(f):
                    graph.print_graph()
                    print("\n")

                f.write("------------- Etape 3 : Etat des entrées/sorties et ordonnancement -------------\n")
                # Write the start and end node to the file
                # If the start_node is "0"
                if start_node.name == "0":
                    # Get the list of all the initiales nodes
                    starts = str(list(start_node.neighbors.keys())).translate({ord(i): None for i in '[\']'})
                    # Write the result to the file
                    f.write(f"Il y a une seule entrée {start_node.name}, car il y a {len(start_node.neighbors.keys())} entrées initiales : {starts}\n")
                else:
                    f.write(f"Il y a une seule entrée {start_node.name}\n")

                # If the end_node is the highest node value + 1
                if end_node.name == str(highest_node_value):
                    # Get the list of all the final nodes
                    ends = str(list(graph.search_pred(end_node))).translate({ord(i): None for i in '[\']'})
                    # Write the result to the file
                    f.write(f"Il y a une seule sortie {end_node.name}, car il y a {len(graph.search_pred(end_node))} sorties initiales : {ends}\n")
                else:
                    f.write(f"Il y a une seule sortie {end_node.name}\n")

                f.write("\n----------- Etape 4 : Vérification des propriétés du graphe -----------\n")
                if graph.is_cyclic():
                    f.write("-> Le graphe est cyclique\n")
                else:
                    f.write("-> Le graphe n'est pas cyclique\n")

                if graph.verif_poids():
                    f.write("-> Il n'y a pas de poids négatif\n")
                else:
                    f.write("-> Il y a un poids négatif\n")

                if not graph.is_cyclic() and graph.verif_poids():
                    f.write("==> C’est donc un graphe d’ordonnancement")
                else:
                    f.write("==> Ce n'est pas un graphe d’ordonnancement")