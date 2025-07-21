
def key(state: dict) -> str:
    """
    @brief Génère une clé unique pour un état
    @param state: Dictionnaire représentant un état du jeu
    @return: Chaîne de caractères unique représentant l'état
    
    Convertit un état en une chaîne de caractères unique pour
    l'utiliser comme clé de dictionnaire ou dans un ensemble.
    """
    return ''.join(str(state[value]) for value in range(len(state)))

def reconstruire_chemin(parents: dict, end_key: str) -> list:
    """
    @brief Reconstruit le chemin de la solution à partir du dictionnaire des parents
    @param parents: Dictionnaire associant à chaque état son parent
    @param end_key: Clé de l'état final
    @return: Liste des états formant le chemin de la solution
    
    Utilise le dictionnaire des parents pour reconstruire le chemin
    de l'état initial à l'état final.
    """
    path = []
    while end_key is not None:
        path.append(end_key)
        end_key = parents[end_key]
    path.reverse()
    return path
