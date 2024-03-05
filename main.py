from showGraph import generateGraph, drawGraph
from dataValidator import is_cyclic

testG = {
    "A": ["B", "C", "D", "E", "F", "G", "H"],
    "B": ["C", "D", "E"],
    "C": ["F", "G"],
    "D": ["E"],
    "E": ["D", "G"],
    "F": ["C", "H"],
    "G": ["C", "E"],
    "H": ["F"]
}

generateGraph(testG)
print("Is cyclic; ",is_cyclic(testG))
#drawGraph(testG, True)