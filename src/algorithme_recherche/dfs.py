from algorithme_recherche.FilePile import FilePile
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.utile import key, reconstruct_path

def dfs_search(jeu: JeuTaquin, start_state: dict, final_state: dict, 
               max_depth=100000, store_path: bool = False):
    """
    Depth-First Search avec profondeur maximale.
    
    Args:
        jeu: Instance de JeuTaquin
        start_state: État initial
        final_state: État final
        max_depth: Profondeur maximale de recherche
        store_path: Si True, stocke et retourne le chemin de la solution
    """
    visited = set()
    stack = FilePile()
    stack.pushFirst((start_state, 0))
    
    start_key = key(start_state)
    visited.add(start_key)
    
    # Initialiser parents comme un dict si store_path est True, sinon None
    parents: dict[str, str | None] | None = {start_key: None} if store_path else None

    while stack:
        popped_item = stack.pop()

        if popped_item is None:
            continue
        
        current_state, depth = popped_item
        current_key = key(current_state)
        
        jeu.set_current_state(current_state)
        
        if current_state == final_state:
            if store_path and parents is not None:  # Vérification explicite
                jeu.solution_path = reconstruct_path(parents, current_key)
            return current_state

        if depth < max_depth:
            possible_moves = jeu.get_possible_moves()
            
            for next_state in possible_moves:
                next_key = key(next_state)
                if next_key not in visited:
                    visited.add(next_key)
                    if store_path and parents is not None:  # Vérification explicite
                        parents[next_key] = current_key
                    stack.pushFirst((next_state, depth + 1))

    jeu.display_state()
    print("État final non trouvé avec DFS!")
    return None
