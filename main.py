from graphClass import Node, Graph
nodes = {name: Node(name) for name in "ABCDEFGH"}

nodes["A"].add_neighbor(nodes["B"])
nodes["A"].add_neighbor(nodes["C"])
nodes["A"].add_neighbor(nodes["D"])
nodes["A"].add_neighbor(nodes["E"])
nodes["A"].add_neighbor(nodes["F"])
nodes["A"].add_neighbor(nodes["G"])
nodes["A"].add_neighbor(nodes["H"])
nodes["B"].add_neighbor(nodes["C"])
nodes["B"].add_neighbor(nodes["D"])
nodes["B"].add_neighbor(nodes["E"])
nodes["C"].add_neighbor(nodes["F"])
nodes["C"].add_neighbor(nodes["G"])
nodes["D"].add_neighbor(nodes["E"])
nodes["E"].add_neighbor(nodes["D"])
nodes["E"].add_neighbor(nodes["G"])
nodes["F"].add_neighbor(nodes["C"])
nodes["F"].add_neighbor(nodes["H"])
nodes["G"].add_neighbor(nodes["C"])
nodes["G"].add_neighbor(nodes["E"])
nodes["H"].add_neighbor(nodes["F"])

graph = Graph()
graph.directed = True

for node in nodes.values():
    graph.add_node(node)

if graph.is_cyclic():
    print("The graph contains a cycle.")
else:
    print("The graph is acyclic.")

# Draw the graph
graph.draw()