class Element:
    def __init__(self, contenu):
        self.precedent: 'Element | None' = None 
        self.prochain: 'Element | None' = None 
        self.contenu = contenu

class FilePile:
    def __init__(self, max_size=None):
        self.start: 'Element | None' = None
        self.end: 'Element | None' = None 
        self.size = 0
        self.max_size = max_size
        self.batch_removal_threshold = 10

    def pop(self):
        """Supprime et retourne le premier élément."""
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
        """Ajoute un élément à la fin de la file/pile."""
        elt = Element(contenu)
        if not self.start:
            self.start = elt
            self.end = elt
        else:

            if self.end is not None:
                self.end.prochain = elt 
                elt.precedent = self.end
            self.end = elt

        self.size += 1

        if self.max_size and self.size > self.max_size:
            self._batch_remove_oldest()

    def pushFirst(self, contenu):
        """Ajoute un élément au début de la file/pile."""
        elt = Element(contenu)
        if not self.start:
            self.start = elt
            self.end = elt
        else:

            elt.prochain = self.start
            if self.start is not None:
                self.start.precedent = elt
            self.start = elt 
        
        self.size += 1

        if self.max_size and self.size > self.max_size:
            self._batch_remove_oldest()

    def _batch_remove_oldest(self):
        """Supprime plusieurs éléments pour respecter la limite de taille."""
        if self.max_size is None:
            return  # Si max_size est None, ne rien faire

        # Assurer que max_size est un entier pour le calcul
        removal_count = min(max(self.size - (self.max_size or 0), 0), self.batch_removal_threshold)
        
        for _ in range(removal_count):
            self.pop()


    def __bool__(self): 
        return self.start is not None

    def __len__(self):
        return self.size
