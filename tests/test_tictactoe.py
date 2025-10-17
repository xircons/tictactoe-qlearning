"""
Unit Tests for Tic-Tac-Toe Q-Learning AI

Tests cover:
- Game logic and win/draw detection
- Canonicalization and symmetry reduction
- Q-learning agent updates
- Basic functionality
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tictactoe import TicTacToe
from qlearning_agent import UltraAdvancedQLearningAgent


class TestTicTacToe(unittest.TestCase):
    """Test Tic-Tac-Toe game engine functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.game = TicTacToe()
    
    def test_initial_state(self):
        """Test initial game state."""
        self.assertEqual(self.game.board, [0] * 9)
        self.assertEqual(self.game.current_player, 1)
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
    
    def test_available_actions(self):
        """Test available actions detection."""
        actions = self.game.get_available_actions()
        self.assertEqual(set(actions), set(range(9)))
        
        # Make a move
        self.game.make_move(0)
        actions = self.game.get_available_actions()
        self.assertEqual(len(actions), 8)
        self.assertNotIn(0, actions)
    
    def test_win_detection_rows(self):
        """Test win detection for rows."""
        # Test first row win
        self.game.board = [1, 1, 1, 0, 0, 0, 0, 0, 0]
        self.game.current_player = 1
        self.assertTrue(self.game.check_winner())
        
        # Test second row win
        self.game.board = [0, 0, 0, -1, -1, -1, 0, 0, 0]
        self.game.current_player = -1
        self.assertTrue(self.game.check_winner())
    
    def test_win_detection_columns(self):
        """Test win detection for columns."""
        # Test first column win
        self.game.board = [1, 0, 0, 1, 0, 0, 1, 0, 0]
        self.game.current_player = 1
        self.assertTrue(self.game.check_winner())
        
        # Test second column win
        self.game.board = [0, -1, 0, 0, -1, 0, 0, -1, 0]
        self.game.current_player = -1
        self.assertTrue(self.game.check_winner())
    
    def test_win_detection_diagonals(self):
        """Test win detection for diagonals."""
        # Test main diagonal win
        self.game.board = [1, 0, 0, 0, 1, 0, 0, 0, 1]
        self.game.current_player = 1
        self.assertTrue(self.game.check_winner())
        
        # Test anti-diagonal win
        self.game.board = [0, 0, -1, 0, -1, 0, -1, 0, 0]
        self.game.current_player = -1
        self.assertTrue(self.game.check_winner())
    
    def test_draw_detection(self):
        """Test draw detection."""
        # Create a draw scenario
        self.game.board = [1, -1, 1, -1, 1, -1, -1, 1, -1]
        self.game.current_player = 1
        self.assertFalse(self.game.check_winner())
        
        # Check if game is over (no available moves)
        actions = self.game.get_available_actions()
        self.assertEqual(len(actions), 0)
    
    def test_canonical_state(self):
        """Test canonical state representation."""
        # Test empty board
        canonical = self.game.get_canonical_state()
        self.assertIsInstance(canonical, str)
        
        # Test with moves
        self.game.make_move(0)  # X at position 0
        canonical = self.game.get_canonical_state()
        self.assertIsInstance(canonical, str)
        self.assertIn('1', canonical)  # Should contain current player's move
    
    def test_symmetry_reduction(self):
        """Test symmetry reduction functionality."""
        # Create symmetric boards
        board1 = [1, 0, 0, 0, 0, 0, 0, 0, 0]  # Corner
        board2 = [0, 0, 1, 0, 0, 0, 0, 0, 0]  # Rotated corner
        
        self.game.board = board1
        self.game.current_player = 1
        canonical1 = self.game.get_canonical_state()
        
        self.game.board = board2
        canonical2 = self.game.get_canonical_state()
        
        # Should be the same canonical state due to symmetry
        self.assertEqual(canonical1, canonical2)


class TestQLearningAgent(unittest.TestCase):
    """Test Q-Learning agent functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.agent = UltraAdvancedQLearningAgent()
        self.game = TicTacToe()
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        self.assertEqual(self.agent.alpha_start, 0.1)
        self.assertEqual(self.agent.alpha_end, 0.01)
        self.assertEqual(self.agent.gamma, 0.99)
        self.assertEqual(self.agent.epsilon_start, 1.0)
        self.assertEqual(self.agent.epsilon_end, 0.001)
    
    def test_epsilon_decay(self):
        """Test epsilon decay calculation."""
        # Test initial epsilon
        epsilon = self.agent.get_epsilon()
        self.assertEqual(epsilon, 1.0)
        
        # Simulate some steps
        self.agent.total_steps = 100000
        epsilon = self.agent.get_epsilon()
        self.assertLess(epsilon, 1.0)
        self.assertGreater(epsilon, 0.0)
    
    def test_alpha_decay(self):
        """Test learning rate decay calculation."""
        # Test initial alpha
        alpha = self.agent.get_alpha()
        self.assertEqual(alpha, 0.1)
        
        # Simulate some steps
        self.agent.total_steps = 100000
        alpha = self.agent.get_alpha()
        self.assertLess(alpha, 0.1)
        self.assertGreater(alpha, 0.0)
    
    def test_q_value_updates(self):
        """Test Q-value update functionality."""
        state_key = "[0, 0, 0, 0, 0, 0, 0, 0, 0]"
        action = 0
        reward = 1.0
        next_state_key = "[1, 0, 0, 0, 0, 0, 0, 0, 0]"
        
        # Initial Q-value should be 0
        q_values = self.agent.get_combined_q_values(state_key)
        initial_q = q_values[action]
        
        # Update Q-value
        self.agent.update_q_value(state_key, action, reward, next_state_key)
        
        # Q-value should have changed
        q_values = self.agent.get_combined_q_values(state_key)
        updated_q = q_values[action]
        self.assertNotEqual(initial_q, updated_q)
    
    def test_action_selection(self):
        """Test action selection functionality."""
        # Test with empty board
        action = self.agent.choose_action(self.game)
        self.assertIn(action, range(9))
        
        # Test with some moves made
        self.game.make_move(0)
        self.game.make_move(1)
        action = self.agent.choose_action(self.game)
        available_actions = self.game.get_available_actions()
        self.assertIn(action, available_actions)
    
    def test_tactical_intelligence(self):
        """Test tactical intelligence (win/block detection)."""
        # Test win detection
        self.game.board = [1, 1, 0, 0, 0, 0, 0, 0, 0]
        self.game.current_player = 1
        tactical_action = self.agent.check_immediate_win_or_block(self.game)
        self.assertEqual(tactical_action, 2)  # Should win at position 2
        
        # Test block detection
        self.game.board = [-1, -1, 0, 0, 0, 0, 0, 0, 0]
        self.game.current_player = 1
        tactical_action = self.agent.check_immediate_win_or_block(self.game)
        self.assertEqual(tactical_action, 2)  # Should block at position 2


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def test_complete_game_simulation(self):
        """Test complete game simulation."""
        agent = UltraAdvancedQLearningAgent()
        game = TicTacToe()
        
        # Simulate a complete game
        moves = 0
        while not game.game_over and moves < 9:
            action = agent.choose_action(game)
            game.make_move(action)
            moves += 1
        
        # Game should be over
        self.assertTrue(game.game_over)
        
        # Should have a winner or be a draw
        self.assertTrue(game.winner is not None or len(game.get_available_actions()) == 0)
    
    def test_q_table_persistence(self):
        """Test Q-table save/load functionality."""
        agent = UltraAdvancedQLearningAgent()
        
        # Train agent a bit
        for _ in range(10):
            game = TicTacToe()
            agent.train_episode(game)
        
        # Save Q-table
        test_file = "test_q_table.json"
        agent.save_q_table(test_file)
        
        # Create new agent and load Q-table
        new_agent = UltraAdvancedQLearningAgent()
        new_agent.load_q_table(test_file)
        
        # Q-tables should be similar
        self.assertEqual(len(agent.q_table_a), len(new_agent.q_table_a))
        
        # Clean up
        import os
        if os.path.exists(test_file):
            os.remove(test_file)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
