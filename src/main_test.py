from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.bfs import bfs_search
import time

if __name__ == "__main__":
    k = int(input("Entrez la taille du plateau (k x k) : "))
    who = int(input("Entrez 0 pour l'algorithme ou 1 pour joueur : "))
    memory_limit = 22_000_000  
    jeu = JeuTaquin(k)
    start_state = jeu.generate_random_state()

    print("État initial :")
    jeu.display_state()
    print()
    if who == 0:
        start_time = time.time()  # Temps avant l'exécution du BFS
        bfs_search(jeu, start_state,memory_limit)
        end_time = time.time()  # Temps après l'exécution du BFS
        print(f"Temps d'exécution du BFS : {end_time - start_time:.4f} secondes")
    else:
        jeu.jeu()