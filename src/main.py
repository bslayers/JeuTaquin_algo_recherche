import sys
import time
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.astar import astar
from algorithme_recherche.bfs import bfs
from algorithme_recherche.dfs import dfs

def calculate_final_state(k: int) -> dict:
    """Calcule l'état final pour une grille de taille k."""
    final_state = {i: ((i-1)//k, (i-1)%k) for i in range(1, k*k)}
    final_state[0] = (k-1, k-1)
    return final_state

def main():
    try:
        k = int(input("Entrez la taille de la grille (k x k): "))
        if k < 2:
            raise ValueError("La taille de la grille doit être d'au moins 2.")
        
        print("Sélectionnez la stratégie de recherche:")
        print("1. A* Search (entrez 'astar' ou 'a')")
        print("2. Breadth-First Search (entrez 'bfs' ou 'b')")
        print("3. Depth-First Search (entrez 'dfs' ou 'd')")
        print("4. Jeu humain (entrez 'h')")
        strategy = input("Entrez la stratégie de recherche (astar/bfs/dfs/h): ").strip().lower()

        if strategy not in ['astar', 'bfs', 'dfs', 'h', 'a', 'b', 'd']:
            print("Stratégie invalide sélectionnée.")
            sys.exit(1)

        show_path = input("Voulez-vous voir le chemin de la solution de la grille? (o/n): ").strip().lower()
        stocker_chemin = show_path in ['o', 'oui', 'y', 'yes']

    except ValueError as e:
        print(f"Erreur: {e}")
        sys.exit(1)

    jeu = JeuTaquin(k)

    initial_state = jeu.generate_random_state()
    jeu.set_current_state(initial_state)

    final_state = calculate_final_state(k)

    print("\nÉtat initial:")
    jeu.afficher_etat()
    print("\nÉtat final attendu:")
    jeu.display_final_grid()
    print()

    if strategy != 'h':
        start_time = time.time()
        result = None
        
        if strategy in ['bfs', 'b']:
            print("Lancement de la recherche BFS:")
            result = bfs(jeu, initial_state, final_state, stocker_chemin=stocker_chemin)
        elif strategy in ['astar', 'a']:
            print("Lancement de la recherche A*:")
            result = astar(jeu, initial_state, final_state, stocker_chemin=stocker_chemin)
        elif strategy in ['dfs', 'd']:
            print("Lancement de la recherche DFS:")
            result = dfs(jeu, initial_state, final_state, stocker_chemin=stocker_chemin)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\nTemps d'exécution: {execution_time:.12f} secondes")

        if result:
            print("\nSolution trouvée!")
            print("\nÉtat final atteint:")
            jeu.set_current_state(result)
            jeu.afficher_etat()
            
            if stocker_chemin and jeu.solution_path:
                if show_path in ['o', 'oui', 'y', 'yes']:
                    jeu.afficher_chemin_solution()
        else:
            print("\nAucune solution trouvée.")
    else:
        print("Mode de jeu normal selectionné. Utilisez h/b/g/d pour déplacer la case vide.")
        jeu.jeu()

if __name__ == "__main__":
    main()