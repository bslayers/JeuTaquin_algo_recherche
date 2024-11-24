import cProfile
import pstats
import os
from datetime import datetime
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.astar import astar
from algorithme_recherche.bfs import bfs
from algorithme_recherche.dfs import dfs

def run_astar_test(size):
    jeu = JeuTaquin(size)
    initial_state = jeu.generate_random_state()
    final_state = jeu.final_positions  # Utiliser la grille finale attendue pour la taille donnée

    print(f"Profiling A* pour une grille {size}x{size}...")
    
    # Profilage en temps réel
    profiler = cProfile.Profile()
    profiler.enable()

    # Ajoute un check périodique pour afficher les stats pendant l'exécution
    try:
        astar(jeu, initial_state, final_state)
    except KeyboardInterrupt:
        print("Profiling interrompu.")
    
    profiler.disable()
    
    # Générer un fichier de profil pour analyse future
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    profile_file = f'profiling_astar_{size}x{size}_{timestamp}.prof'
    profiler.dump_stats(profile_file)
    
    print(f"Profiling terminé pour la grille {size}x{size}. Résultats sauvegardés dans {profile_file}")
    
    # Afficher les statistiques en temps réel
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('ncalls')  # Trier par nombre d'appels (du plus appelé au moins appelé)
    stats.print_stats(50)  # Afficher les 50 premières fonctions les plus appelées

def run_profiling():
    grid_sizes = [3,4]  # Vous pouvez ajuster la taille de la grille ici
    for size in grid_sizes:
        # Profiling de l'algorithme A* pour la taille de grille spécifiée
        try:
            run_astar_test(size)
        except KeyboardInterrupt:
            print("Profiling a été interrompu par l'utilisateur.")
            break

if __name__ == "__main__":
    run_profiling()
