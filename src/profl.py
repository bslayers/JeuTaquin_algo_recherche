import cProfile
import pstats
import os
from datetime import datetime
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.astar import astar_search
from algorithme_recherche.bfs import bfs_search
from algorithme_recherche.dfs import dfs_search

def run_astar_test(size):
    jeu = JeuTaquin(size)
    initial_state = jeu.generate_random_state()
    final_state = jeu.final_positions  # Utiliser la grille finale attendue pour la taille donnée

    print(f"Profiling A* pour une grille {size}x{size}...")
    astar_search(jeu, initial_state, final_state)

def run_profiling():
    grid_sizes = [3]  # Vous pouvez ajuster la taille de la grille ici
    for size in grid_sizes:
        # Profiling de l'algorithme A* pour la taille de grille spécifiée
        profiler = cProfile.Profile()
        profiler.enable()

        run_astar_test(size)

        profiler.disable()
        
        # Générer un fichier de profil pour analyse future
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        profile_file = f'profiling_astar_{size}x{size}_{timestamp}.prof'
        profiler.dump_stats(profile_file)
        
        print(f"Profiling terminé pour la grille {size}x{size}. Résultats sauvegardés dans {profile_file}")
        
        # Afficher les statistiques
        stats = pstats.Stats(profiler)
        stats.strip_dirs()
        stats.sort_stats('cumtime')
        stats.print_stats(20)  # Afficher les 20 premières fonctions les plus coûteuses

if __name__ == "__main__":
    run_profiling()
    
