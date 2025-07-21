import random

class JeuTaquin:
    
    def __init__(self, k: int):
        """
        @brief Initialise une nouvelle instance du jeu de taquin
        @param k: Dimension du plateau de jeu (k x k)
        @throws ValueError si k < 2
        
        Initialise un nouveau jeu avec un plateau de taille k x k.
        Les positions finales sont calculées pour chaque tuile,
        avec la case vide (0) placée en bas à droite.
        """
        if k < 2:
            raise ValueError("La taille doit etre supérieure ou égal à 2.")
        self.k = k
        self.size = self.k * self.k
        self.current_state = None
        self.empty_pos = None
        self.solution_path = []
        self.final_positions = {i: ((i-1)//self.k, (i-1)%self.k) for i in range(1, self.size)}
        self.final_positions[0] = (self.k-1, self.k-1)
        
    def display_final_grid(self):
        """
        @brief Affiche la configuration finale du plateau
        
        Affiche la disposition finale attendue du plateau où chaque tuile
        est à sa position cible.
        """
        grid = [[0] * self.k for _ in range(self.k)]
        for val, (i, j) in self.final_positions.items():
            grid[i][j] = val
        
        for i in grid:
            for case in i:
                print(case, end=' ')
            print()
        
    def get_k(self) -> int:
        """
        @brief Retourne la dimension du plateau
        @return: La dimension k du plateau k x k
        """
        return self.k

    def generate_random_state(self) -> dict:
        """
        @brief Génère un état initial aléatoire résolvable
        @return: Dictionnaire représentant un état initial valide et résolvable
        
        Génère une configuration aléatoire du plateau qui garantit
        l'existence d'une solution vers l'état final.
        """
        while True:
            positions = [(i, j) for i in range(self.k) for j in range(self.k)]
            random.shuffle(positions)
            state = {i: positions[i] for i in range(self.size)}
            if self.resolvable_grille(state):
                self.set_current_state(state)
                return state

    def set_current_state(self, state: dict) -> None:
        """
        @brief Définit l'état actuel du jeu
        @param state: Dictionnaire associant les valeurs des tuiles à leurs positions
        @throws ValueError si l'état ne contient pas de case vide (0)
        
        Met à jour l'état actuel du jeu et la position de la case vide.
        """
        if not state or 0 not in state:
            raise ValueError("Il n'y a pas de case avec un 0.")
        self.current_state = state
        self.empty_pos = state[0]
        self.position_to_value = {pos: val for val, pos in state.items()}

    def get_possible_moves(self) -> list:
        """
        @brief Retourne tous les états possibles après un mouvement
        @return: Liste des états possibles après un mouvement
        @throws ValueError si l'état actuel n'est pas initialisé
        
        Calcule tous les états atteignables en un mouvement
        depuis l'état actuel.
        """
        if self.empty_pos is None or self.current_state is None:
            raise ValueError("La position vide ou l'état actuel n'ont pas été initialisés correctement.")

        moves = []
        i, j = self.empty_pos

        # Déplacements possibles : haut, bas, gauche, droite
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for posi, posj in possible_moves:
            new_i, new_j = i + posi, j + posj
            if 0 <= new_i < self.k and 0 <= new_j < self.k:
                new_pos = (new_i, new_j)
                value = self.get_position_value(new_pos)
                if value is not None:
                    new_state = self.swap(self.current_state, self.empty_pos, new_pos, value)
                    moves.append(new_state)
        return moves

    def get_position_value(self, pos: tuple) -> int:
        """
        @brief Retourne la valeur d'une tuile à une position donnée
        @param pos: Tuple (i,j) représentant la position à vérifier
        @return: Valeur de la tuile à la position donnée ou None si invalide
        """
        return self.position_to_value.get(pos, None)

    def resolvable_grille(self, state: dict) -> bool:
        """
        @brief Vérifie si une configuration est résolvable
        @param state: État à vérifier
        @return: True si l'état est résolvable, False sinon
        
        Utilise le théorème des inversions pour déterminer
        si une configuration peut être résolue.
        """
        inversions = 0
        values = [val for i in range(self.k) for j in range(self.k) for val, pos in state.items() if pos == (i, j) and val != 0]
        
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
        """
        @brief Vérifie si un état donné est l'état final
        @param state: État à vérifier (utilise l'état actuel si None)
        @return: True si l'état est final, False sinon
        """
        check_state = state if state is not None else self.current_state
        if not check_state:
            return False
        return all(pos == self.final_positions.get(val) for val, pos in check_state.items())


    def moves(self, direction: str) -> bool:
        """
        @brief Effectue un mouvement dans la direction spécifiée
        @param direction: Direction du mouvement ('haut'/'h', 'bas'/'b', 'gauche'/'g', 'droite'/'d')
        @return: True si le mouvement a été effectué, False si impossible
        @throws ValueError si l'état actuel n'est pas initialisé
        
        Déplace la case vide dans la direction spécifiée si possible.
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
        """
        @brief Échange deux positions dans un état
        @param state: État actuel
        @param pos1: Position de la première tuile
        @param pos2: Position de la deuxième tuile
        @param value2: Valeur de la tuile à la position 2
        @return: Nouvel état après l'échange
        """
        new_state = state.copy()
        new_state[value2] = pos1
        new_state[0] = pos2
        return new_state
    
    def afficher_chemin_solution(self) -> None:
        if not self.solution_path:
            print("Aucun chemin de solution disponible")
            return
        
        print("\nChemin de la solution: ")
        for i in range(len(self.solution_path)):
            state_str = self.solution_path[i]
            state = {}

            positions = state_str[1:-1].split(')(')

            for index, pos in enumerate(positions):
                coords = pos.split(',')
                x = int(coords[0].strip())
                y = int(coords[1].strip())
                state[index] = (x, y)

            print(f"\nÉtape {i}:")
            self.set_current_state(state)
            self.afficher_etat()

        print(f"\nNombre total de mouvements : {len(self.solution_path) - 1}")

    def afficher_etat(self) -> None:
        """
        @brief Affiche l'état actuel du jeu
        
        Affiche le plateau de jeu dans sa configuration actuelle
        sous forme de grille.
        """
        if not self.current_state:
            print("Aucun état actuel défini.")
            return
        
        grid = [[0] * self.k for _ in range(self.k)]
        for val, (i, j) in self.current_state.items():
            grid[i][j] = val

        for i in grid:
            for case in i:
                print(case, end=' ')
            print()
        
    def jeu(self):
        """
        @brief Démarre une partie interactive du jeu de taquin
        
        Permet au joueur de déplacer les tuiles jusqu'à atteindre
        l'état final. Le joueur entre les directions via le clavier.
        """
        while not self.is_final_state(self.current_state):
            self.afficher_etat()
            print("Mouvements possibles : haut, bas, gauche, droite")
            direction = input("Entrez la direction de mouvement : ").strip().lower()
            if direction in ['haut', 'bas', 'gauche', 'droite','h','b','g','d']:
                if not self.moves(direction):
                    print("Déplacement non valide.")
            else:
                print("Direction invalide.")
        print("Félicitations, vous avez résolu le jeu Taquin.")

