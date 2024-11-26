from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.FilePile import FilePile
from algorithme_recherche.utile import key, reconstruire_chemin

def bfs(jeu: JeuTaquin, etat_initial: dict, etat_final: dict, stocker_chemin: bool = False):
    """
    @brief Implémente l'algorithme de parcours en largeur
    @param jeu: Instance de la classe JeuTaquin
    @param etat_initial: État initial du puzzle
    @param etat_final: État final désiré
    @param stocker_chemin: Indique si le chemin de solution doit être stocké (défaut: False)
    @return: État final si trouvé, None sinon
    
    Explore systématiquement tous les états possibles niveau par niveau jusqu'à
    trouver l'état final ou épuiser tous les états possibles.
    """
    visites = set()
    file = FilePile()

    file.pushLast(etat_initial)
    cle_depart = key(etat_initial)
    visites.add(cle_depart)
    
    parents: dict[str, str | None] | None = {cle_depart: None} if stocker_chemin else None

    while file:
        etat_actuel = file.pop()
        if etat_actuel is None:
            continue
            
        cle_courante = key(etat_actuel)
        
        jeu.set_current_state(etat_actuel)

        if etat_actuel == etat_final:
            if stocker_chemin and parents is not None:
                jeu.solution_path = reconstruire_chemin(parents, cle_courante)
            return etat_actuel

        mouvements_possibles = jeu.get_possible_moves()
        
        for etat_suivant in mouvements_possibles:
            cle_suivante = key(etat_suivant)
            
            if cle_suivante not in visites:
                visites.add(cle_suivante)
                if stocker_chemin and parents is not None:
                    parents[cle_suivante] = cle_courante
                file.pushLast(etat_suivant)

    print("État final non trouvé avec bfs!")
    return None


