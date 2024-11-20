from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.FilePileAstar import FilePileAstar
from algorithme_recherche.utile import *

def manhattan_distance(state: dict, k: int) -> int:
    """Calcule la distance de Manhattan pour un état"""
    distance = 0
    for value in range(1, k * k):
        current_pos = state[value]
        target_i = (value - 1) // k
        target_j = (value - 1) % k
        distance += abs(current_pos[0] - target_i) + abs(current_pos[1] - target_j)
    return distance


def astar_search(jeu: JeuTaquin, start_state: dict, memory_limit=5000000) -> None:

    visited = set()
    queue = FilePileAstar(max_size=memory_limit)

    h_score = manhattan_distance(start_state, jeu.get_k())
    g_score = 0 
    f_score = g_score + h_score

    queue.push(start_state, g_score, f_score)
    start_key = key(start_state)
    visited.add(start_key)

    #parents = {start_key: None}

    while queue:

        current_state, current_g = queue.pop()
        current_key = key(current_state)
        jeu.set_current_state(current_state)

        if jeu.is_final_state(current_state):
            print("État final trouvé!")

            #jeu.solution_path = reconstruct_path(parents, current_key)
            return

        for next_state in jeu.get_possible_moves():
            next_key = key(next_state)
            
            if next_key not in visited:

                next_g = current_g + 1 
                next_h = manhattan_distance(next_state, jeu.get_k())
                next_f = next_g + next_h

                visited.add(next_key)
                #parents[next_key] = current_key
                queue.push(next_state, next_g, next_f)
    
    print("État final non trouvé!")
    
