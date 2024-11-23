from jeu.jeuTaquin import JeuTaquin
import time
from algorithme_recherche.utile import reconstruct_path, key

def manhattan_distance(state: dict, k: int) -> int:
    """Calcule la distance de Manhattan pour un état."""
    distance = 0
    linear_conflicts = 0
    
    for value, (x, y) in state.items():
        if value != 0:
            target_i = (value - 1) // k
            target_j = (value - 1) % k
            # Distance de Manhattan de base
            distance += abs(x - target_i) + abs(y - target_j)
            
            # Détection des conflits linéaires (pièces sur la même ligne/colonne)
            for other_value, (other_x, other_y) in state.items():
                if other_value != 0 and value != other_value:
                    other_target_i = (other_value - 1) // k
                    other_target_j = (other_value - 1) % k
                    
                    # Conflit sur la même ligne
                    if x == other_x and target_i == other_target_i:
                        if (y < other_y and target_j > other_target_j) or \
                           (y > other_y and target_j < other_target_j):
                            linear_conflicts += 2
                    
                    # Conflit sur la même colonne
                    if y == other_y and target_j == other_target_j:
                        if (x < other_x and target_i > other_target_i) or \
                           (x > other_x and target_i < other_target_i):
                            linear_conflicts += 2
                            
    return distance + linear_conflicts

def state_to_tuple(state: dict) -> tuple:
    """Convertit un état en tuple immuable sans tri si l'ordre est garanti."""
    return tuple(state[i] for i in range(len(state)))

def astar_search(jeu: JeuTaquin, start_state: dict, final_state: dict, time_limit: float = 50.0, max_nodes: int = 1000000, store_path: bool = False):
    """
    A* avec limites de temps et de nœuds.
    
    Args:
        jeu: Instance de JeuTaquin
        start_state: État initial
        final_state: État final
        time_limit: Limite de temps en secondes (défaut: 50s)
        max_nodes: Nombre maximum de nœuds à explorer (défaut: 100000)
        store_path: Si True, stocke et retourne le chemin de la solution
    """
    start_time = time.time()
    nodes_explored = 0
    
    open_dict = {}
    closed_set = set()
    g_scores = {state_to_tuple(start_state): 0}
    
    initial_h = manhattan_distance(start_state, jeu.get_k())
    initial_state_key = state_to_tuple(start_state)
    open_dict[initial_h] = {initial_state_key: (start_state, 0, initial_h)}
    
    # Initialiser parents comme un dict si store_path est True, sinon None
    parents: dict[str, str | None] | None = {key(start_state): None} if store_path else None
    
    while open_dict:
        current_time = time.time()
        if current_time - start_time > time_limit:
            print(f"Limite de temps dépassée ({time_limit} secondes)")
            return None
            
        if nodes_explored >= max_nodes:
            print(f"Limite de nœuds dépassée ({max_nodes} nœuds)")
            return None
            
        min_f_score = min(open_dict.keys())
        state_entries = open_dict[min_f_score]
        
        current_key, (current_state, current_g, current_f) = state_entries.popitem()
        nodes_explored += 1
        
        if not state_entries:
            del open_dict[min_f_score]
        
        if current_state == final_state:
            if store_path and parents is not None:  # Vérification explicite
                jeu.solution_path = reconstruct_path(parents, key(current_state))
            #jeu.set_current_state(current_state)
            #jeu.display_state()
            return current_state
        
        closed_set.add(current_key)
        
        jeu.set_current_state(current_state)
        possible_moves = jeu.get_possible_moves()
        
        for next_state in possible_moves:
            next_key = state_to_tuple(next_state)
            tentative_g_score = current_g + 1
            
            next_h = manhattan_distance(next_state, jeu.get_k())
            next_f = tentative_g_score + next_h
            
            if next_key in closed_set:
                continue
            
            if next_key not in g_scores or tentative_g_score < g_scores[next_key]:
                g_scores[next_key] = tentative_g_score
                
                if store_path and parents is not None:  # Vérification explicite
                    parents[key(next_state)] = key(current_state)
                
                if next_f not in open_dict:
                    open_dict[next_f] = {}
                open_dict[next_f][next_key] = (next_state, tentative_g_score, next_f)
    
    print("Aucune solution trouvée dans les limites imposées")
    return None


