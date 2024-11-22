from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.FilePile import FilePile
from algorithme_recherche.utile import *

def bfs_search(jeu: JeuTaquin, start_state: dict, final_state: dict, memory_limit=5000000):
    visited = set()
    queue = FilePile(max_size=memory_limit)

    queue.pushLast(start_state)
    start_key = key(start_state)
    visited.add(start_key)
    
    #parents = {start_key: None}

    while queue:
        current_state = queue.pop()
        if current_state is None:
            continue
        #current_key = key(current_state)
        
        jeu.set_current_state(current_state)

        if current_state == final_state:
            print("État final trouvé!")
            #jeu.solution_path = reconstruct_path(parents, current_key)
            return

        possible_moves = jeu.get_possible_moves()
        
        for next_state in possible_moves:
            next_key = key(next_state)
            
            if next_key not in visited:
                visited.add(next_key)
                #parents[next_key] = current_key
                queue.pushLast(next_state)

    jeu.display_state()
    print("État final non trouvé avec BFS!")






