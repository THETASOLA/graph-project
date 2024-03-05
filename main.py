from showGraph import generateGraph, drawGraph

testG = [{"A": ["B", "C", "D", "E", "F", "G", "H"]}, 
         {"B": ["A", "C", "D", "E"]}, 
         {"C": ["A", "B", "F", "G"]},
         {"D": ["A", "B", "E"]},
         {"E": ["A", "B", "D", "G"]},
         {"F": ["A", "C", "H"]},
         {"G": ["A", "C", "E"]},
         {"H": ["A", "F"]}]

generateGraph(testG)
drawGraph(testG, True)