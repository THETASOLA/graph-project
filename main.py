from showGraph import generateGraph, drawGraph

testG = [{"A": ["B", "C", "D", "E", "F", "G", "H"]}, 
         {"B": ["C", "D", "E"]}, 
         {"C": ["F", "G"]},
         {"D": ["E"]},
         {"E": ["D", "G"]},
         {"F": ["C", "H"]},
         {"G": ["C", "E"]},
         {"H": ["F"]}]

generateGraph(testG)
drawGraph(testG, True)