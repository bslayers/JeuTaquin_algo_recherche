class Element:
    """
    @brief Classe représentant un élément dans la structure de données FilePile
    
    Chaque élément contient un contenu et des références vers les éléments précédent et suivant.
    """
    def __init__(self, contenu):
        self.precedent: 'Element | None' = None
        self.prochain: 'Element | None' = None
        self.contenu = contenu

class FilePile:
    """
    @brief Structure de données hybride pouvant fonctionner comme une file ou une pile
    """
    def __init__(self):
        self.start: 'Element | None' = None
        self.end: 'Element | None' = None
        self.size = 0

    def pop(self):
        """Supprime et retourne l'élément au début de la file/pile."""
        if not self.start:
            return None

        contenu = self.start.contenu
        self.start = self.start.prochain

        if self.start is None:
            self.end = None
        else:
            self.start.precedent = None

        self.size -= 1
        return contenu

    def pushLast(self, contenu):
        """
        @brief Ajoute un élément à la fin de la structure
        @param contenu: L'élément à ajouter
        """
        elt = Element(contenu)
        
        if self.end is None: 
            self.start = elt
            self.end = elt
        else:
            self.end.prochain = elt
            elt.precedent = self.end
            self.end = elt
        
        self.size += 1

    def pushFirst(self, contenu):
        """
        @brief Ajoute un élément au début de la structure
        @param contenu: L'élément à ajouter
        """
        elt = Element(contenu)
        
        if self.start is None:
            self.start = elt
            self.end = elt
        else:
            elt.prochain = self.start
            self.start.precedent = elt
            self.start = elt 
        self.size += 1

    def __bool__(self):
        """Retourne True si la file/pile n'est pas vide, sinon False."""
        return self.start is not None

    def __len__(self):
        """Retourne la taille de la file/pile."""
        return self.size
