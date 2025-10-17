## Tic-Tac-Toe Q-Learning AI System

> This project transforms a simple 3×3 grid into a sophisticated artificial intelligence demonstration that showcases the evolution from basic games to advanced machine learning systems. At its core lies an Ultra-Advanced Q-Learning agent employing cutting-edge techniques including double Q-learning for stability, Dyna-Q for simulated experience learning, and experience replay with prioritized sampling. The system transcends traditional trial-and-error learning by incorporating tactical intelligence with immediate win/block detection, strategic position preferences, and MCTS-style evaluation for complex endgame positions.
The brilliance of this implementation lies in its symmetry reduction technique, which recognizes that rotated boards represent identical strategic situations. By canonicalizing game states, the AI learns more efficiently, transforming thousands of possibilities into meaningful patterns that reflect a deeper understanding of how intelligence emerges from structured learning processes. This optimization demonstrates how simple rules can generate sophisticated behaviors through systematic exploration and adaptation.
Beyond pure AI research, the project evolves into a complete production-ready ecosystem featuring a Flask backend that serves the trained model via RESTful APIs, a modern web frontend providing engaging gameplay experiences, and intelligent fallback systems that ensure continuous operation. When the Q-learning API becomes unavailable, the system seamlessly switches to perfect minimax algorithms, showcasing robust system design principles.
The project exemplifies how derived values flow through complex interconnected systems, where each component—from the game engine's state representation to the Q-learning agent's strategic preferences emerging from thousands of self-play games—contributes to a greater whole. The configurable training system supports multiple modes ranging from quick 10,000-episode runs to intensive 100,000-episode sessions, complete with comprehensive analytics, real-time performance tracking, and convergence analysis that transforms raw training data into meaningful insights about AI learning processes.
This multi-layered architecture demonstrates contemporary AI development practices, showcasing everything from low-level game mechanics to high-level user interfaces. The project proves that even elementary games can illuminate the deepest principles of artificial intelligence, serving as both an educational tool and practical demonstration of how modern machine learning techniques can be applied to create intelligent systems that are theoretically sound and practically useful in real-world applications.

## Demo

<div align="center">
  <img src="tictactoe-qlearning.gif" alt="Tic-Tac-Toe Q-Learning AI Demo" />
</div>

## Folder Structure

```
tictactoe-qlearning/
├── src/                           # Core AI implementation
│   ├── agents/                    # AI agents
│   │   ├── qlearning_agent.py     # Ultra-Advanced Q-Learning agent
│   │   ├── perfect_agent.py       # Perfect Minimax agent
│   │   └── baseline_agents.py     # Random & heuristic agents
│   ├── core/                      # Game engine
│   │   └── tictactoe.py          # Tic-tac-toe game logic
│   ├── training/                  # Training system
│   │   └── train.py              # Self-play training loop
│   └── config.yaml               # Training configuration
├── backend/                       # Flask API server
│   ├── agents/
│   │   └── perfect_agent.py      # API agent implementation
│   ├── core/
│   │   └── tictactoe.py         # Game engine for API
│   └── main.py                   # Flask server
├── frontend/                      # Web interface
│   └── public/
│       ├── index.html            # Main HTML file
│       ├── css/
│       │   └── styles.css        # Styling
│       └── js/
│           ├── config.js         # API configuration
│           └── game.js           # Game logic
├── requirements.txt              # Python dependencies
├── config.env                    # Environment variables
└── README.md                     # This file
```

## Frontend Setup

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Quick Start
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd tictactoe-qlearning
   ```

2. **Open the game**
   - **Option 1**: Open `frontend/public/index.html` directly in your browser
   - **Option 2**: Use a local server for better development experience:
     ```bash
     # Using Python
     cd frontend/public
     python -m http.server 8000
     # Then visit http://localhost:8000
     
     # Using Node.js (if you have it)
     npx serve frontend/public
     ```

3. **Start playing!**
   - Enter your name
   - Play against the AI
   - The frontend will automatically connect to the backend API if available

### Features
- **Responsive design** with modern UI/UX
- **Real-time gameplay** with AI opponent
- **Score tracking** and game statistics
- **Automatic fallback** to random AI if backend is unavailable
- **Cross-platform compatibility** (works on GitHub Pages and locally)

## Backend Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation & Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment** (optional)
   ```bash
   # Edit config.env if needed
   # Default settings work out of the box
   ```

3. **Start the Flask server**
   ```bash
   # From the project root
   python backend/main.py
   
   # Or specify a custom port
   PORT=5001 python backend/main.py
   ```

4. **Verify the API is running**
   ```bash
   # Test the health endpoint
   curl http://localhost:5001/api/health
   
   # Expected response:
   # {"status": "healthy", "message": "Tic-Tac-Toe API is running", "agent": "Perfect Minimax AI"}
   ```

### Training the Q-Learning Agent

1. **Configure training parameters**
   ```bash
   # Edit src/config.yaml for custom settings
   # Default: 50,000 episodes with parallel processing
   ```

2. **Start training**
   ```bash
   python src/training/train.py
   ```

3. **Monitor progress**
   - Real-time statistics every 1,000 episodes
   - Automatic Q-table saving every 5,000 episodes
   - Performance plots generated automatically

4. **Use trained model**
   - Trained Q-table saved as `q_table.json`
   - Can be loaded by the Q-learning agent for gameplay

## License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License**.

Copyright (c) 2025 pppwtk

For full license details, see [LICENSE](LICENSE) file.