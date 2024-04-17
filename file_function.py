from graphClass import Node, Graph
def read_file(filename):
    """
    Read file, remove backslash n, and return a list of steps from the constraint table
    :param filename: the name of the file
    :return steps:
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
    Initialize nodes
    :return nodes:
    """
    # read file
    constraint_table = read_file("./test_file/table " + str(num_file) + ".txt")
    # initialize nodes
    nodes = {element[0]: Node(element[0]) for element in constraint_table}

    for element in constraint_table:
        if len(element) > 2:
            for i in range(2, len(element) - 1):
                nodes[element[i]].add_neighbor(nodes[element[0]], constraint_table[int(element[i])][1])

    graph = Graph()
    graph.directed = True

    for node in nodes.values():
        graph.add_node(node)

    start_node = graph.get_start_node(1)
    end_node = graph.get_end_node(len(nodes))

    return nodes, graph, start_node, end_node
