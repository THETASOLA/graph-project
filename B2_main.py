from B2_graphClass import Node, Graph
from B2_file_function import graph_initialization, input_file, traces_execution
import os

# ------------------------- Reading file and start of the program -------------------------
traces_execution()
os.system('cls')
num_file = input_file()
nodes, graph, start_node, end_node = graph_initialization(num_file)

# ------------------------- Start of user interface -------------------------
while True:
    print("\nChoisissez une option :")
    print("1. Afficher le graphe")
    print("2. Vérifier si le graphe est cyclique")
    print("3. Vérifier si le graphe contient des poids négatifs")
    print(f"4. Afficher les chemins de {start_node.name} à {end_node.name}")
    print("5. Obtenir les rangs des sommets")
    print("6. Dessiner le graphe")
    print("7. Changer de table de contrainte")
    print("8. Quitter")

    choice = input("Entrez le numéro de l'option choisie : ")

    if choice == "1":
        graph.print_graph()
    elif choice == "2":
        if graph.is_cyclic():
            print("\nLe graphe est cyclique")
        else:
            print("\nLe graphe n'est pas cyclique")
    elif choice == "3":
        if graph.verif_poids():
            print("\nIl n'y a pas de poids négatif")
        else:
            print("\nIl y a un poids négatif")

    elif choice == "4":
        #graph.display_paths(start_node, end_node)

        if graph.is_cyclic():
            print("\nLe graphe est cyclique impossible !")
        else : 
            if not graph.verif_rank():
                graph.get_rank()
             #graph.display_paths(start_node, end_node)
            task_ranks_earliest, tasks_earliest, task_predecessors, task_successors, task_paths, task_path_weights, task_earliest_dates, max_earliest_date = graph.earliest_dates()
            task_ranks_latest, tasks_latest, task_successors, task_weights, task_latest_dates = graph.latest_date(max_earliest_date)
            graph.date_table(task_ranks_earliest, task_earliest_dates, task_ranks_latest, task_latest_dates)
            
        
    elif choice == "5":
        print("\n", end="")
        graph.get_rank()
    elif choice == "6":
        graph.draw()
    elif choice == "7":
        os.system('cls')
        num_file = input_file()
        nodes, graph, start_node, end_node = graph_initialization(num_file)

    elif choice == "8":
        break
    else:
        print("Option invalide. Veuillez réessayer.")
