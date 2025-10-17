# Tic-Tac-Toe AI - Unbeatable Edition

A Tic-Tac-Toe game with a **perfect AI** that uses Minimax algorithm. This AI never loses - you can only draw at best!

## Features

- **Perfect AI**: Uses Minimax with alpha-beta pruning (0% loss rate)
- **Friendly UI**: Entertaining messages that make the game fun
- **Simple Menu**: Play, Watch Demo, or Exit
- **Thoroughly Tested**: 0 losses in 1,500+ test games

## Quick Start

```bash
# Clone and setup
git clone https://github.com/xircons/tictactoe-qlearning.git
cd tictactoe-qlearning
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Play the game
python3 scripts/demo/play.py
```

## Usage

### Main Game
```bash
python3 scripts/demo/play.py
```

**Menu Options:**
1. **Play vs UNBEATABLE AI** - Challenge the perfect AI
2. **Watch AI vs AI Demo** - See the AI play itself  
3. **Exit** - Leave the game

### Alternative Entry Point
```bash
python3 main.py play
```

## How It Works

The AI uses **Minimax algorithm** with:
- Complete game tree search
- Alpha-beta pruning for speed
- Immediate win/block detection
- Optimal move selection

**Result**: Mathematically impossible to beat!

## Project Structure

```
tictactoe-qlearning/
├── src/
│   ├── agents/
│   │   ├── perfect_agent.py      # Unbeatable Minimax AI
│   │   └── qlearning_agent.py    # Q-Learning AI
│   ├── core/
│   │   └── tictactoe.py          # Game engine
│   └── training/
│       └── train.py              # Q-Learning training
├── scripts/demo/
│   ├── play.py                   # Main game
│   └── demo.py                   # AI vs AI
├── tests/
│   ├── test_perfect_agent.py    # AI tests
│   └── test_tictactoe.py        # Game tests
└── main.py                       # CLI entry
```

## Test Results

- **1,000 games vs Random**: 919 wins, 81 draws, **0 losses**
- **500 games vs Heuristic**: 18 wins, 482 draws, **0 losses**
- **100 games vs Perfect AI**: 100% draws (as expected)

## Tips for Getting a Draw

1. Take center (4) or corner (0,2,6,8) first
2. Always block threats immediately  
3. Never give AI fork opportunities
4. Think ahead 2-3 moves
5. Play perfectly (any mistake = you lose)

## Technologies

- Python 3.8+
- NumPy
- Matplotlib & Seaborn (for analytics)
- PyYAML

## Optional: Train Q-Learning Agent

```bash
python3 src/training/train.py
```

## Run Tests

```bash
python3 tests/test_perfect_agent.py
python3 tests/test_tictactoe.py
```

## License

Creative Commons Attribution-NonCommercial 4.0 International License

Copyright (c) 2025 pppwtk

This work is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/

## Challenge

Think you can win? **You can't.** But try anyway:

```bash
python3 scripts/demo/play.py
```

The best you'll do is a draw. Good luck!
