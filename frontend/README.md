# Tic Tac Toe React Frontend

This is the React version of the Tic Tac Toe game frontend, converted from vanilla HTML/CSS/JS to Vite React.

## Features

- **Identical Styling**: All CSS styles preserved exactly as they were
- **Same Functionality**: All game features work identically to the original
- **API Integration**: Connects to the same backend API for AI moves
- **Responsive Design**: Mobile-friendly with the same responsive behavior
- **Stars Animation**: Animated starfield background
- **Pixel Art Style**: Retro pixel-art design with phone container

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── index.html          # Vite entry point
├── package.json        # Dependencies and scripts
├── vite.config.js      # Vite configuration
├── .env.local          # Environment variables
└── src/
    ├── App.jsx         # Main application component
    ├── main.jsx        # React entry point
    ├── components/     # React components
    │   ├── NameEntryScreen.jsx
    │   ├── GameScreen.jsx
    │   ├── WinModal.jsx
    │   └── SlideMessage.jsx
    ├── styles/
    │   └── App.css     # All original CSS styles
    └── config/
        └── api.js      # API configuration
```

## Environment Variables

The `.env.local` file contains API configuration:

```
VITE_API_PRODUCTION_URL=https://tictactoe-qlearning.onrender.com
VITE_API_LOCAL_URL=http://localhost:5001
```

## Game Features

- **Player vs AI**: Play against a perfect minimax AI
- **Score Tracking**: Keep track of wins, losses, and draws
- **API Fallback**: Falls back to random AI if backend is unavailable
- **Mobile Support**: Responsive design that works on mobile devices
- **Smooth Animations**: Cell pop animations and sliding messages

## API Integration

The game connects to the backend API for AI moves:
- Health check endpoint: `/api/health`
- Move endpoint: `/api/move`
- Automatic fallback to random moves if API is unavailable

## Development

The project uses:
- **React 18** with hooks for state management
- **Vite** for fast development and building
- **CSS Modules** for styling (preserved from original)
- **ES6+** JavaScript features

All original functionality has been preserved while converting to React's component-based architecture.
