import pstats

# Charger le fichier de profil généré
profile_file = 'profiling_astar_3x3_20241122_181800.prof'
p = pstats.Stats(profile_file)

# Trier et afficher les résultats
p.strip_dirs()
p.sort_stats('cumtime')  # Trier par temps cumulé
p.print_stats(20)         # Afficher les 20 premières lignes
