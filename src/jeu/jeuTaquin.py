import random

class JeuTaquin:
    
    def __init__(self, k: int):
        if k < 2:
            print("La taille du plateau doit être au moins 2x2")
        self.k = k
        self.current_state = None
        self.empty_pos = None
        self.solution_path = []
        
    def get_k(self) -> int:
        return self.k

    def generate_random_state(self) -> dict:
        """
        Génère un état initial aléatoire résolvable.
        
        Returns:
            dict: État initial aléatoire valide
        """
        positions = [(i, j) for i in range(self.k) for j in range(self.k)]
        random.shuffle(positions)

        state = {}
        for i in range(self.k * self.k):
            state[i] = positions[i]
        
        if not self.resolvable_grille(state):
            return self.generate_random_state()
            
        self.set_current_state(state)
        return state

    def set_current_state(self, state: dict) -> None:
        """
        Définit l'état actuel du jeu.
        """
        self.current_state = state
        self.empty_pos = state[0]

    def get_possible_moves(self) -> list:
        """Retourne les états obtenus après chaque mouvement possible."""
        moves = []
        i, j = self.empty_pos
        
        # Définition des mouvements possibles
        if i > 0:  # haut
            moves.append(self._create_new_state((i-1, j)))
        if i < self.k-1:  # bas
            moves.append(self._create_new_state((i+1, j)))
        if j > 0:  # gauche
            moves.append(self._create_new_state((i, j-1)))
        if j < self.k-1:  # droite
            moves.append(self._create_new_state((i, j+1)))
        
        return moves

    def _create_new_state(self, new_pos: tuple) -> dict:
        """
        Crée un nouvel état après déplacement de la case vide.
        """
        value = self.get_position_value(new_pos)
        new_state = dict(self.current_state)
        new_state[0] = new_pos
        new_state[value] = self.empty_pos
        return new_state
    
    def get_position_value(self, pos: tuple) -> int:
        """
        Retourne la valeur à une position donnée.
        
        Args:
            pos (tuple): Position à vérifier
            
        Returns:
            int: Valeur à la position donnée ou None si non trouvée
        """
        for value, position in self.current_state.items():
            if position == pos:
                return value
        return None

    def resolvable_grille(self, state: dict) -> bool:
        """
        Vérifie si la grille est résolvable en comptant le nombre d'inversions.
        Une grille est résolvable si:
        - Pour une grille de taille impaire: le nombre d'inversions est pair
        - Pour une grille de taille paire: la somme du nombre d'inversions et de la ligne 
        de la case vide (depuis le haut) est impaire
        
        Args:
            state (dict): État actuel de la grille
            
        Returns:
            bool: True si la grille est résolvable, False sinon
        """
        n = self.k * self.k
        count = 0
        
        # Crée un tableau ordonné par position
        values = [0] * (n-1)  # On exclut le 0
        idx = 0
        for i in range(self.k):
            for j in range(self.k):
                for val, pos in state.items():
                    if pos == (i,j) and val != 0:
                        values[idx] = val
                        idx += 1
                        break

        # Compte les inversions
        for i in range(n-2):  # n-1 éléments, donc n-2 pour l'index
            for j in range(i+1, n-1):
                if values[i] > values[j]:
                    count += 1

        if self.k % 2 == 1:
            return count % 2 == 0
        else:
            return (count + (self.k - state[0][0])) % 2 == 1

    def is_final_state(self, state=None) -> bool:
        """
        Vérifie si l'état est l'état final

        Returns:
            bool: True si l'état est final, False sinon
        """
        
        check_state = state if state is not None else self.current_state
        value = 1
        for i in range(self.k):
            for j in range(self.k):
                if value < self.k * self.k:
                    if check_state[value] != (i, j):
                        return False
                    value += 1
        return check_state[0] == (self.k - 1, self.k - 1)


    def moves(self, direction: str) -> bool:
        """
        Effectue un mouvement dans la direction donnée si possible.
        
        Args:
            direction (str): Direction du mouvement ('haut', 'bas', 'gauche', 'droite')
            
        Returns:
            bool: True si le mouvement a été effectué, False sinon
        """
        i, j = self.empty_pos
        new_pos = None
        
        if direction == 'haut' and i > 0:
            new_pos = (i - 1, j)
        elif direction == 'bas' and i < self.k - 1:
            new_pos = (i + 1, j)
        elif direction == 'gauche' and j > 0:
            new_pos = (i, j - 1)
        elif direction == 'droite' and j < self.k - 1:
            new_pos = (i, j + 1)
        
        if new_pos:
            value = self.get_position_value(new_pos)
            new_state = self.swap(self.current_state, self.empty_pos, new_pos, value)
            self.set_current_state(new_state)
            return True
        return False
    
    def swap(self, state: dict, pos1: tuple, pos2: tuple, value2: int) -> dict:
        new_state = dict(state)
        new_state[value2] = pos1
        new_state[0] = pos2
        return new_state
    
    def display_solution_path(self) -> None:
        """Affiche le chemin de la solution à partir du chemin enregistré dans solution_path."""
        if not self.solution_path:
            print("Aucun chemin de solution trouvé.")
            return
        print("Chemin de la solution:")
        for step_key in self.solution_path:
            print(step_key)

    def display_state(self) -> None:
        for i in range(self.k):
            for j in range(self.k):
                value = self.get_position_value((i, j))
                print(f'{value}', end=' ' if j != self.k - 1 else '\n')
        
    def jeu(self):
        while not self.is_final_state(self.current_state):
            self.display_state()
            print("Mouvements possibles : haut, bas, gauche, droite")
            direction = input("Entrez la direction de mouvement : ").strip().lower()
            if direction in ['haut', 'bas', 'gauche', 'droite']:
                if not self.moves(direction):
                    print("Déplacement non valide.")
            else:
                print("Direction invalide.")
        print("Félicitations, vous avez résolu le puzzle !")

