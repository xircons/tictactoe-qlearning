import random
import time
from typing import Dict, List, Tuple
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from core.tictactoe import TicTacToe
from agents.qlearning_agent import UltraAdvancedQLearningAgent, RandomAgent


class GameEvaluator:
    """Evaluator for testing trained Q-learning agent."""
    
    def __init__(self, q_table_file: str = "q_table.json"):
        """
        Initialize evaluator.
        
        Args:
            q_table_file: Path to saved Q-table
        """
        self.q_table_file = q_table_file
        self.trained_agent = UltraAdvancedQLearningAgent()
        self.random_agent = RandomAgent()
        
        # Load trained Q-table
        self.trained_agent.load_q_table(q_table_file)
        
    def play_game(self, 
                  agent1, 
                  agent2, 
                  verbose: bool = False,
                  delay: float = 0.0) -> Tuple[int, int]:
        """
        Play a game between two agents.
        
        Args:
            agent1: First agent (plays as X, player 1)
            agent2: Second agent (plays as O, player -1)
            verbose: Whether to display the game
            delay: Delay between moves (for visualization)
            
        Returns:
            Tuple of (winner, game_length)
        """
        game = TicTacToe()
        
        if verbose:
            print("Let starting the game!")
            print("=" * 20)
            game.display_board()
            print()
        
        move_count = 0
        
        while not game.game_over:
            if verbose:
                player_symbol = 'X' if game.current_player == 1 else 'O'
                print(f"Player {player_symbol}'s turn:")
            
            # Choose agent based on current player
            if game.current_player == 1:
                action = agent1.choose_action(game)
            else:
                action = agent2.choose_action(game)
            
            # Make move
            game.make_move(action)
            move_count += 1
            
            if verbose:
                print(f"Plays at position {action}")
                game.display_board()
                print()
                
                if delay > 0:
                    time.sleep(delay)
        
        # Game finished
        if verbose:
            if game.winner == 1:
                print("Player X wins!")
            elif game.winner == -1:
                print("Player O wins!")
            else:
                print("It's a draw!")
            print(f"Game length: {move_count} moves")
            print("=" * 20)
            print()
        
        return game.winner, move_count
    
    def evaluate_vs_random(self, num_games: int = 1000, verbose: bool = False) -> Dict:
        """
        Evaluate trained agent against random agent.
        
        Args:
            num_games: Number of games to play
            verbose: Whether to show individual games
            
        Returns:
            Dictionary with evaluation results
        """
        print(f"Evaluating trained agent vs random agent ({num_games} games)")
        print("=" * 60)
        
        results = {
            'trained_wins': 0,
            'random_wins': 0,
            'draws': 0,
            'game_lengths': []
        }
        
        for game_num in range(1, num_games + 1):
            if verbose and game_num <= 5:  # Show first 5 games
                print(f"Game {game_num}:")
                winner, length = self.play_game(
                    self.trained_agent, 
                    self.random_agent, 
                    verbose=True,
                    delay=0.5
                )
            else:
                winner, length = self.play_game(
                    self.trained_agent, 
                    self.random_agent, 
                    verbose=False
                )
            
            results['game_lengths'].append(length)
            
            if winner == 1:  # Trained agent wins
                results['trained_wins'] += 1
            elif winner == -1:  # Random agent wins
                results['random_wins'] += 1
            else:  # Draw
                results['draws'] += 1
            
            # Progress update
            if game_num % 100 == 0:
                win_rate = results['trained_wins'] / game_num * 100
                print(f"Progress: {game_num}/{num_games} games | "
                      f"Trained agent win rate: {win_rate:.1f}%")
        
        # Calculate final statistics
        total_games = sum([results['trained_wins'], results['random_wins'], results['draws']])
        results['trained_win_rate'] = results['trained_wins'] / total_games * 100
        results['random_win_rate'] = results['random_wins'] / total_games * 100
        results['draw_rate'] = results['draws'] / total_games * 100
        results['avg_game_length'] = sum(results['game_lengths']) / len(results['game_lengths'])
        
        # Print results
        print("\nEvaluation Results:")
        print("-" * 30)
        print(f"Trained Agent Wins: {results['trained_wins']:,} ({results['trained_win_rate']:.1f}%)")
        print(f"Random Agent Wins: {results['random_wins']:,} ({results['random_win_rate']:.1f}%)")
        print(f"Draws: {results['draws']:,} ({results['draw_rate']:.1f}%)")
        print(f"Average Game Length: {results['avg_game_length']:.1f} moves")
        
        return results
    
    def play_human_vs_ai(self):
        """Interactive human vs AI game."""
        print("Human vs AI Tic-Tac-Toe")
        print("=" * 30)
        print("You are X, AI is O")
        print("Enter position (0-8) or 'quit' to exit")
        print()
        
        while True:
            game = TicTacToe()
            
            print("New game! You go first kub.")
            game.display_board()
            print()
            
            while not game.game_over:
                if game.current_player == 1:  # Human's turn
                    while True:
                        try:
                            user_input = input("Your move (0-8): ").strip()
                            if user_input.lower() == 'quit':
                                print("Thanks for playing kub!")
                                return
                            
                            action = int(user_input)
                            if action in game.get_available_actions():
                                break
                            else:
                                print("Invalid move! Try again.")
                        except ValueError:
                            print("Please enter a number 0-8 or 'quit'.")
                    
                    game.make_move(action)
                    print(f"You play at {action}")
                    game.display_board()
                    print()
                    
                else:  # AI's turn
                    print("AI is thinking...")
                    action = self.trained_agent.choose_action(game)
                    game.make_move(action)
                    print(f"AI plays at {action}")
                    game.display_board()
                    print()
            
            # Game finished
            if game.winner == 1:
                print("You win! Congratulations!")
            elif game.winner == -1:
                print("AI wins! มึงอะกาก!")
            else:
                print("It's a draw! GG kub!")
            
            print()
            play_again = input("Play again? (y/n): ").strip().lower()
            if play_again not in ['y', 'yes']:
                print("Thanks for playing kub!")
                break
    
    def analyze_agent_strategy(self, num_games: int = 100):
        """Analyze the trained agent's strategy by examining move patterns."""
        print("Analyzing Agent Strategy")
        print("=" * 30)
        
        # Play games and collect move data
        move_patterns = {}
        opening_moves = []
        
        for _ in range(num_games):
            game = TicTacToe()
            
            # Record opening move
            if not game.game_over:
                action = self.trained_agent.choose_action(game)
                opening_moves.append(action)
            
            # Play full game and record patterns
            while not game.game_over:
                state_key = game.get_state_key()
                action = self.trained_agent.choose_action(game)
                
                if state_key not in move_patterns:
                    move_patterns[state_key] = []
                move_patterns[state_key].append(action)
                
                game.make_move(action)
        
        # Analyze opening moves
        print("Opening Move Analysis:")
        opening_counts = {}
        for move in opening_moves:
            opening_counts[move] = opening_counts.get(move, 0) + 1
        
        for move, count in sorted(opening_counts.items()):
            percentage = count / len(opening_moves) * 100
            print(f"  Position {move}: {count} times ({percentage:.1f}%)")
        
        print(f"\nTotal unique states encountered: {len(move_patterns)}")
        
        # Show some interesting patterns
        print("\nSample Move Patterns:")
        for i, (state, moves) in enumerate(list(move_patterns.items())[:5]):
            print(f"  State {state}: {moves}")
    
    def demonstrate_ai_games(self, num_games: int = 3):
        """Demonstrate AI vs AI games with visualization."""
        print(f"AI vs AI Demonstration ({num_games} games)")
        print("=" * 40)
        
        for game_num in range(1, num_games + 1):
            print(f"Game {game_num}:")
            self.play_game(
                self.trained_agent, 
                self.trained_agent, 
                verbose=True,
                delay=1.0
            )


def main():
    """Main evaluation function."""
    evaluator = GameEvaluator("q_table.json")
    
    print("Q-Learning Tic-Tac-Toe AI Evaluation")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Evaluate vs Random Agent")
        print("2. Play Human vs AI")
        print("3. Analyze Agent Strategy")
        print("4. Demonstrate AI vs AI")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == '1':
            num_games = input("Number of games (default 1000): ").strip()
            num_games = int(num_games) if num_games else 1000
            evaluator.evaluate_vs_random(num_games)
            
        elif choice == '2':
            evaluator.play_human_vs_ai()
            
        elif choice == '3':
            evaluator.analyze_agent_strategy()
            
        elif choice == '4':
            evaluator.demonstrate_ai_games()
            
        elif choice == '5':
            print("Thank you for playing kub!")
            break
            
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
