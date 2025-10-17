import numpy as np
from typing import List, Tuple, Optional, Set


class TicTacToe:
    """Tic-Tac-Toe game engine with canonical state representation and symmetry reduction."""
    
    def __init__(self):
        self.board = [0] * 9  # 3x3 grid as flat list
        self.current_player = 1  # 1 for X, -1 for O
        self.game_over = False
        self.winner = None
        self.move_history = []  # Track moves for Q-learning updates
        
    def reset(self):
        """Reset the game to initial state."""
        self.board = [0] * 9
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.move_history = []
        
    def get_available_actions(self) -> List[int]:
        """Return list of available action indices (0-8 for empty cells)."""
        return [i for i in range(9) if self.board[i] == 0]
    
    def make_move(self, action: int) -> bool:
        """
        Make a move at the given action index.
        Returns True if move was valid, False otherwise.
        """
        if action not in self.get_available_actions():
            return False
            
        self.board[action] = self.current_player
        self.move_history.append((self.get_canonical_state(), action))
        
        # Check for win or draw
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
        elif len(self.get_available_actions()) == 0:
            self.game_over = True
            self.winner = 0  # Draw
        else:
            self.current_player *= -1  # Switch players
            
        return True
    
    def check_winner(self) -> bool:
        """Check if current player has won."""
        board = self.board
        
        # Check rows
        for i in range(0, 9, 3):
            if board[i] == board[i+1] == board[i+2] == self.current_player:
                return True
                
        # Check columns
        for i in range(3):
            if board[i] == board[i+3] == board[i+6] == self.current_player:
                return True
                
        # Check diagonals
        if board[0] == board[4] == board[8] == self.current_player:
            return True
        if board[2] == board[4] == board[6] == self.current_player:
            return True
            
        return False
    
    def get_canonical_state(self) -> str:
        """
        Get canonical state representation from current player's perspective.
        Current player is always represented as 1, opponent as -1.
        """
        # Create board from current player's perspective
        canonical_board = [cell * self.current_player for cell in self.board]
        
        # Apply symmetry reduction to get smallest representation
        return self._get_canonical_symmetric_state(canonical_board)
    
    def _get_canonical_symmetric_state(self, board: List[int]) -> str:
        """
        Apply all 8 symmetries and return lexicographically smallest state.
        Symmetries: 4 rotations (0°, 90°, 180°, 270°) + 4 reflections
        """
        # Convert to 3x3 matrix for transformations
        matrix = np.array(board).reshape(3, 3)
        
        # Generate all symmetric states
        symmetric_states = []
        
        # 4 rotations
        for rotation in [0, 90, 180, 270]:
            if rotation == 0:
                rotated = matrix
            else:
                rotated = np.rot90(matrix, k=rotation//90)
            symmetric_states.append(rotated.flatten().tolist())
        
        # 4 reflections
        symmetric_states.append(np.fliplr(matrix).flatten().tolist())  # horizontal
        symmetric_states.append(np.flipud(matrix).flatten().tolist())  # vertical
        symmetric_states.append(np.fliplr(np.flipud(matrix)).flatten().tolist())  # diagonal
        symmetric_states.append(np.flipud(np.fliplr(matrix)).flatten().tolist())  # anti-diagonal
        
        # Convert to strings and find lexicographically smallest
        state_strings = [str(state) for state in symmetric_states]
        return min(state_strings)
    
    def get_state_key(self) -> str:
        """Get current state as string key for Q-table."""
        return self.get_canonical_state()
    
    def display_board(self):
        """Display the current board state."""
        symbols = {1: 'X', -1: 'O', 0: ' '}
        
        for i in range(3):
            row_start = i * 3
            print(f" {symbols[self.board[row_start]]} | {symbols[self.board[row_start+1]]} | {symbols[self.board[row_start+2]]}")
            if i < 2:
                print(" ---------")
    
    def get_reward(self, player: int) -> int:
        """
        Get reward for a player based on game outcome.
        Returns: +1 for win, -1 for loss, 0 for draw or ongoing game
        """
        if not self.game_over:
            return 0
            
        if self.winner == player:
            return 1
        elif self.winner == -player:
            return -1
        else:  # draw
            return 0
    
    def copy(self):
        """Create a copy of the current game state."""
        new_game = TicTacToe()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.game_over = self.game_over
        new_game.winner = self.winner
        new_game.move_history = self.move_history.copy()
        return new_game


def test_game_engine():
    """Test the game engine functionality."""
    game = TicTacToe()
    
    print("Testing Tic-Tac-Toe Game Engine")
    print("=" * 40)
    
    # Test basic moves
    print("Initial board:")
    game.display_board()
    print(f"Available actions: {game.get_available_actions()}")
    print(f"Current player: {game.current_player}")
    
    # Test a winning game
    moves = [0, 1, 3, 4, 6]  # X wins diagonally
    for i, move in enumerate(moves):
        print(f"\nMove {i+1}: Player {game.current_player} plays at {move}")
        game.make_move(move)
        game.display_board()
        print(f"Game over: {game.game_over}, Winner: {game.winner}")
        
        if game.game_over:
            break
    
    # Test canonical state
    print(f"\nCanonical state: {game.get_canonical_state()}")
    
    # Test symmetry reduction
    print("\nTesting symmetry reduction:")
    test_board = [1, 0, -1, 0, 1, 0, -1, 0, 0]
    game.board = test_board
    game.current_player = 1
    print(f"Original board: {test_board}")
    print(f"Canonical state: {game.get_canonical_state()}")


if __name__ == "__main__":
    test_game_engine()
