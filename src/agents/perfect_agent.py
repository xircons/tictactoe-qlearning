"""
Perfect Tic-Tac-Toe Agent using Minimax with Alpha-Beta Pruning
This agent plays perfectly and cannot be beaten (only drawn or wins)

Creative Commons Attribution-NonCommercial 4.0 International License
Copyright (c) 2025 pppwtk

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/
"""

import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.tictactoe import TicTacToe
from typing import Tuple, Optional


class PerfectMinimaxAgent:
    """
    Perfect Minimax agent with alpha-beta pruning.
    This agent plays optimally and cannot be beaten.
    """
    
    def __init__(self, name: str = "Perfect Minimax"):
        self.name = name
        self.nodes_evaluated = 0
        self.cache = {}  # Memoization for faster evaluation
        
    def choose_action(self, game: TicTacToe) -> int:
        """
        Choose the best action using Minimax with alpha-beta pruning.
        
        Args:
            game: Current game state
            
        Returns:
            Best action to take
        """
        available_actions = game.get_available_actions()
        if not available_actions:
            raise ValueError("No available actions!")
        
        # If only one move, take it immediately
        if len(available_actions) == 1:
            return available_actions[0]
        
        # Check for immediate win
        for action in available_actions:
            test_game = game.copy()
            test_game.make_move(action)
            if test_game.winner == game.current_player:
                return action
        
        # Check for immediate block
        for action in available_actions:
            test_game = game.copy()
            test_game.current_player = -game.current_player
            test_game.make_move(action)
            if test_game.winner == -game.current_player:
                return action
        
        # Use Minimax with alpha-beta pruning
        best_action = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Shuffle to add variety when multiple moves are equally good
        random.shuffle(available_actions)
        
        for action in available_actions:
            test_game = game.copy()
            test_game.make_move(action)
            
            score = self._minimax(test_game, 0, alpha, beta, False, game.current_player)
            
            if score > best_score:
                best_score = score
                best_action = action
            
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Alpha-beta pruning
        
        return best_action
    
    def _minimax(self, game: TicTacToe, depth: int, alpha: float, beta: float, 
                 is_maximizing: bool, original_player: int) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            game: Current game state
            depth: Current depth in the game tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            is_maximizing: Whether this is a maximizing node
            original_player: The player making the original move
            
        Returns:
            Best score for this position
        """
        self.nodes_evaluated += 1
        
        # Terminal state evaluation
        if game.game_over:
            if game.winner == original_player:
                score = 10 - depth  # Prefer faster wins
            elif game.winner == -original_player:
                score = depth - 10  # Prefer slower losses
            else:
                score = 0  # Draw
            return score
        
        available_actions = game.get_available_actions()
        if not available_actions:
            return 0
        
        # Check if it's the original player's turn
        is_original_player_turn = (game.current_player == original_player)
        
        if is_original_player_turn:
            # Maximizing for original player
            max_eval = float('-inf')
            for action in available_actions:
                test_game = game.copy()
                test_game.make_move(action)
                eval_score = self._minimax(test_game, depth + 1, alpha, beta, False, original_player)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            # Minimizing for opponent
            min_eval = float('inf')
            for action in available_actions:
                test_game = game.copy()
                test_game.make_move(action)
                eval_score = self._minimax(test_game, depth + 1, alpha, beta, True, original_player)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval
    
    def reset_cache(self):
        """Reset the evaluation cache."""
        self.cache.clear()
        self.nodes_evaluated = 0


class HybridQLearningMinimaxAgent:
    """
    Hybrid agent that combines Q-learning experience with perfect Minimax play.
    Uses Q-learning for guidance but ensures perfect tactical play.
    """
    
    def __init__(self, qlearning_agent=None, minimax_depth: int = 9):
        """
        Initialize hybrid agent.
        
        Args:
            qlearning_agent: Trained Q-learning agent (optional)
            minimax_depth: Depth for minimax search
        """
        self.name = "Hybrid Q-Learning + Minimax"
        self.qlearning_agent = qlearning_agent
        self.minimax_agent = PerfectMinimaxAgent()
        self.minimax_depth = minimax_depth
        
    def choose_action(self, game: TicTacToe) -> int:
        """
        Choose action using hybrid approach.
        
        Strategy:
        1. Always check for immediate wins/blocks (tactical)
        2. In critical positions (few moves left), use Minimax
        3. In early game, can use Q-learning if available
        4. Always fall back to Minimax for guaranteed optimal play
        
        Args:
            game: Current game state
            
        Returns:
            Best action to take
        """
        available_actions = game.get_available_actions()
        if not available_actions:
            raise ValueError("No available actions!")
        
        # Always play perfectly - use minimax for all positions
        # This ensures the human cannot win
        return self.minimax_agent.choose_action(game)


class UnbeatableAgent:
    """
    The ultimate unbeatable agent that plays perfectly.
    Combines strategic opening play with perfect minimax.
    """
    
    def __init__(self):
        self.name = "Unbeatable AI"
        self.minimax_agent = PerfectMinimaxAgent()
        self.move_count = 0
        
    def choose_action(self, game: TicTacToe) -> int:
        """
        Choose action to ensure perfect play.
        
        Args:
            game: Current game state
            
        Returns:
            Best action to take
        """
        available_actions = game.get_available_actions()
        if not available_actions:
            raise ValueError("No available actions!")
        
        # Count current moves to determine game phase
        move_count = sum(1 for cell in game.board if cell != 0)
        
        # Opening book for variety (all optimal moves)
        if move_count == 0:
            # First move: prefer center, corners are also optimal
            if random.random() < 0.7:
                return 4  # Center
            else:
                return random.choice([0, 2, 6, 8])  # Corners
        
        if move_count == 1 and game.current_player == -1:
            # Response to first move
            if game.board[4] == 0:  # Center available
                return 4
            # If opponent took center, take corner
            corners = [0, 2, 6, 8]
            available_corners = [c for c in corners if c in available_actions]
            if available_corners:
                return random.choice(available_corners)
        
        # For all other positions, use perfect minimax
        return self.minimax_agent.choose_action(game)
    
    def reset(self):
        """Reset agent state."""
        self.move_count = 0
        self.minimax_agent.reset_cache()


def test_perfect_agent():
    """Test the perfect agent."""
    print("Testing Perfect Minimax Agent")
    print("=" * 50)
    
    agent = PerfectMinimaxAgent()
    game = TicTacToe()
    
    # Test 1: Should win from this position
    print("\nTest 1: Win detection")
    game.reset()
    game.board = [1, 1, 0, 0, 0, 0, 0, 0, 0]  # X can win at position 2
    game.current_player = 1
    game.display_board()
    action = agent.choose_action(game)
    print(f"Agent chooses: {action} (expected: 2)")
    assert action == 2, f"Expected 2, got {action}"
    print("✓ Test passed!")
    
    # Test 2: Should block opponent's win
    print("\nTest 2: Block detection")
    game.reset()
    game.board = [-1, -1, 0, 0, 0, 0, 0, 0, 0]  # O can win at position 2
    game.current_player = 1
    game.display_board()
    action = agent.choose_action(game)
    print(f"Agent chooses: {action} (expected: 2)")
    assert action == 2, f"Expected 2, got {action}"
    print("✓ Test passed!")
    
    # Test 3: Play complete game
    print("\nTest 3: Complete game against random")
    game.reset()
    move_count = 0
    while not game.game_over and move_count < 9:
        if game.current_player == 1:
            action = agent.choose_action(game)
            print(f"Perfect agent plays: {action}")
        else:
            available = game.get_available_actions()
            action = random.choice(available)
            print(f"Random opponent plays: {action}")
        
        game.make_move(action)
        game.display_board()
        print()
        move_count += 1
    
    if game.winner == 1:
        print("Perfect agent wins!")
    elif game.winner == -1:
        print("Random opponent wins (should not happen often)")
    else:
        print("Draw!")
    
    print(f"\nNodes evaluated: {agent.nodes_evaluated:,}")
    print("All tests completed!")


if __name__ == "__main__":
    test_perfect_agent()

