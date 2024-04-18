from graphClass import Node, Graph

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
    constraint_table = read_file("./test_file/table " + str(num_file) + ".txt")
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
    """
    # Code bon à mettre en place quand on aura les vrais start et end node avec plusieurs départs et fins
    start_node = graph.get_start_node(graph.find_nodes_without_predecessors())
    end_node = graph.get_end_node(graph.find_nodes_without_successors())
    """

    # Attribution TEMPORAIRE de start_node et end_node pour faire fonctionner le programme
    start_node = graph.get_start_node("1")
    end_node = graph.get_end_node(f"{len(nodes)}")

    return graph, start_node, end_node
