
def key(state: dict) -> str:
    """Génère une clé unique pour un état donné sous forme de chaîne de caractères."""
    return ''.join(str(state[value]) for value in range(len(state)))

def reconstruct_path(parents: dict, end_key: str) -> list:
    """Reconstruit le chemin de l'état initial à l'état final."""
    path = []
    while end_key is not None:
        path.append(end_key)
        end_key = parents[end_key]
    path.reverse()
    return path