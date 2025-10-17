# Tic-Tac-Toe with Perfect AI

A modern, pixel-art styled Tic-Tac-Toe game featuring an unbeatable AI opponent powered by the Perfect Minimax algorithm. The game is deployed on GitHub Pages with a separate Python API backend.

**[>> Play the Game Now <<](https://xircons.github.io/tictactoe-qlearning/index.html)**

## Features

- **8-bit Pixel Art Design**: Retro gaming aesthetic with smooth animations
- **Perfect Minimax AI**: Unbeatable opponent that plays optimally
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time API Integration**: AI moves powered by Python backend
- **Fallback System**: Graceful degradation to random AI if API unavailable
- **Score Tracking**: Persistent score tracking across games
- **Modern UI/UX**: Smooth transitions and engaging visual feedback

## Project Structure

```
tictactoe-qlearning/
├── frontend/                 # Frontend application
│   └── public/              # Static files for GitHub Pages
│       ├── index.html      # Main HTML file
│       ├── css/            # Stylesheets
│       └── js/             # JavaScript files
├── backend/                 # Python API backend
│   ├── main.py             # Flask API server
│   ├── agents/             # AI agent implementations
│   ├── core/               # Game engine
│   └── requirements.txt    # Python dependencies
├── src/                    # Original Python source code
├── .github/workflows/      # GitHub Actions for deployment
└── deployment/             # Backend deployment configs
```

## Live Demo

- **Frontend**: [Play Game on GitHub Pages](https://xircons.github.io/tictactoe-qlearning/index.html)
- **API**: [Backend API](https://tictactoe-qlearning.onrender.com)

## Setup Instructions

### Frontend (GitHub Pages)

The frontend is automatically deployed to GitHub Pages when you push to the main branch.

1. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Source: GitHub Actions
   - The workflow will automatically deploy from `frontend/public`

2. **Update API URL**:
   - Edit `frontend/public/js/config.js`
   - Update `PRODUCTION_URL` with your deployed backend URL

### Backend API

#### Local Development

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python main.py
   ```

3. **Test the API**:
   ```bash
   curl http://localhost:5000/api/health
   ```

#### Production Deployment

Choose one of the following platforms:

##### Option 1: Render.com (Recommended)

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Use the configuration from `deployment/render.yaml`
4. Set environment variables as needed

##### Option 2: Railway

1. Connect your GitHub repository to Railway
2. Railway will auto-detect Python and install dependencies
3. Set environment variables in Railway dashboard

##### Option 3: Heroku

1. Install Heroku CLI
2. Create a new app:
   ```bash
   heroku create your-app-name
   ```
3. Deploy:
   ```bash
   git push heroku main
   ```

##### Option 4: DigitalOcean App Platform

1. Connect your GitHub repository
2. Set build command: `pip install -r backend/requirements.txt`
3. Set run command: `cd backend && gunicorn main:app`

## How to Play

1. **Start the Game**: Enter your name and click "START GAME"
2. **Make Moves**: Click on empty cells to place your X
3. **AI Response**: The Perfect Minimax AI will respond with optimal moves
4. **Win Conditions**: Get three in a row (horizontal, vertical, or diagonal)
5. **Game Over**: Win, lose, or draw - then play again!

## 🤖 AI Agent Details

The Perfect Minimax agent uses:
- **Alpha-Beta Pruning**: Optimized search algorithm
- **Tactical Intelligence**: Immediate win/block detection
- **Optimal Play**: Cannot be beaten (only drawn or wins)
- **Strategic Depth**: Evaluates all possible game states

## API Endpoints

### Health Check
```
GET /api/health
```

### Get AI Move
```
POST /api/move
Content-Type: application/json

{
    "board": [0, 1, -1, 0, 0, 0, 0, 0, 0],
    "player": -1
}
```

### Validate Board
```
POST /api/validate
Content-Type: application/json

{
    "board": [0, 1, -1, 0, 0, 0, 0, 0, 0]
}
```

## 🎨 Customization

### Styling
- Modify `frontend/public/css/styles.css` for visual changes
- CSS variables are defined in `:root` for easy theming

### AI Behavior
- Edit `backend/agents/perfect_agent.py` for AI modifications
- The agent can be configured for different difficulty levels

### API Configuration
- Update `frontend/public/js/config.js` for API endpoints
- Modify CORS settings in `backend/main.py` for domain restrictions

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your frontend domain is included in backend CORS origins
2. **API Not Available**: Check backend deployment and update config.js URL
3. **GitHub Pages Not Updating**: Verify GitHub Actions workflow is running
4. **Local Development**: Ensure backend is running on localhost:5000

### Debug Mode

Enable debug mode in the browser console to see API calls and responses.

## Development

### Adding Features

1. **Frontend**: Modify files in `frontend/public/`
2. **Backend**: Update `backend/main.py` and related files
3. **Testing**: Test locally before deploying

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Perfect Minimax algorithm implementation
- 8-bit pixel art styling inspiration
- Flask and modern web technologies
