import time
import os
from datetime import datetime
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.bfs import bfs
from algorithme_recherche.dfs import dfs
from algorithme_recherche.astar import astar

class Colors:
    ASTAR = '\033[94m'  # Bleu
    BFS = '\033[92m'    # Vert
    DFS = '\033[93m'    # Jaune
    FAIL = '\033[91m'   # Rouge
    END = '\033[0m'     # reset

precision:int = 12

def test_bfs(jeu, initial_state, final_state=None):
    start_time = time.time()
    if final_state is None:
        return None
    try:
        result = bfs(jeu, initial_state.copy(), final_state)
        if result is None:
            return time.time() - start_time, False
        return time.time() - start_time, True
    except Exception as e:
        print(f"{Colors.FAIL}Erreur dans bfs : {e}{Colors.END}")
        return float('inf'), False

def test_dfs(jeu, initial_state, final_state=None):
    start_time = time.time()
    if final_state is None:
        return None
    try:
        result = dfs(jeu, initial_state.copy(), final_state)
        if result is None:
            return time.time() - start_time, False
        return time.time() - start_time, True
    except Exception as e:
        print(f"{Colors.FAIL}Erreur dans dfs : {e}{Colors.END}")
        return float('inf'), False

def test_astar(jeu, initial_state, final_state=None):
    if final_state is None:
        return None, False
    
    start_time = time.time()
    try:
        result = astar(jeu, initial_state.copy(), final_state)
        if result is None:
            return time.time() - start_time, False
        return time.time() - start_time, True
    except Exception as e:
        print(f"{Colors.FAIL}Erreur dans A* : {e}{Colors.END}")
        return float('inf'), False

def test(size, final_state=None):
    jeu = JeuTaquin(size)
    initial_state = jeu.generate_random_state()
    results = {'astar': [], 'bfs': [], 'dfs': []}
    completed_tests = {'astar': 0, 'bfs': 0, 'dfs': 0}
    failed_attempts = {'astar': 0, 'bfs': 0, 'dfs': 0}
    
    # Pour la taille 4, on ne teste que A*
    if size == 4:
        try:
            jeu_copy = JeuTaquin(size)
            jeu_copy.set_current_state(initial_state.copy())
            time_result, success = test_astar(jeu_copy, initial_state.copy(), final_state)
            if success and time_result is not None:
                results['astar'].append(time_result)
                completed_tests['astar'] += 1
                print(f"{Colors.ASTAR}A* terminé en {time_result:{precision}f} secondes{Colors.END}")
            else:
                failed_attempts['astar'] += 1
                print(f"{Colors.FAIL}A* : Solution non trouvée{Colors.END}")
        except Exception as e:
            print(f"{Colors.FAIL}Erreur inattendue : {e}{Colors.END}")
            failed_attempts['astar'] += 1
        return results, completed_tests, failed_attempts
    
    # Pour la taille 3, on teste tous les algorithmes
    algorithms = [
        ('astar', test_astar, Colors.ASTAR),
        ('bfs', test_bfs, Colors.BFS),
        ('dfs', test_dfs, Colors.DFS)
    ]
    
    try:
        for name, test, color in algorithms:
            jeu_copy = JeuTaquin(size)
            jeu_copy.set_current_state(initial_state.copy())
            
            execution_time, success = test(jeu_copy, initial_state.copy(), final_state)
            if success and execution_time is not None:
                results[name].append(execution_time)
                completed_tests[name] += 1
                print(f"{color}{name.upper()} terminé en {execution_time:{precision}f} secondes{Colors.END}")
            else:
                failed_attempts[name] += 1
                print(f"{Colors.FAIL}{name.upper()} : Solution non trouvée{Colors.END}")
            
    except KeyboardInterrupt:
        raise KeyboardInterrupt(results, completed_tests, failed_attempts)
    
    return results, completed_tests, failed_attempts

def multiple_tests(size, num_tests=10, final_state=None):
    combined_results = {'astar': [], 'bfs': [], 'dfs': []}
    total_completed = {'astar': 0, 'bfs': 0, 'dfs': 0}
    total_failed = {'astar': 0, 'bfs': 0, 'dfs': 0}
    
    try:
        for i in range(num_tests):
            print(f"\nTest #{i+1} pour grille {size}x{size}")
            single_test_results, completed, failed = test(size, final_state)
            
            for algo in combined_results:
                if algo in single_test_results:
                    combined_results[algo].extend(single_test_results[algo])
                    total_completed[algo] += completed[algo]
                    total_failed[algo] += failed[algo]
                
    except KeyboardInterrupt:
        print("\n\nInterruption détectée. Sauvegarde des résultats partiels...")
        return combined_results, total_completed, total_failed
    
    return combined_results, total_completed, total_failed

def calculate_statistics(results, completed_tests, failed_tests):
    stats = {}
    for algo, times in results.items():
        if times:  # Si des temps ont été enregistrés
            stats[algo] = {
                'min': min(times),
                'max': max(times),
                'avg': sum(times) / len(times),
                'times': times,
                'completed_tests': completed_tests[algo],
                'failed_tests': failed_tests[algo]
            }
        else:  # Si aucun temps n'a été enregistré
            stats[algo] = {
                'min': 0,
                'max': 0,
                'avg': 0,
                'times': [],
                'completed_tests': completed_tests[algo],
                'failed_tests': failed_tests[algo]
            }
    return stats

def format_resultat(grid_results):
    """Formate les résultats en Markdown."""
    output = [f"# Résultats des tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
    output.append("---\n")

    colors = {
        'astar': "🟦",
        'bfs': "🟩",
        'dfs': "🟨"
    }

    for size, results in grid_results.items():
        output.append(f"\n## Résultats pour grille {size}x{size}")
        output.append("---")

        for algo, stats in results.items():
            if stats['completed_tests'] > 0 or stats['failed_tests'] > 0:
                color_emoji = colors.get(algo, '⬜️')
                output.append(f"\n### {color_emoji} {algo.upper()}")
                output.append(f"- **Tests complétés**: {stats['completed_tests']}")
                output.append(f"- **Tests échoués**: {stats['failed_tests']}")

                if stats['times']:
                    output.append(f"  - **Temps minimum**: `{stats['min']:.{precision}f}` secondes")
                    output.append(f"  - **Temps maximum**: `{stats['max']:.{precision}f}` secondes")
                    output.append(f"  - **Temps moyen**: `{stats['avg']:.{precision}f}` secondes")

    return "\n".join(output)

def save_file(formatted_results, filename):
    repertoire_courant = os.path.dirname(__file__)
    dossier = os.path.join(repertoire_courant, 'test')
    
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    chemin_fichier = os.path.join(dossier, filename)
    
    try:
        with open(chemin_fichier, 'w', encoding='utf-8') as f:
            f.write(formatted_results)
        print(f"\nRésultats sauvegardés dans {chemin_fichier}")
    except Exception as e:
        print(f"{Colors.FAIL}Erreur lors de la sauvegarde des résultats: {str(e)}{Colors.END}")

def calculate_final_state(k: int) -> dict:
    """Calcule l'état final pour une grille de taille k."""
    final_state = {i: ((i-1)//k, (i-1)%k) for i in range(1, k*k)}
    final_state[0] = (k-1, k-1)
    return final_state

def main():
    taille_grille = [2,3,4]
    num_tests = 1000
    all_results = {}
    
    try:
        print("Démarrage des tests: ")
        for size in taille_grille:
            print(f"\nTests pour grille {size}x{size}")
            final_state = calculate_final_state(size)
            results, completed, failed = multiple_tests(size, num_tests, final_state)
            all_results[size] = calculate_statistics(results, completed, failed)
            
    except KeyboardInterrupt as e:
        print("\n\nInterruption détectée. Sauvegarde des résultats partiels")
        if len(e.args) >= 3:
            partial_results, partial_completed, partial_failed = e.args[:3]
            current_size = taille_grille[len(all_results)] if len(all_results) < len(taille_grille) else "Unknown"
            all_results[current_size] = calculate_statistics(partial_results, partial_completed, partial_failed)
    
    except Exception as e:
        print(f"{Colors.FAIL}Erreur lors de l'exécution des tests: {str(e)}{Colors.END}")
    
    finally:
        time = datetime.now().strftime('%Y%m%d_%H%M%S')
        status = "partiels" if len(all_results) < len(taille_grille) else "complets"
        resultat = format_resultat(all_results)
        save_file(resultat, f'resultats_{status}_{time}.md')

if __name__ == "__main__":
    main()