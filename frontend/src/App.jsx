import React, { useState, useEffect, useCallback } from 'react'
import NameEntryScreen from './components/NameEntryScreen'
import GameScreen from './components/GameScreen'
import WinModal from './components/WinModal'
import SlideMessage from './components/SlideMessage'
import API_CONFIG from './config/api'

// Game state
const initialGameState = {
  board: ['', '', '', '', '', '', '', '', ''],
  currentPlayer: 'X',
  gameActive: false,
  scores: { X: 0, O: 0, draw: 0 },
  playerNames: { X: 'PLAYER', O: 'AI' },
  isPlayerTurn: true,
  apiAvailable: true,
  showNameEntry: true,
  showGameScreen: false,
  showWinModal: false,
  winMessage: '',
  slideMessage: '',
  showSlideMessage: false
}

// Win patterns
const winPatterns = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8],
  [0, 3, 6], [1, 4, 7], [2, 5, 8],
  [0, 4, 8], [2, 4, 6]
]

function App() {
  const [gameState, setGameState] = useState(initialGameState)

  // Initialize debug logging and generate stars
  useEffect(() => {
    console.log('[GAME INIT] Tic-Tac-Toe with Perfect Minimax AI')
    console.log('[CONFIG] API Configuration loaded:')
    console.log('   Environment:', window.location.hostname.includes('github.io') ? 'Production (GitHub Pages)' : 'Local Development')
    console.log('   Backend URL:', API_CONFIG.getBaseUrl())
    console.log('   Health Endpoint:', API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.HEALTH)
    console.log('   Move Endpoint:', API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.MOVE)
    console.log('   AI Agent: Perfect Minimax (backend/agents/perfect_agent.py)')
    console.log('==========================================')

    // Generate stars
    const starsContainer = document.getElementById('stars')
    if (starsContainer) {
      // Clear existing stars
      starsContainer.innerHTML = ''
      
      // Generate new stars
      for (let i = 0; i < 80; i++) {
        const star = document.createElement('div')
        star.className = 'star'
        star.style.left = Math.random() * 100 + '%'
        star.style.top = Math.random() * 100 + '%'
        star.style.animationDelay = Math.random() * 3 + 's'
        starsContainer.appendChild(star)
      }
    }
  }, [])

  // Game utility functions
  const showSlideMessage = useCallback((message, duration = 3000) => {
    setGameState(prev => ({
      ...prev,
      slideMessage: message,
      showSlideMessage: true
    }))
    
    setTimeout(() => {
      setGameState(prev => ({
        ...prev,
        showSlideMessage: false
      }))
    }, duration)
  }, [])

  // API Helper Functions
  const convertBoardToAPI = useCallback((board) => {
    return board.map(cell => {
      if (cell === 'X') return 1
      if (cell === 'O') return -1
      return 0
    })
  }, [])

  const convertBoardFromAPI = useCallback((apiBoard) => {
    return apiBoard.map(cell => {
      if (cell === 1) return 'X'
      if (cell === -1) return 'O'
      return ''
    })
  }, [])

  const getAIMoveFromAPI = useCallback(async (currentBoard) => {
    try {
      const apiBoard = convertBoardToAPI(currentBoard)
      const apiUrl = API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.MOVE
      
      console.log('[AI REQUEST] Calling Perfect Minimax Agent...')
      console.log('   API URL:', apiUrl)
      console.log('   Board State:', apiBoard)
      console.log('   Player: -1 (AI plays O)')
      
      const startTime = performance.now()
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          board: apiBoard,
          player: -1 // AI is always player -1 (O)
        })
      })
      
      const endTime = performance.now()
      const responseTime = (endTime - startTime).toFixed(2)
      
      if (!response.ok) {
        console.error('[API ERROR] Request failed:', response.status, response.statusText)
        throw new Error(`API request failed: ${response.status}`)
      }
      
      const data = await response.json()
      
      console.log('[AI RESPONSE] Perfect Minimax move received!')
      console.log('   AI Move:', data.move)
      console.log('   Updated Board:', data.board)
      console.log('   Response Time:', responseTime + 'ms')
      console.log('   Game Over:', data.game_over)
      if (data.winner !== null) {
        console.log('   Winner:', data.winner)
      }
      console.log('   Message:', data.message)
      
      return data
      
    } catch (error) {
      console.error('[API ERROR] Failed to connect to backend:', error)
      console.error('   Troubleshooting: Check if backend is running at:', API_CONFIG.getBaseUrl())
      setGameState(prev => ({ ...prev, apiAvailable: false }))
      showSlideMessage('API UNAVAILABLE - USING RANDOM AI', 3000)
      return null
    }
  }, [convertBoardToAPI, showSlideMessage])

  const checkAPIHealth = useCallback(async () => {
    try {
      const apiUrl = API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.HEALTH
      
      console.log('[HEALTH CHECK] Testing backend connection...')
      console.log('   API URL:', apiUrl)
      
      const startTime = performance.now()
      
      const response = await fetch(apiUrl, {
        method: 'GET',
        timeout: 5000
      })
      
      const endTime = performance.now()
      const responseTime = (endTime - startTime).toFixed(2)
      
      if (response.ok) {
        const data = await response.json()
        setGameState(prev => ({ ...prev, apiAvailable: true }))
        
        console.log('[HEALTH CHECK] Backend is ONLINE!')
        console.log('   Agent:', data.agent)
        console.log('   Message:', data.message)
        console.log('   Response Time:', responseTime + 'ms')
        console.log('   Connected to: backend/agents/perfect_agent.py')
        
        return true
      }
    } catch (error) {
      console.warn('[HEALTH CHECK] Backend is OFFLINE')
      console.warn('   Attempted URL:', API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.HEALTH)
      console.warn('   Error:', error.message)
      console.warn('   Fallback: Using random AI moves')
      setGameState(prev => ({ ...prev, apiAvailable: false }))
    }
    return false
  }, [])

  // Game logic functions

  const updateScores = useCallback((winner) => {
    setGameState(prev => ({
      ...prev,
      scores: {
        ...prev.scores,
        [winner]: prev.scores[winner] + 1
      }
    }))
  }, [])

  const showWinModal = useCallback((message) => {
    console.log('[WIN MODAL] ==== SHOWING WIN MODAL ====')
    console.log('[WIN MODAL] Message:', message)
    console.log('[WIN MODAL] gameActive:', gameState.gameActive)
    console.log('[WIN MODAL] Current board:', gameState.board)
    
    setGameState(prev => ({
      ...prev,
      winMessage: message,
      showWinModal: true
    }))
  }, [gameState.gameActive, gameState.board])

  const resetGame = useCallback(() => {
    console.log('[RESET GAME] Resetting game state...')
    console.log('[RESET GAME] gameActive before reset:', gameState.gameActive)
    
    setGameState(prev => ({
      ...prev,
      board: ['', '', '', '', '', '', '', '', ''],
      currentPlayer: 'X',
      gameActive: true,
      isPlayerTurn: true,
      showWinModal: false
    }))
    
    console.log('[RESET GAME] Reset complete!')
    showSlideMessage('GAME RESET!')
  }, [gameState.gameActive, showSlideMessage])

  const resetToNameEntry = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      scores: { X: 0, O: 0, draw: 0 },
      showNameEntry: true,
      showGameScreen: false,
      showWinModal: false
    }))
    resetGame()
    showSlideMessage('BACK TO MAIN!')
  }, [resetGame, showSlideMessage])

  const startGame = useCallback((playerName) => {
    const name = playerName.trim().toUpperCase() || 'PLAYER'
    
    setGameState(prev => ({
      ...prev,
      playerNames: { X: name, O: 'AI' },
      showNameEntry: false,
      showGameScreen: true,
      gameActive: true,
      isPlayerTurn: true,
      currentPlayer: 'X'
    }))
    
    // Check API health on game start
    checkAPIHealth().then(isHealthy => {
      if (isHealthy) {
        showSlideMessage(`GAME STARTED! ${name} VS PERFECT AI`)
      } else {
        showSlideMessage(`GAME STARTED! ${name} VS RANDOM AI`)
      }
    })
  }, [checkAPIHealth, showSlideMessage])

  const handleCellClick = useCallback(async (index) => {
    console.log('[PLAYER MOVE] Clicked cell:', index, 'gameActive:', gameState.gameActive, 'isPlayerTurn:', gameState.isPlayerTurn)
    
    if (gameState.board[index] !== '' || !gameState.gameActive || !gameState.isPlayerTurn) return
    
    // Create new board with the move
    const newBoard = gameState.board.map((cell, i) => i === index ? gameState.currentPlayer : cell)
    
    console.log('[PLAYER MOVE] After move, board:', newBoard)
    console.log('[PLAYER MOVE] Checking if player won...')
    
    const playerWon = winPatterns.some(pattern => {
      return pattern.every(idx => newBoard[idx] === gameState.currentPlayer)
    })
    const boardFull = newBoard.every(cell => cell !== '')
    
    console.log('[PLAYER MOVE] Player won:', playerWon)
    console.log('[PLAYER MOVE] Board full:', boardFull)
    
    if (playerWon) {
      console.log('[PLAYER MOVE] Player wins! Showing modal...')
      setGameState(prev => ({ 
        ...prev, 
        board: newBoard,
        gameActive: false 
      }))
      updateScores(gameState.currentPlayer)
      showWinModal(`${gameState.playerNames[gameState.currentPlayer]} WINS!`)
      showSlideMessage(`${gameState.playerNames[gameState.currentPlayer]} WINS!`)
    } else if (boardFull) {
      console.log('[PLAYER MOVE] Draw game! Showing modal...')
      setGameState(prev => ({ 
        ...prev, 
        board: newBoard,
        gameActive: false 
      }))
      updateScores('draw')
      showWinModal('DRAW GAME!')
      showSlideMessage('DRAW GAME!')
    } else {
      console.log('[PLAYER MOVE] Game continues, AI turn...')
      // Switch to AI turn
      setGameState(prev => ({
        ...prev,
        board: newBoard,
        isPlayerTurn: false,
        currentPlayer: 'O'
      }))
      showSlideMessage('AI IS THINKING...', 1000)
      
      // AI makes move after a short delay
      setTimeout(() => {
        makeAIMove(newBoard)
      }, 1000)
    }
  }, [gameState.board, gameState.gameActive, gameState.isPlayerTurn, gameState.currentPlayer, gameState.playerNames, updateScores, showWinModal, showSlideMessage])

  const makeAIMove = useCallback(async (currentBoard) => {
    if (!gameState.gameActive) return
    
    // Get available moves
    const availableMoves = []
    for (let i = 0; i < 9; i++) {
      if (currentBoard[i] === '') {
        availableMoves.push(i)
      }
    }
    
    if (availableMoves.length === 0) return
    
    let aiMove
    let gameOver = false
    let winner = null
    
    // Try to get move from API first
    if (gameState.apiAvailable) {
      const apiResult = await getAIMoveFromAPI(currentBoard)
      if (apiResult && typeof apiResult === 'object') {
        aiMove = apiResult.move
        gameOver = apiResult.game_over
        winner = apiResult.winner
      } else {
        aiMove = apiResult
      }
    }
    
    // Fallback to random move if API fails or is unavailable
    if (aiMove === null || aiMove === undefined) {
      aiMove = availableMoves[Math.floor(Math.random() * availableMoves.length)]
    }
    
    // Create new board with AI move
    const newBoard = currentBoard.map((cell, i) => i === aiMove ? 'O' : cell)
    
    console.log('[AI MOVE] After AI move, board:', newBoard)
    console.log('[AI MOVE] API gameOver:', gameOver, 'winner:', winner)
    
    // Check game state - use API result if available, otherwise use frontend check
    if (gameOver && winner !== null) {
      console.log('[AI MOVE] Using API game state')
      setGameState(prev => ({ 
        ...prev, 
        board: newBoard,
        gameActive: false 
      }))
      if (winner === -1) {
        // AI wins
        console.log('[AI MOVE] AI wins! Showing modal...')
        updateScores('O')
        showWinModal(`${gameState.playerNames.O} WINS!`)
        showSlideMessage(`${gameState.playerNames.O} WINS!`)
      } else if (winner === 1) {
        // Player wins
        console.log('[AI MOVE] Player wins! Showing modal...')
        updateScores('X')
        showWinModal(`${gameState.playerNames.X} WINS!`)
        showSlideMessage(`${gameState.playerNames.X} WINS!`)
      } else {
        // Draw
        console.log('[AI MOVE] Draw game! Showing modal...')
        updateScores('draw')
        showWinModal('DRAW GAME!')
        showSlideMessage('DRAW GAME!')
      }
    } else {
      console.log('[AI MOVE] Using frontend game state check')
      const aiWon = winPatterns.some(pattern => {
        return pattern.every(idx => newBoard[idx] === 'O')
      })
      const boardFull = newBoard.every(cell => cell !== '')
      console.log('[AI MOVE] AI won:', aiWon, 'Board full:', boardFull)
      
      if (aiWon) {
        console.log('[AI MOVE] AI wins! Showing modal...')
        setGameState(prev => ({ 
          ...prev, 
          board: newBoard,
          gameActive: false 
        }))
        updateScores('O')
        showWinModal(`${gameState.playerNames.O} WINS!`)
        showSlideMessage(`${gameState.playerNames.O} WINS!`)
      } else if (boardFull) {
        console.log('[AI MOVE] Draw game! Showing modal...')
        setGameState(prev => ({ 
          ...prev, 
          board: newBoard,
          gameActive: false 
        }))
        updateScores('draw')
        showWinModal('DRAW GAME!')
        showSlideMessage('DRAW GAME!')
      } else {
        console.log('[AI MOVE] Game continues, player turn...')
        // Switch back to player turn
        setGameState(prev => ({
          ...prev,
          board: newBoard,
          isPlayerTurn: true,
          currentPlayer: 'X'
        }))
        showSlideMessage(`${gameState.playerNames.X}'S TURN`, 2000)
      }
    }
  }, [gameState.gameActive, gameState.apiAvailable, gameState.playerNames, getAIMoveFromAPI, updateScores, showWinModal, showSlideMessage])

  return (
    <>
      <div className="stars" id="stars"></div>
      <SlideMessage 
        message={gameState.slideMessage}
        show={gameState.showSlideMessage}
      />
      
      <div className="phone-container pixel-corners">
        <div className="phone-notch pixel-corners">
          <div className="phone-speaker"></div>
        </div>
        <div className="phone-screen pixel-corners">
          <NameEntryScreen 
            show={gameState.showNameEntry}
            onStartGame={startGame}
          />
          
          <GameScreen 
            show={gameState.showGameScreen}
            board={gameState.board}
            scores={gameState.scores}
            playerNames={gameState.playerNames}
            onCellClick={handleCellClick}
            onResetGame={resetGame}
            onBackToMain={resetToNameEntry}
          />
        </div>
      </div>

      <WinModal 
        show={gameState.showWinModal}
        message={gameState.winMessage}
        onPlayAgain={resetGame}
        onNewGame={resetToNameEntry}
      />
    </>
  )
}

export default App
