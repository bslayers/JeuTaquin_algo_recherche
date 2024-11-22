import time
import os
from datetime import datetime
from jeu.jeuTaquin import JeuTaquin
from algorithme_recherche.bfs import bfs_search
from algorithme_recherche.dfs import dfs_search
from algorithme_recherche.astar import astar_search 

precision:int = 12

def test_bfs(jeu, initial_state, final_state=None):
    start_time = time.time()
    if final_state is None:
        return None
    try:
        bfs_search(jeu, initial_state.copy(), final_state)
        return time.time() - start_time
    except Exception as e:
        print(f"Erreur dans bfs : {e}")
        return float('inf')

def test_dfs(jeu, initial_state, final_state=None):
    start_time = time.time()
    if final_state is None:
        return None
    try:
        dfs_search(jeu, initial_state.copy(), final_state)
        return time.time() - start_time
    except Exception as e:
        print(f"Erreur dans dfs : {e}")
        return float('inf')

def test_astar(jeu, initial_state, final_state=None):
    start_time = time.time()
    if final_state is None:
        return None
    try:
        astar_search(jeu, initial_state.copy(), final_state)
        return time.time() - start_time
    except Exception as e:
        print(f"Erreur dans A* : {e}")
        return float('inf')

def run_single_test(size, final_state=None):
    jeu = JeuTaquin(size)
    initial_state = jeu.generate_random_state()
    results = {'astar': [], 'bfs': [], 'dfs': []}
    completed_tests = {'astar': 0, 'bfs': 0, 'dfs': 0}
    
    algorithms = [
        ('astar', test_astar),
        ('bfs', test_bfs),
        ('dfs', test_dfs)
    ]
    
    try:
        for name, test in algorithms:
            jeu_copy = JeuTaquin(size)
            jeu_copy.set_current_state(initial_state.copy())
            
            execution_time = test(jeu_copy, initial_state.copy(), final_state)
            results[name].append(execution_time)
            completed_tests[name] += 1
            print(f"{name.upper()} terminé en {execution_time:{precision}f} secondes")
            
    except KeyboardInterrupt:
        raise KeyboardInterrupt(results, completed_tests)
    
    return results, completed_tests

def run_multiple_tests(size, num_tests=10, final_state=None):
    combined_results = {'astar': [], 'bfs': [], 'dfs': []}
    total_completed = {'astar': 0, 'bfs': 0, 'dfs': 0}
    
    try:
        for i in range(num_tests):
            print(f"\nTest #{i+1} pour grille {size}x{size}")
            single_test_results, completed = run_single_test(size, final_state)
            
            for algo in combined_results:
                combined_results[algo].extend(single_test_results[algo])
                total_completed[algo] += completed[algo]
                
    except KeyboardInterrupt as e:
        print("\n\nInterruption détectée. Sauvegarde des résultats partiels...")
        partial_results = e.args[0] if len(e.args) > 0 else {}
        partial_completed = e.args[1] if len(e.args) > 1 else {}

        # Merge the partial results with combined_results
        for algo in combined_results:
            if algo in partial_results:
                combined_results[algo].extend(partial_results[algo])
                total_completed[algo] += partial_completed.get(algo, 0)

        raise KeyboardInterrupt(combined_results, total_completed)
    
    return combined_results, total_completed

def calculate_statistics(results, completed_tests):
    stats = {}
    for algo, times in results.items():
        if times:
            stats[algo] = {
                'min': min(times),
                'max': max(times),
                'avg': sum(times) / len(times),
                'times': times,
                'completed_tests': completed_tests[algo]
            }
        else:
            stats[algo] = {
                'min': 0,
                'max': 0,
                'avg': 0,
                'times': [],
                'completed_tests': 0
            }
    return stats

def format_results(grid_results):
    output = [f"Résultats des tests - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
    output.append("=" * 50 + "\n")
    
    for size, results in grid_results.items():
        output.append(f"\nRésultats pour grille {size}x{size}")
        output.append("-" * 30)
        
        for algo, stats in results.items():
            output.append(f"\n{algo.upper()} (Tests complétés: {stats['completed_tests']}):")
            if stats['times']:
                output.append(f"  Temps minimum: {stats['min']:.{precision}f} secondes")
                output.append(f"  Temps maximum: {stats['max']:.{precision}f} secondes")
                output.append(f"  Temps moyen: {stats['avg']:.{precision}f} secondes")
                #output.append(f"  Détail des temps: {', '.join([f'{t:.{precision}f}' for t in stats['times']])}")
            else:
                output.append("  Aucun test complété")
    
    return "\n".join(output)

def save_results(formatted_results, filename):
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
        print(f"Erreur lors de la sauvegarde des résultats: {str(e)}")


def calculate_final_state(k: int) -> dict:
    """Calcule l'état final pour une grille de taille k."""
    final_state = {i: ((i-1)//k, (i-1)%k) for i in range(1, k*k)}
    final_state[0] = (k-1, k-1)
    return final_state

def main():
    grid_sizes = [4]
    num_tests = 100
    all_results = {}
    
    try:
        print("Démarrage des tests...")
        for size in grid_sizes:
            print(f"\nTests pour grille {size}x{size}")
            # Calculer l'état final une fois pour chaque taille
            final_state = calculate_final_state(size)
            results, completed = run_multiple_tests(size, num_tests, final_state)
            all_results[size] = calculate_statistics(results, completed)
            
    except KeyboardInterrupt as e:
        print("\n\nInterruption détectée. Sauvegarde des résultats partiels...")
        partial_results = e.args[0] if len(e.args) > 0 else {}
        partial_completed = e.args[1] if len(e.args) > 1 else {}

        current_size = grid_sizes[len(all_results)] if len(all_results) < len(grid_sizes) else "Unknown"
        all_results[current_size] = calculate_statistics(partial_results, partial_completed)
    
    except Exception as e:
        print(f"Erreur lors de l'exécution des tests: {str(e)}")
    
    finally:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        status = "partiels" if len(all_results) < len(grid_sizes) else "complets"
        formatted_results = format_results(all_results)
        save_results(formatted_results, f'resultats_{status}_{timestamp}.txt')

if __name__ == "__main__":
    main()
