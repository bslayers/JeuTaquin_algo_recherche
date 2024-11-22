from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.FilePileAstar import FilePileAstar
from algorithme_recherche.utile import *

def manhattan_distance(state: dict, k: int) -> int:
    """Calcule la distance de Manhattan pour un état."""
    distance = 0
    for value, (x, y) in state.items():
        if value != 0:
            target_i = (value - 1) // k
            target_j = (value - 1) % k
            distance += abs(x - target_i) + abs(y - target_j)
    return distance

def astar_search(jeu: JeuTaquin, start_state: dict, final_state: dict):
    
    queue = FilePileAstar()
    visited = set()
    #parents = {}
    g_scores = {state_to_key(start_state): 0}
    
    h_score = manhattan_distance(start_state, jeu.get_k())
    g_score = 0
    f_score = g_score + h_score
    
    queue.push(start_state, g_score, f_score)
    visited.add(state_to_key(start_state))
    #parents[state_to_key(start_state)] = None
    
    expanded_nodes = 0
    
    while queue:
        popped = queue.pop()
        if not popped:
            continue
        
        current_state, current_g, current_f = popped
        current_key = state_to_key(current_state)
        
        # Vérifier si c'est l'état final
        if current_state == final_state:
            print("Etat final trouvé:")
            jeu.set_current_state(current_state)
            jeu.display_state()
            jeu.display_final_grid()
            return current_state
        
        jeu.set_current_state(current_state)
        
        expanded_nodes += 1
        
        for next_state in jeu.get_possible_moves():
            next_key = state_to_key(next_state)
            
            # Éviter de revisiter des états déjà explorés
            if next_key in visited:
                continue
            
            tentative_g_score = current_g + 1
            
            # Mettre à jour les scores si nouveau chemin plus court
            if next_key not in g_scores or tentative_g_score < g_scores[next_key]:
                #parents[next_key] = current_key
                g_scores[next_key] = tentative_g_score
                next_h = manhattan_distance(next_state, jeu.get_k())
                next_f = tentative_g_score + next_h
                
                visited.add(next_key)
                queue.push(next_state, tentative_g_score, next_f)
    
    print("Aucune solution trouvée")
    return None

