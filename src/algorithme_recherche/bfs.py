from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.FilePile import FilePile
from algorithme_recherche.utile import key, reconstruct_path

def bfs_search(jeu: JeuTaquin, start_state: dict, final_state: dict, 
               memory_limit=5000000, store_path: bool = False):
    """
    Breadth-First Search avec limite de mémoire optionnelle.
    
    Args:
        jeu: Instance de JeuTaquin
        start_state: État initial
        final_state: État final
        memory_limit: Limite de mémoire (nombre max d'états)
        store_path: Si True, stocke et retourne le chemin de la solution
    """
    visited = set()
    queue = FilePile(max_size=memory_limit)

    queue.pushLast(start_state)
    start_key = key(start_state)
    visited.add(start_key)
    
    # Initialiser parents comme un dict si store_path est True, sinon None
    parents: dict[str, str | None] | None = {start_key: None} if store_path else None

    while queue:
        current_state = queue.pop()
        if current_state is None:
            continue
            
        current_key = key(current_state)
        
        jeu.set_current_state(current_state)

        if current_state == final_state:
            if store_path and parents is not None:  # Vérification explicite
                jeu.solution_path = reconstruct_path(parents, current_key)
            return current_state

        possible_moves = jeu.get_possible_moves()
        
        for next_state in possible_moves:
            next_key = key(next_state)
            
            if next_key not in visited:
                visited.add(next_key)
                if store_path and parents is not None:  # Vérification explicite
                    parents[next_key] = current_key
                queue.pushLast(next_state)

    jeu.display_state()
    print("État final non trouvé avec BFS!")
    return None