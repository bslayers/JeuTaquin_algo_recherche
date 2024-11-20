import sys
import time
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.astar import astar_search
from algorithme_recherche.bfs import bfs_search
from algorithme_recherche.dfs import dfs_search

def main():
    try:
        # Demander la taille de la grille
        k = int(input("Entrez la taille de la grille (k x k): "))
        if k < 2:
            raise ValueError("La taille de la grille doit être d'au moins 2.")
        
        print("Sélectionnez la stratégie de recherche:")
        print("1. A* Search (entrez 'astar')")
        print("2. Breadth-First Search (entrez 'bfs')")
        print("3. Depth-First Search (entrez 'dfs')")
        print("4. Jeu humain (entrez 'h')")
        strategy = input("Entrez la stratégie de recherche (astar/bfs/dfs/h): ").strip().lower()

        if strategy not in ['astar', 'bfs', 'dfs', 'h','a','b','d']:
            print("Stratégie invalide sélectionnée.")
            sys.exit(1)

    except ValueError as e:
        print(f"Erreur: {e}")
        sys.exit(1)

    # Initialiser le jeu
    jeu = JeuTaquin(k)  # Jeu avec taille k

    # Générer un état initial aléatoire
    initial_state = jeu.generate_random_state()
    jeu.set_current_state(initial_state)

    # Sélectionner l'algorithme de recherche en fonction du choix de l'utilisateur
    if strategy != 'h':
        start_time = time.time()  # Démarrer le chronomètre
        
        if strategy == 'bfs'or strategy == 'b':
            print("Lancement de la recherche BFS...")
            result_path = bfs_search(jeu, initial_state)  # Utilisation de bfs_search avec état initial
        elif strategy == 'astar' or strategy == 'a':
            print("Lancement de la recherche A*...")
            result_path = astar_search(jeu, initial_state)  # Utilisation de astar_search avec état initial
        elif strategy == 'dfs' or strategy == 'd':
            print("Lancement de la recherche DFS...")
            result_path = dfs_search(jeu, initial_state)  # Utilisation de dfs_search avec état initial
        
        end_time = time.time()  # Arrêter le chronomètre
        
        # Afficher le temps d'exécution
        print(f"\nTemps d'exécution: {end_time - start_time:.3f} secondes")

        # Afficher les résultats
        if result_path:
            print("\nSolution trouvée!")
        else:
            print("\nAucune solution trouvée.")
    else:
        # Si l'utilisateur choisit de jouer manuellement
        print("Vous avez choisi de jouer le jeu manuellement.")
        jeu.jeu()  # Lancer la méthode de jeu pour l'utilisateur

if __name__ == "__main__":
    main()
