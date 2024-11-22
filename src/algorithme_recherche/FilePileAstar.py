class FilePileAstar:
    def __init__(self):
        self.elements = []  # Liste pour stocker les éléments triés

    def pop(self):
        """Retourne et supprime l'état avec le f_score le plus bas."""
        if not self.elements:
            return None
        # Extraire et supprimer le premier élément (le plus petit f_score)
        return self.elements.pop(0)

    def push(self, state, g_score, f_score):
        """Ajoute un nouvel état avec ses scores en maintenant la liste triée."""
        elt = (state, g_score, f_score)
        # Insertion triée pour maintenir la liste par ordre de f_score
        index = 0
        while index < len(self.elements) and self.elements[index][2] <= f_score:
            index += 1
        self.elements.insert(index, elt)

    def __bool__(self):
        return bool(self.elements)

    def __len__(self):
        return len(self.elements)
