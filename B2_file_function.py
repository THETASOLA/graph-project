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
    # Getting the list of directories
    dir_traces = os.listdir(path)
    # Checking if the list of directories contains all the test files
    if len(dir_traces) < 14:

        # Running the function for each file
        for num_file in range(1, 15):
            nodes, graph, start_node, end_node = graph_initialization(num_file)
            with open("B2_traces_execution/trace_graph_" + str(num_file) + ".txt", "w", encoding="utf-8") as f:
                f.write("----------- Etape 1 : Lecture de la table de contrainte et création des nœuds -----------\n")
                # TODO: nombre de sommets et d'arcs en comptant les entrées et sorties à 0
                """f.write(f"Nombre de sommets : {len(nodes)}\n")"""  # TODO : Ajouter sommets d'entrée et de sortie quand E et S

                f.write("----------- Etape 2 : Matrice des valeurs -----------\n")
                # Redirect the std output to the file
                with contextlib.redirect_stdout(f):
                    graph.print_graph()
                    print("\n")

                f.write("------------- Etape 3 -------------\n")

                """f.write("Affichage du graphe\n")
                f.write(str(graph.print_graph()) + "\n\n")

                f.write("Vérification si le graphe est cyclique\n")
                f.write(str(graph.is_cyclic()) + "\n\n")

                f.write("Vérification si le graphe contient des poids négatifs\n")
                f.write(str(graph.verif_poids()) + "\n\n")

                f.write("Affichage des chemins de E à S\n")
                f.write(str(graph.display_paths(start_node, end_node)) + "\n\n")

                f.write("Dessin du graphe\n")
                f.write(str(graph.draw()) + "\n\n")
                """
