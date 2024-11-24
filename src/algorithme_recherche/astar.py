from jeu.jeuTaquin import JeuTaquin
import time
from algorithme_recherche.utile import reconstruire_chemin, key

def manhattan_distance(state: dict, k: int) -> int:
    """
    @brief Calcule la distance de Manhattan pour un état donné
    @param state: Dictionnaire représentant l'état actuel du puzzle
    @param k: Dimension du puzzle (k x k)
    @return: La distance de Manhattan totale
    
    Calcule la somme des distances de Manhattan de chaque tuile à sa position cible,
    en ajoutant une pénalité de 1 si une tuile n'est pas à sa place finale.
    """
    distance = 0
    for value, (x, y) in state.items():
        if value != 0:
            target_i = (value - 1) // k
            target_j = (value - 1) % k
            distance += abs(x - target_i) + abs(y - target_j)
            
            if (x, y) != (target_i, target_j):
                distance += 1
                
    return distance

def etat_vers_tuple(etat: dict) -> tuple:
    """
    @brief Convertit un état du jeu en tuple
    @param etat: Dictionnaire représentant l'état du jeu
    @return: Tuple représentant l'état du jeu
    
    Convertit un dictionnaire d'état en tuple pour permettre son utilisation comme clé de dictionnaire.
    """
    return tuple(etat[i] for i in range(len(etat)))

def astar(jeu: JeuTaquin, etat_initial: dict, etat_final: dict, limite_temps: float = 40.0, max_noeuds: int = 100000, stocker_chemin: bool = False):
    """
    @brief Implémente l'algorithme A* pour résoudre le jeu de taquin
    @param jeu: Instance de la classe JeuTaquin
    @param etat_initial: État initial du puzzle
    @param etat_final: État final désiré
    @param limite_temps: Temps maximum d'exécution en secondes (défaut: 40.0)
    @param max_noeuds: Nombre maximum de nœuds à explorer par itération (défaut: 100000)
    @param stocker_chemin: Indique si le chemin de solution doit être stocké (défaut: False)
    @return: État final si trouvé, None sinon
    
    Utilise l'algorithme A* avec une heuristique de distance de Manhattan pour trouver
    le chemin optimal de l'état initial à l'état final. Inclut des mécanismes de
    gestion de la mémoire et du temps d'exécution.
    """
    temps_debut = time.time()
    noeuds_explores = 0
    max_noeuds_dynamique = max_noeuds
    branches_a_explorer = [] 
    
    etats_a_explorer = {}
    visites = set()  
    couts_g = {etat_vers_tuple(etat_initial): 0}
    
    h_initial = manhattan_distance(etat_initial, jeu.get_k())
    cle_etat_initiale = etat_vers_tuple(etat_initial)
    etats_a_explorer[h_initial] = {cle_etat_initiale: (etat_initial, 0, h_initial)}
    
    parent_states: dict[str, str | None] = {key(etat_initial): None} if stocker_chemin else {}

    while etats_a_explorer:
        temps_actuel = time.time()
        temps_ecoule = temps_actuel - temps_debut
        
        if temps_ecoule > limite_temps:
            print(f"Limite de temps dépassée ({limite_temps} secondes)")
            return None
        
        if noeuds_explores >= max_noeuds_dynamique:
            branches_a_explorer.append((etats_a_explorer, visites, couts_g, parent_states))
            
            if branches_a_explorer:
                etats_a_explorer, visites, couts_g, parent_states = branches_a_explorer.pop(0)
                max_noeuds_dynamique += int(max_noeuds_dynamique * 0.15)
            noeuds_explores = 0
            continue
        
        score_f_min = min(etats_a_explorer.keys())
        etats_possibles = etats_a_explorer[score_f_min] 
        
        cle_courante, (etat_courant, g_courant, f_courant) = etats_possibles.popitem()
        noeuds_explores += 1
        
        if not etats_possibles:
            del etats_a_explorer[score_f_min]
        
        if etat_courant == etat_final:
            if stocker_chemin:
                jeu.solution_path = reconstruire_chemin(parent_states, key(etat_courant))
            return etat_courant
        
        visites.add(cle_courante)
        
        jeu.set_current_state(etat_courant)
        mouvements_possibles = jeu.get_possible_moves()
        
        for etat_suivant in mouvements_possibles:
            cle_suivante = etat_vers_tuple(etat_suivant)
            new_g_score = g_courant + 1 
            
            h_suivant = manhattan_distance(etat_suivant, jeu.get_k())
            f_suivant = new_g_score + h_suivant
            
            if cle_suivante in visites:
                continue
            
            if cle_suivante not in couts_g or new_g_score < couts_g[cle_suivante]:
                couts_g[cle_suivante] = new_g_score
                
                if stocker_chemin:
                    parent_states[key(etat_suivant)] = key(etat_courant)
                
                if f_suivant not in etats_a_explorer:
                    etats_a_explorer[f_suivant] = {}
                etats_a_explorer[f_suivant][cle_suivante] = (etat_suivant, new_g_score, f_suivant)
    
    print("Aucune solution trouvée dans les limites imposées avec A*")
    return None



