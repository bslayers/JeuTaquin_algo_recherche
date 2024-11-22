import random

class JeuTaquin:
    
    def __init__(self, k: int):
        if k < 2:
            print("La taille du plateau doit être au moins 2x2")
        self.k = k
        self.size = self.k * self.k
        self.current_state = None
        self.empty_pos = None
        self.solution_path = []
        self.final_positions = {i: ((i-1)//self.k, (i-1)%self.k) for i in range(1, self.size)}
        self.final_positions[0] = (self.k-1, self.k-1)
        #print("Grille finale attendue :")
        #self.display_final_grid()
        
    def display_final_grid(self):
        """Affiche la grille finale basée sur `final_positions`."""
        grid = [[0] * self.k for _ in range(self.k)]
        for val, (i, j) in self.final_positions.items():
            grid[i][j] = val
        
        for row in grid:
            print(' '.join(map(str, row)))
        
    def get_k(self) -> int:
        return self.k

    def generate_random_state(self) -> dict:
        """
        Génère un état initial aléatoire résolvable.
        
        Returns:
            dict: État initial aléatoire valide
        """
        while True:
            positions = [(i, j) for i in range(self.k) for j in range(self.k)]
            random.shuffle(positions)
            state = {i: positions[i] for i in range(self.size)}
            if self.resolvable_grille(state):
                self.set_current_state(state)
                return state

    def set_current_state(self, state: dict) -> None:
        """Sets the current state and updates empty position."""
        if not state or 0 not in state:
            raise ValueError("L'état du jeu doit contenir une case vide représentée par 0.")
        self.current_state = state
        self.empty_pos = state[0]
        self.position_to_value = {pos: val for val, pos in state.items()}

    def get_possible_moves(self) -> list:
        """Retourne les états obtenus après chaque mouvement possible."""
        if self.empty_pos is None or self.current_state is None:
            raise ValueError("La position vide ou l'état actuel n'ont pas été initialisés correctement.")
    
        
        moves = []
        i, j = self.empty_pos

        # Déplacements possibles : haut, bas, gauche, droite
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for di, dj in possible_moves:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < self.k and 0 <= new_j < self.k:
                new_pos = (new_i, new_j)
                value = self.get_position_value(new_pos)
                if value is not None:
                    new_state = self.swap(self.current_state, self.empty_pos, new_pos, value)
                    moves.append(new_state)
        return moves

    def get_position_value(self, pos: tuple) -> int:
        """
        Retourne la valeur à une position donnée.
        
        Args:
            pos (tuple): Position à vérifier
            
        Returns:
            int: Valeur à la position donnée ou None si non trouvée
        """
        return self.position_to_value.get(pos, None)

    def resolvable_grille(self, state: dict) -> bool:
        """Vérifie si la grille est résolvable."""
        inversions = 0
        values = [val for row in range(self.k) for col in range(self.k) for val, pos in state.items() if pos == (row, col) and val != 0]
        
        # Compter les inversions
        for i in range(len(values)-1):
            for j in range(i+1, len(values)):
                if values[i] > values[j]:
                    inversions += 1
        
        if self.k % 2 == 1:
            return inversions % 2 == 0
        else:
            empty_row = state[0][0]
            return (inversions + empty_row) % 2 == 1

    def is_final_state(self, state=None) -> bool:
        """Vérifie si l'état est l'état final."""
        check_state = state if state is not None else self.current_state
        if not check_state:
            return False
        return all(pos == self.final_positions.get(val) for val, pos in check_state.items())


    def moves(self, direction: str) -> bool:
        """
        Effectue un mouvement dans la direction donnée si possible.
        
        Args:
            direction (str): Direction du mouvement ('haut', 'bas', 'gauche', 'droite')
            
        Returns:
            bool: True si le mouvement a été effectué, False sinon
        """
        if self.empty_pos is None or self.current_state is None:
            raise ValueError("La position vide ou l'état actuel n'ont pas été initialisés correctement.")
        
        i, j = self.empty_pos
        new_pos = None
        
        if (direction == 'haut' or direction == 'h') and i > 0:
            new_pos = (i - 1, j)
        elif (direction == 'bas' or direction == 'b') and i < self.k - 1:
            new_pos = (i + 1, j)
        elif (direction == 'gauche' or direction == 'g') and j > 0:
            new_pos = (i, j - 1)
        elif (direction == 'droite' or direction == 'd') and j < self.k - 1:
            new_pos = (i, j + 1)
        
        if new_pos:
            value = self.get_position_value(new_pos)
            if value is not None and self.current_state is not None:
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
        """Affiche l'état actuel sous forme de grille."""
        if not self.current_state:
            print("Aucun état actuel défini.")
            return
        
        grid = [[0] * self.k for _ in range(self.k)]
        for val, (i, j) in self.current_state.items():
            grid[i][j] = val
        
        for row in grid:
            print(' '.join(map(str, row)))
        
    def jeu(self):
        while not self.is_final_state(self.current_state):
            self.display_state()
            print("Mouvements possibles : haut, bas, gauche, droite")
            direction = input("Entrez la direction de mouvement : ").strip().lower()
            if direction in ['haut', 'bas', 'gauche', 'droite','h','b','g','d']:
                if not self.moves(direction):
                    print("Déplacement non valide.")
            else:
                print("Direction invalide.")
        print("Félicitations, vous avez résolu le puzzle !")

