import time
from tictactoe import TicTacToe
from qlearning_agent import UltraAdvancedQLearningAgent


def demonstrate_ai_vs_ai(num_games=3):
    """Demonstrate AI vs AI games with console visualization."""
    
    # Load trained agent
    agent = UltraAdvancedQLearningAgent()
    agent.load_q_table("q_table.json")
    
    print("AI vs AI Tic-Tac-Toe Demonstration")
    print("=" * 50)
    print(f"Showing {num_games} games with 3x3 grid visualization")
    print("Both players are using the trained Q-learning agent")
    print()
    
    for game_num in range(1, num_games + 1):
        print(f"GAME {game_num}")
        print("-" * 20)
        
        # Create new game
        game = TicTacToe()
        move_count = 0
        
        # Show initial board
        print("Starting board:")
        game.display_board()
        print()
        
        # Play the game
        while not game.game_over:
            move_count += 1
            player_symbol = 'X' if game.current_player == 1 else 'O'
            player_number = 1 if game.current_player == 1 else 2
            
            print(f"Move {move_count}: Player {player_number} ({player_symbol})'s turn")
            
            # AI chooses action
            action = agent.choose_action(game)
            game.make_move(action)
            
            print(f"Player {player_number} ({player_symbol}) plays")
            game.display_board()
            print()
            
            # Add small delay for better visualization
            time.sleep(0.5)
        
        # Game finished
        print("GAME OVER!")
        if game.winner == 1:
            print("Player 1 (X) wins!")
        elif game.winner == -1:
            print("Player 2 (O) wins!")
        else:
            print("It's a draw!")
        
        print(f"Total moves: {move_count}")
        print("=" * 50)
        print()
        
        # Pause between games
        if game_num < num_games:
            time.sleep(1)


if __name__ == "__main__":
    demonstrate_ai_vs_ai(3)
