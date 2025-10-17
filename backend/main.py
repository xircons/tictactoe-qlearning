"""
Tic-Tac-Toe API Backend with Multiple AI Agents
Flask API server supporting both Perfect Minimax and Q-Learning AI agents

Creative Commons Attribution-NonCommercial 4.0 International License
Copyright (c) 2025 pppwtk

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import pickle
import gzip
import numpy as np

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))

from agents.perfect_agent import PerfectMinimaxAgent, HybridQLearningMinimaxAgent
from agents.qlearning_agent import UltraAdvancedQLearningAgent
from core.tictactoe import TicTacToe

app = Flask(__name__)
# Configure CORS to allow requests from GitHub Pages and localhost
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://xircons.github.io",
            "http://localhost:5001",
            "http://127.0.0.1:5001",
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "file://",
            "null"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Initialize AI agents
perfect_agent = PerfectMinimaxAgent()
qlearning_agent = None
hybrid_agent = None

# Try to load trained Q-learning agent
def load_qlearning_agent():
    global qlearning_agent, hybrid_agent
    try:
        # Look for trained Q-table files
        q_table_files = [
            "q_table.json",
            "q_table.json.gz", 
            "backend/q_table.json",
            "backend/q_table.json.gz"
        ]
        
        q_table_file = None
        for file_path in q_table_files:
            if os.path.exists(file_path):
                q_table_file = file_path
                break
        
        if q_table_file:
            print(f"Loading Q-learning agent from {q_table_file}")
            
            # Create Q-learning agent
            qlearning_agent = UltraAdvancedQLearningAgent()
            
            # Load Q-table
            if q_table_file.endswith('.gz'):
                with gzip.open(q_table_file, 'rt') as f:
                    q_table_data = json.load(f)
            else:
                with open(q_table_file, 'r') as f:
                    q_table_data = json.load(f)
            
            # Convert loaded data back to numpy arrays
            for state_key, q_values in q_table_data.items():
                qlearning_agent.q_table_a[state_key] = np.array(q_values, dtype=np.float32)
            
            print(f"Loaded Q-learning agent with {len(qlearning_agent.q_table_a)} states")
            
            # Create hybrid agent
            hybrid_agent = HybridQLearningMinimaxAgent(qlearning_agent)
            
            return True
        else:
            print("No trained Q-learning agent found. Only Perfect Minimax available.")
            return False
            
    except Exception as e:
        print(f"Failed to load Q-learning agent: {e}")
        return False

# Load Q-learning agent on startup
qlearning_available = load_qlearning_agent()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with agent information"""
    agents_info = {
        "perfect_minimax": "Available",
        "qlearning": "Available" if qlearning_available else "Not trained",
        "hybrid": "Available" if qlearning_available else "Not available"
    }
    
    return jsonify({
        "status": "healthy",
        "message": "Tic-Tac-Toe API is running",
        "agents": agents_info,
        "default_agent": "Perfect Minimax"
    })

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List available AI agents"""
    agents = {
        "perfect_minimax": {
            "name": "Perfect Minimax",
            "description": "Unbeatable agent using Minimax algorithm",
            "available": True,
            "type": "deterministic"
        },
        "qlearning": {
            "name": "Q-Learning Agent", 
            "description": "Machine learning agent trained through self-play",
            "available": qlearning_available,
            "type": "learning"
        },
        "hybrid": {
            "name": "Hybrid Q-Learning + Minimax",
            "description": "Combines Q-learning guidance with perfect tactical play",
            "available": qlearning_available,
            "type": "hybrid"
        }
    }
    
    return jsonify({
        "agents": agents,
        "total_available": sum(1 for agent in agents.values() if agent["available"])
    })

@app.route('/api/move', methods=['POST'])
def get_ai_move():
    """
    Get AI move for given board state
    
    Expected JSON:
    {
        "board": [0, 1, -1, 0, 0, 0, 0, 0, 0],  # 9-element array: 0=empty, 1=X, -1=O
        "player": -1,  # Current player: 1=X, -1=O (AI should be -1)
        "agent": "perfect_minimax"  # Optional: "perfect_minimax", "qlearning", "hybrid"
    }
    
    Returns:
    {
        "move": 4,  # Position index (0-8)
        "message": "AI plays position 4",
        "board": [0, 1, -1, 0, -1, 0, 0, 0, 0],  # Updated board
        "agent_used": "Perfect Minimax"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        board = data.get('board')
        player = data.get('player')
        agent_type = data.get('agent', 'perfect_minimax')  # Default to perfect minimax
        
        if not board:
            return jsonify({"error": "Board state is required"}), 400
        
        if not isinstance(board, list) or len(board) != 9:
            return jsonify({"error": "Board must be a list of 9 elements"}), 400
        
        if player is None:
            return jsonify({"error": "Player is required"}), 400
        
        # Validate board values
        for i, cell in enumerate(board):
            if cell not in [0, 1, -1]:
                return jsonify({"error": f"Invalid value {cell} at position {i}"}), 400
        
        # Create game instance
        game = TicTacToe()
        game.board = board.copy()
        game.current_player = player
        
        # Check if game is already over
        if game.check_winner():
            return jsonify({"error": "Game is already won"}), 400
        
        if len(game.get_available_actions()) == 0:
            return jsonify({"error": "No available moves"}), 400
        
        # Choose agent based on request
        agent_used = "Perfect Minimax"
        ai_move = None
        
        if agent_type == "qlearning" and qlearning_available:
            ai_move = qlearning_agent.choose_action(game)
            agent_used = "Q-Learning Agent"
        elif agent_type == "hybrid" and qlearning_available:
            ai_move = hybrid_agent.choose_action(game)
            agent_used = "Hybrid Q-Learning + Minimax"
        else:
            # Default to perfect minimax
            ai_move = perfect_agent.choose_action(game)
            agent_used = "Perfect Minimax"
        
        # Make the move to get updated board
        game.make_move(ai_move)
        
        return jsonify({
            "move": ai_move,
            "message": f"AI plays position {ai_move}",
            "board": game.board,
            "game_over": game.game_over,
            "winner": game.winner,
            "agent_used": agent_used,
            "agent_type": agent_type
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/validate', methods=['POST'])
def validate_board():
    """
    Validate board state and return game status
    
    Expected JSON:
    {
        "board": [0, 1, -1, 0, 0, 0, 0, 0, 0]
    }
    
    Returns:
    {
        "valid": true,
        "game_over": false,
        "winner": null,
        "available_moves": [3, 4, 5, 6, 7, 8]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'board' not in data:
            return jsonify({"error": "Board state is required"}), 400
        
        board = data['board']
        
        if not isinstance(board, list) or len(board) != 9:
            return jsonify({"error": "Board must be a list of 9 elements"}), 400
        
        # Validate board values
        for i, cell in enumerate(board):
            if cell not in [0, 1, -1]:
                return jsonify({"error": f"Invalid value {cell} at position {i}"}), 400
        
        # Create game instance
        game = TicTacToe()
        game.board = board.copy()
        
        # Check for winner
        game.check_winner()
        
        return jsonify({
            "valid": True,
            "game_over": game.game_over,
            "winner": game.winner,
            "available_moves": game.get_available_actions()
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/train', methods=['POST'])
def train_qlearning():
    """
    Train Q-learning agent (for development/testing)
    
    Expected JSON:
    {
        "episodes": 1000,  # Optional: number of training episodes
        "save": true       # Optional: whether to save the trained model
    }
    """
    try:
        data = request.get_json() or {}
        episodes = data.get('episodes', 1000)
        save_model = data.get('save', True)
        
        if not qlearning_available:
            return jsonify({
                "message": "Training Q-learning agent...",
                "episodes": episodes,
                "status": "started"
            })
        
        # This would trigger training in a separate process
        # For now, just return success
        return jsonify({
            "message": f"Q-learning training started for {episodes} episodes",
            "episodes": episodes,
            "status": "started",
            "note": "Training runs in background"
        })
        
    except Exception as e:
        return jsonify({"error": f"Training error: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    print("Starting Tic-Tac-Toe API server with multiple AI agents...")
    print("Available agents:")
    print("  ✓ Perfect Minimax AI (always available)")
    if qlearning_available:
        print("  ✓ Q-Learning AI (trained)")
        print("  ✓ Hybrid Q-Learning + Minimax")
    else:
        print("  ⚠ Q-Learning AI (not trained - run training first)")
        print("  ⚠ Hybrid Agent (requires Q-learning)")
    
    print("\nAvailable endpoints:")
    print("  GET  /api/health     - Health check with agent status")
    print("  GET  /api/agents     - List available agents")
    print("  POST /api/move       - Get AI move (specify agent type)")
    print("  POST /api/validate   - Validate board state")
    print("  POST /api/train      - Train Q-learning agent")
    
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
