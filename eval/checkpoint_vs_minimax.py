"""
Minimax Evaluation Script for Q-Learning Tic-Tac-Toe AI

Evaluates trained Q-learning agent against minimax opponent.
Provides deterministic comparison for checkpoint evaluation.
"""

import sys
import os
import time
import argparse
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tictactoe import TicTacToe
from qlearning_agent import UltraAdvancedQLearningAgent


class MinimaxAgent:
    """Perfect minimax agent for comparison."""
    
    def __init__(self):
        self.name = "Minimax"
    
    def evaluate_position(self, game: TicTacToe) -> int:
        """Evaluate current position using minimax."""
        if game.game_over:
            if game.winner == 1:
                return 1
            elif game.winner == -1:
                return -1
            else:
                return 0
        
        available_actions = game.get_available_actions()
        if not available_actions:
            return 0
        
        # Try each possible move
        scores = []
        for action in available_actions:
            # Make move
            test_game = game.copy()
            test_game.make_move(action)
            
            # Evaluate resulting position
            score = self.evaluate_position(test_game)
            scores.append(score)
        
        # Return best score for current player
        if game.current_player == 1:
            return max(scores)
        else:
            return min(scores)
    
    def choose_action(self, game: TicTacToe) -> int:
        """Choose best action using minimax."""
        available_actions = game.get_available_actions()
        if not available_actions:
            raise ValueError("No available actions!")
        
        best_action = None
        best_score = float('-inf') if game.current_player == 1 else float('inf')
        
        for action in available_actions:
            # Make move
            test_game = game.copy()
            test_game.make_move(action)
            
            # Evaluate position
            score = self.evaluate_position(test_game)
            
            # Update best action
            if game.current_player == 1:  # Maximizing player
                if score > best_score:
                    best_score = score
                    best_action = action
            else:  # Minimizing player
                if score < best_score:
                    best_score = score
                    best_action = action
        
        return best_action


class GameEvaluator:
    """Evaluator for comparing agents."""
    
    def __init__(self, q_table_file: str = "q_table.json"):
        """Initialize evaluator with trained Q-learning agent."""
        self.q_agent = UltraAdvancedQLearningAgent()
        self.minimax_agent = MinimaxAgent()
        
        # Load trained Q-table
        try:
            self.q_agent.load_q_table(q_table_file)
            print(f"Loaded Q-table from {q_table_file}")
        except FileNotFoundError:
            print(f"Q-table file {q_table_file} not found!")
            print("Please train the agent first using: python train.py")
            sys.exit(1)
    
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
        
        winner = game.winner
        return winner, moves
    
    def evaluate_vs_minimax(self, num_games: int = 100, verbose: bool = False) -> Dict:
        """Evaluate Q-learning agent vs minimax agent."""
        print(f"Evaluating Q-Learning Agent vs Minimax Agent ({num_games} games)")
        print("=" * 60)
        
        results = {
            'q_wins': 0,
            'minimax_wins': 0,
            'draws': 0,
            'game_lengths': []
        }
        
        for game_num in range(1, num_games + 1):
            if verbose and game_num <= 3:  # Show first 3 games
                print(f"Game {game_num}:")
                winner, length = self.play_game(
                    self.q_agent, 
                    self.minimax_agent, 
                    verbose=True
                )
            else:
                winner, length = self.play_game(
                    self.q_agent, 
                    self.minimax_agent, 
                    verbose=False
                )
            
            results['game_lengths'].append(length)
            
            if winner == 1:  # Q-agent wins
                results['q_wins'] += 1
            elif winner == -1:  # Minimax wins
                results['minimax_wins'] += 1
            else:  # Draw
                results['draws'] += 1
            
            # Progress update
            if game_num % 20 == 0:
                q_rate = results['q_wins'] / game_num * 100
                print(f"Progress: {game_num}/{num_games} games | "
                      f"Q-agent win rate: {q_rate:.1f}%")
        
        # Calculate final statistics
        total_games = sum([results['q_wins'], results['minimax_wins'], results['draws']])
        results['q_win_rate'] = results['q_wins'] / total_games * 100
        results['minimax_win_rate'] = results['minimax_wins'] / total_games * 100
        results['draw_rate'] = results['draws'] / total_games * 100
        results['avg_game_length'] = sum(results['game_lengths']) / len(results['game_lengths'])
        
        return results
    
    def print_results(self, results: Dict):
        """Print evaluation results."""
        print("\nEvaluation Results:")
        print("-" * 40)
        print(f"Q-Learning Agent Wins: {results['q_wins']:,} ({results['q_win_rate']:.1f}%)")
        print(f"Minimax Agent Wins: {results['minimax_wins']:,} ({results['minimax_win_rate']:.1f}%)")
        print(f"Draws: {results['draws']:,} ({results['draw_rate']:.1f}%)")
        print(f"Average Game Length: {results['avg_game_length']:.1f} moves")
        
        # Performance analysis
        print("\nPerformance Analysis:")
        print("-" * 40)
        if results['q_win_rate'] > 40:
            print("Q-Learning agent shows strong performance!")
        elif results['q_win_rate'] > 20:
            print("Q-Learning agent shows moderate performance")
        else:
            print("Q-Learning agent needs more training")
        
        if results['draw_rate'] > 60:
            print("High draw rate indicates good defensive play")
        elif results['draw_rate'] > 40:
            print("Moderate draw rate")
        else:
            print("Low draw rate - may need defensive training")


def main():
    """Main evaluation function."""
    parser = argparse.ArgumentParser(description='Evaluate Q-Learning agent vs Minimax')
    parser.add_argument('--games', type=int, default=100, 
                       help='Number of games to play (default: 100)')
    parser.add_argument('--q-table', type=str, default='q_table.json',
                       help='Path to Q-table file (default: q_table.json)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed game output for first few games')
    
    args = parser.parse_args()
    
    print("Q-Learning vs Minimax Evaluation")
    print("=" * 50)
    print(f"Q-table file: {args.q_table}")
    print(f"Number of games: {args.games}")
    print(f"Verbose mode: {args.verbose}")
    print()
    
    # Create evaluator
    evaluator = GameEvaluator(args.q_table)
    
    # Run evaluation
    start_time = time.time()
    results = evaluator.evaluate_vs_minimax(args.games, args.verbose)
    end_time = time.time()
    
    # Print results
    evaluator.print_results(results)
    
    print(f"\nEvaluation completed in {end_time - start_time:.2f} seconds")
    
    # Return exit code based on performance
    if results['q_win_rate'] > 30:  # Good performance threshold
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
