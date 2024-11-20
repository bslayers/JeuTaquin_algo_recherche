class Element:
    def __init__(self, state, g_score, f_score):
        self.precedent = None
        self.prochain = None
        self.state = state        # L'état du jeu
        self.g_score = g_score    # Coût du chemin depuis le début
        self.f_score = f_score    # Score total (g_score + heuristique)

class FilePileAstar:
    def __init__(self, max_size=None):
        self.start = None
        self.end = None
        self.size = 0
        self.max_size = max_size

    def pop(self):
        """Retire et retourne l'état avec le plus petit f_score"""
        if not self.start:
            return None
            
        # Trouve l'élément avec le plus petit f_score
        min_element = self.start
        current = self.start
        min_f_score = float('inf')
        
        while current:
            if current.f_score < min_f_score:
                min_f_score = current.f_score
                min_element = current
            current = current.prochain
            
        # Retire l'élément trouvé
        if min_element.precedent:
            min_element.precedent.prochain = min_element.prochain
        else:
            self.start = min_element.prochain
            
        if min_element.prochain:
            min_element.prochain.precedent = min_element.precedent
        else:
            self.end = min_element.precedent
            
        self.size -= 1
        return min_element.state, min_element.g_score

    def push(self, state, g_score, f_score):
        """Ajoute un nouvel état avec ses scores"""
        elt = Element(state, g_score, f_score)
        if self.start is None:
            self.start = elt
            self.end = elt
        else:
            self.end.prochain = elt
            elt.precedent = self.end
            self.end = elt
        self.size += 1
        
        # Respecte la limite de mémoire si spécifiée
        while self.max_size and self.size > self.max_size:
            print("Déchargement d'un élément pour respecter la limite de mémoire")
            self.pop()

    def __bool__(self):
        return self.start is not None

    def __len__(self):
        return self.size