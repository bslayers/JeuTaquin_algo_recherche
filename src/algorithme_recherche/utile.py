
def key(state: dict) -> str:
    """Génère une clé unique pour un état donné sous forme de chaîne de caractères."""
    return ''.join(str(state[value]) for value in range(len(state)))

def state_to_key(state: dict) -> tuple:
    """Convertit un état en tuple pour un hachage efficace"""
    key = ''.join(f"{val}:{pos[0]},{pos[1]};" for val, pos in sorted(state.items()))
    return key

def reconstruct_path(parents: dict, end_key: str) -> list:
    """Reconstruit le chemin de l'état initial à l'état final."""
    path = []
    while end_key is not None:
        path.append(end_key)
        end_key = parents[end_key]
    path.reverse()
    return path