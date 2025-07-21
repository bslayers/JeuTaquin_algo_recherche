from algorithme_recherche.FilePile import FilePile
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.utile import key, reconstruire_chemin

def dfs(jeu: JeuTaquin, etat_initial: dict, etat_final: dict, prof_max=100000, stocker_chemin: bool = False):
    """
    @brief Implémente l'algorithme de parcours en profondeur
    @param jeu: Instance de la classe JeuTaquin
    @param etat_initial: État initial du puzzle
    @param etat_final: État final désiré
    @param prof_max: Profondeur maximale de recherche (défaut: 100000)
    @param stocker_chemin: Indique si le chemin de solution doit être stocké (défaut: False)
    @return: État final si trouvé, None sinon
    
    Explore les états en profondeur d'abord jusqu'à une profondeur maximale donnée.
    """
    visites = set()
    pile = FilePile()
    pile.pushFirst((etat_initial, 0))
    
    cle_depart = key(etat_initial)
    visites.add(cle_depart)
    
    parents: dict[str, str | None] | None = {cle_depart: None} if stocker_chemin else None

    while pile:
        element_retire = pile.pop()

        if element_retire is None:
            continue
        
        etat_actuel, profondeur = element_retire
        cle_courante = key(etat_actuel)
        
        jeu.set_current_state(etat_actuel)
        
        if etat_actuel == etat_final:
            if stocker_chemin and parents is not None:
                jeu.solution_path = reconstruire_chemin(parents, cle_courante)
            return etat_actuel

        if profondeur < prof_max:
            mouvements_possibles = jeu.get_possible_moves()
            
            for etat_suivant in mouvements_possibles:
                cle_suivante = key(etat_suivant)
                if cle_suivante not in visites:
                    visites.add(cle_suivante)
                    if stocker_chemin and parents is not None:
                        parents[cle_suivante] = cle_courante
                    pile.pushFirst((etat_suivant, profondeur + 1))

    print("État final non trouvé avec dfs!")
    return None