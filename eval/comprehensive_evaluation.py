"""
Comprehensive Agent Evaluation Script

Evaluates trained Q-learning agent against baseline agents and minimax.
"""

import argparse
import time
import json
from typing import Dict, List, Tuple
from tictactoe import TicTacToe
from qlearning_agent import UltraAdvancedQLearningAgent
from baseline_agents import RandomAgent, HeuristicAgent, MinimaxAgent, TournamentHarness


class ComprehensiveEvaluator:
    """Comprehensive evaluator for testing trained agent against baselines."""
    
    def __init__(self, q_table_file: str = "q_table.json"):
        self.q_table_file = q_table_file
        self.trained_agent = UltraAdvancedQLearningAgent()
        self.baseline_agents = {
            'Random': RandomAgent(),
            'Heuristic': HeuristicAgent(),
            'Minimax': MinimaxAgent()
        }
        
        # Load trained Q-table
        try:
            self.trained_agent.load_q_table(q_table_file)
            print(f"Loaded trained agent from {q_table_file}")
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            print("Starting with untrained agent")
    
    def evaluate_vs_baseline(self, baseline_name: str, num_games: int = 100) -> Dict:
        """Evaluate trained agent against a specific baseline."""
        baseline_agent = self.baseline_agents[baseline_name]
        
        print(f"\nEvaluating Trained Agent vs {baseline_name} ({num_games} games)")
        print("-" * 50)
        
        results = {
            'trained_wins': 0,
            'baseline_wins': 0,
            'draws': 0,
            'game_lengths': []
        }
        
        for game_num in range(num_games):
            # Trained agent plays as X (player 1)
            winner, length = self.play_game(self.trained_agent, baseline_agent)
            results['game_lengths'].append(length)
            
            if winner == 1:
                results['trained_wins'] += 1
            elif winner == -1:
                results['baseline_wins'] += 1
            else:
                results['draws'] += 1
            
            # Baseline agent plays as X (player 1) - swap roles
            winner, length = self.play_game(baseline_agent, self.trained_agent)
            results['game_lengths'].append(length)
            
            if winner == 1:
                results['baseline_wins'] += 1
            elif winner == -1:
                results['trained_wins'] += 1
            else:
                results['draws'] += 1
            
            if (game_num + 1) % 20 == 0:
                total_games = (game_num + 1) * 2
                trained_rate = results['trained_wins'] / total_games * 100
                print(f"Progress: {total_games}/{num_games * 2} games | "
                      f"Trained Win Rate: {trained_rate:.1f}%")
        
        # Calculate final statistics
        total_games = num_games * 2
        results['trained_win_rate'] = results['trained_wins'] / total_games * 100
        results['baseline_win_rate'] = results['baseline_wins'] / total_games * 100
        results['draw_rate'] = results['draws'] / total_games * 100
        results['avg_game_length'] = sum(results['game_lengths']) / len(results['game_lengths'])
        
        print(f"\nResults vs {baseline_name}:")
        print(f"Trained Agent Wins: {results['trained_wins']} ({results['trained_win_rate']:.1f}%)")
        print(f"{baseline_name} Wins: {results['baseline_wins']} ({results['baseline_win_rate']:.1f}%)")
        print(f"Draws: {results['draws']} ({results['draw_rate']:.1f}%)")
        print(f"Average Game Length: {results['avg_game_length']:.1f} moves")
        
        return results
    
    def play_game(self, agent1, agent2, verbose: bool = False) -> Tuple[int, int]:
        """Play a game between two agents."""
        game = TicTacToe()
        moves = 0
        
        while not game.game_over and moves < 9:
            if game.current_player == 1:
                action = agent1.choose_action(game)
            else:
                action = agent2.choose_action(game)
            
            game.make_move(action)
            moves += 1
            
            if verbose:
                print(f"Move {moves}: Player {game.current_player} plays at {action}")
                game.display_board()
                print()
        
        return game.winner, moves
    
    def run_comprehensive_evaluation(self, games_per_baseline: int = 100) -> Dict:
        """Run comprehensive evaluation against all baselines."""
        print("Comprehensive Agent Evaluation")
        print("=" * 50)
        
        all_results = {}
        
        # Evaluate against each baseline
        for baseline_name in self.baseline_agents.keys():
            results = self.evaluate_vs_baseline(baseline_name, games_per_baseline)
            all_results[baseline_name] = results
        
        # Print summary
        self.print_evaluation_summary(all_results)
        
        # Save results
        self.save_evaluation_results(all_results)
        
        return all_results
    
    def print_evaluation_summary(self, results: Dict):
        """Print evaluation summary."""
        print("\nEvaluation Summary:")
        print("=" * 60)
        print(f"{'Baseline':<15} {'Trained Win Rate':<18} {'Draw Rate':<12} {'Avg Length':<12}")
        print("-" * 60)
        
        for baseline_name, result in results.items():
            print(f"{baseline_name:<15} {result['trained_win_rate']:<18.1f}% "
                  f"{result['draw_rate']:<12.1f}% {result['avg_game_length']:<12.1f}")
    
    def save_evaluation_results(self, results: Dict):
        """Save evaluation results to file."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\nEvaluation results saved to {filename}")
    
    def run_tournament(self, games_per_match: int = 50):
        """Run tournament including trained agent."""
        print("\nRunning Tournament with All Agents")
        print("=" * 50)
        
        # Create tournament agents list
        tournament_agents = [self.trained_agent]
        tournament_agents.extend(self.baseline_agents.values())
        
        # Run tournament
        tournament = TournamentHarness()
        results = tournament.run_tournament(tournament_agents, games_per_match)
        tournament.print_tournament_results(results)
        
        return results


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(description="Comprehensive agent evaluation")
    parser.add_argument("--q_table_file", type=str, default="q_table.json",
                        help="Path to trained Q-table file")
    parser.add_argument("--games", type=int, default=100,
                        help="Number of games per baseline evaluation")
    parser.add_argument("--tournament", action="store_true",
                        help="Run full tournament")
    parser.add_argument("--baseline", type=str, choices=['Random', 'Heuristic', 'Minimax'],
                        help="Evaluate against specific baseline only")
    
    args = parser.parse_args()
    
    evaluator = ComprehensiveEvaluator(q_table_file=args.q_table_file)
    
    if args.baseline:
        # Evaluate against specific baseline
        evaluator.evaluate_vs_baseline(args.baseline, args.games)
    elif args.tournament:
        # Run tournament
        evaluator.run_tournament(games_per_match=args.games // 2)
    else:
        # Run comprehensive evaluation
        evaluator.run_comprehensive_evaluation(games_per_baseline=args.games)


if __name__ == "__main__":
    main()
