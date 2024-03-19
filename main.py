from graphClass import Node, Graph

nodes = {name: Node(name) for name in "ABCDEH"}
nodes["A"].add_neighbor(nodes["B"], 5)
nodes["A"].add_neighbor(nodes["C"], 5)
nodes["A"].add_neighbor(nodes["D"], 5)
nodes["A"].add_neighbor(nodes["E"], 5)
nodes["B"].add_neighbor(nodes["C"], 5)
nodes["B"].add_neighbor(nodes["D"], 5)
nodes["B"].add_neighbor(nodes["E"], 5)
nodes["C"].add_neighbor(nodes["D"], 5)
nodes["C"].add_neighbor(nodes["E"], 5)
nodes["D"].add_neighbor(nodes["E"], 5)
"""
nodes["A"].add_neighbor(nodes["B"], 5)
nodes["A"].add_neighbor(nodes["C"], 5)
nodes["A"].add_neighbor(nodes["D"], 5)
nodes["A"].add_neighbor(nodes["E"], 5)
nodes["A"].add_neighbor(nodes["F"], 5)
nodes["A"].add_neighbor(nodes["G"], 5)
nodes["A"].add_neighbor(nodes["H"], 5)
nodes["B"].add_neighbor(nodes["C"], 5)
nodes["B"].add_neighbor(nodes["D"], 5)
nodes["B"].add_neighbor(nodes["E"], 5)
nodes["C"].add_neighbor(nodes["F"], 5)
nodes["C"].add_neighbor(nodes["G"], 5)
nodes["D"].add_neighbor(nodes["E"], 5)
nodes["E"].add_neighbor(nodes["D"], 5)
nodes["E"].add_neighbor(nodes["G"], 5)
nodes["F"].add_neighbor(nodes["C"], 5)
nodes["F"].add_neighbor(nodes["H"], 5)
nodes["G"].add_neighbor(nodes["C"], 5)
nodes["G"].add_neighbor(nodes["E"], 5)
nodes["H"].add_neighbor(nodes["F"], 5)"""




graph = Graph()
graph.directed = True

for node in nodes.values():
    graph.add_node(node)

graph.get_rank("A")
graph.verif_poids()

"affiche infos sur les noeuds"
for i in graph.nodes:
    print(i.name)
    print(i.neighbors.keys())
    print(i.rang)
    print("\n")

"""
if graph.is_cyclic():
    print("The graph contains a cycle.")
else:
    print("The graph does not contain a cycle.")

# Draw the graph
graph.print_graph()
graph.draw()"""