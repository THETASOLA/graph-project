from graphClass import Node, Graph
from file_function import graph_initialization, input_file
import os

# ------------------------- Reading file and start of the program -------------------------
os.system('cls')
num_file = input_file()
graph, start_node, end_node = graph_initialization(num_file)
# TODO : vider la mémoire des instances quand on change de graphe

# ------------------------- Start of user interface -------------------------
while True:
    print("\nChoisissez une option :")
    print("1. Afficher le graphe")
    print("2. Vérifier si le graphe est cyclique")
    print("3. Vérifier si le graphe contient des poids négatifs")
    print("4. Afficher les chemins de A à J")
    print("5. Dessiner le graphe")
    print("6. Changer de table de contrainte")
    print("7. Quitter")

    choice = input("Entrez le numéro de l'option choisie : ")

    if choice == "1":
        graph.print_graph()
    elif choice == "2":
        if graph.is_cyclic():
            print("Le graphe est cyclique")
        else:
            print("Le graphe n'est pas cyclique")
    elif choice == "3":
        if graph.verif_poids():
            print("Il n'y a pas de poids négatif")
        else:
            print("Il y a un poids négatif")
    elif choice == "4":
        graph.display_paths(start_node, end_node)
    elif choice == "5":
        graph.draw()
    elif choice == "6":
        os.system('cls')
        num_file = input_file()
        graph, start_node, end_node = graph_initialization(num_file)
    elif choice == "7":
        break
    else:
        print("Option invalide. Veuillez réessayer.")
