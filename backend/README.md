# Tic-Tac-Toe API Backend

A Flask API server that provides an unbeatable AI opponent for Tic-Tac-Toe using the Perfect Minimax algorithm.

## Features

- **Perfect Minimax AI**: Unbeatable opponent that plays optimally
- **RESTful API**: Simple JSON endpoints for game interaction
- **CORS Support**: Configured for GitHub Pages deployment
- **Error Handling**: Comprehensive validation and error responses

## API Endpoints

### Health Check
```
GET /api/health
```
Returns API status and agent information.

### Get AI Move
```
POST /api/move
```
**Request:**
```json
{
    "board": [0, 1, -1, 0, 0, 0, 0, 0, 0],
    "player": -1
}
```

**Response:**
```json
{
    "move": 4,
    "message": "AI plays position 4",
    "board": [0, 1, -1, 0, -1, 0, 0, 0, 0],
    "game_over": false,
    "winner": null
}
```

### Validate Board
```
POST /api/validate
```
**Request:**
```json
{
    "board": [0, 1, -1, 0, 0, 0, 0, 0, 0]
}
```

**Response:**
```json
{
    "valid": true,
    "game_over": false,
    "winner": null,
    "available_moves": [3, 4, 5, 6, 7, 8]
}
```

## Board Representation

The board is represented as a 9-element array where:
- `0` = Empty cell
- `1` = X (Player)
- `-1` = O (AI)

Positions are indexed as:
```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

## Setup

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```

3. **Test the API:**
   ```bash
   curl http://localhost:5000/api/health
   ```

### Production Deployment

#### Option 1: Render.com

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn main:app`
5. Set environment variables as needed

#### Option 2: Railway

1. Connect your GitHub repository to Railway
2. Railway will auto-detect Python and install dependencies
3. Set environment variables in Railway dashboard

#### Option 3: Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn main:app
   ```

2. Deploy using Heroku CLI:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### Option 4: DigitalOcean App Platform

1. Connect your GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `gunicorn main:app`
4. Configure environment variables

## Environment Variables

- `FLASK_ENV`: Set to `production` for production deployment
- `PORT`: Port number (default: 5000)
- `HOST`: Host address (default: 0.0.0.0)

## CORS Configuration

The API is configured to accept requests from:
- GitHub Pages domains (`https://*.github.io`)
- Local development (`http://localhost:*`, `https://localhost:*`)

To add additional domains, modify the `CORS` configuration in `main.py`.

## Testing

Test the API endpoints using curl or any HTTP client:

```bash
# Health check
curl http://localhost:5000/api/health

# Get AI move
curl -X POST http://localhost:5000/api/move \
  -H "Content-Type: application/json" \
  -d '{"board": [1, 0, 0, 0, 0, 0, 0, 0, 0], "player": -1}'

# Validate board
curl -X POST http://localhost:5000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"board": [1, 0, 0, 0, 0, 0, 0, 0, 0]}'
```

## AI Agent Details

The Perfect Minimax agent:
- Uses alpha-beta pruning for optimal performance
- Always plays the best possible move
- Cannot be beaten (only drawn or wins)
- Evaluates all possible game states
- Provides tactical intelligence for immediate wins/blocks

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure your frontend domain is included in CORS origins
2. **Port Conflicts**: Change the port in `main.py` if 5000 is occupied
3. **Import Errors**: Ensure all Python files are in the correct directory structure

### Logs

The API provides detailed error messages and logging. Check the server logs for debugging information.
