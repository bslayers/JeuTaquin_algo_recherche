from algorithme_recherche.FilePile import FilePile
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.utile import *

def dfs_search(jeu: JeuTaquin, start_state: dict, final_state: dict, max_depth=100000):
    visited = set()
    stack = FilePile()
    stack.pushFirst((start_state, 0))
    
    start_key = key(start_state)
    visited.add(start_key)
    

    #parents = {start_key: None}

    while stack:
        popped_item = stack.pop()

        if popped_item is None:
            continue
        
        current_state, depth = popped_item
        
        #current_key = key(current_state)
        
        jeu.set_current_state(current_state)
        
        if current_state == final_state:
            print("État final trouvé!")
            #jeu.solution_path = reconstruct_path(parents, current_key)
            return

        if depth < max_depth:
            possible_moves = jeu.get_possible_moves()
            
            for next_state in possible_moves:
                next_key = key(next_state)
                if next_key not in visited:
                    visited.add(next_key)
                    #parents[next_key] = current_key
                    stack.pushFirst((next_state, depth + 1))

    jeu.display_state()
    print("État final non trouvé avec DFS!")