// Generate stars
const starsContainer = document.getElementById('stars');
for (let i = 0; i < 80; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    star.style.left = Math.random() * 100 + '%';
    star.style.top = Math.random() * 100 + '%';
    star.style.animationDelay = Math.random() * 3 + 's';
    starsContainer.appendChild(star);
}

// Game state
let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let gameActive = false;
let scores = { X: 0, O: 0, draw: 0 };
let playerNames = { X: 'PLAYER', O: 'AI' };
let isPlayerTurn = true;
let apiAvailable = true; // Track API availability

// Initialize debug logging
console.log('[GAME INIT] Tic-Tac-Toe with Perfect Minimax AI');
console.log('[CONFIG] API Configuration loaded:');
console.log('   Environment:', window.location.hostname.includes('github.io') ? 'Production (GitHub Pages)' : 'Local Development');
console.log('   Backend URL:', API_CONFIG.getBaseUrl());
console.log('   Health Endpoint:', API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.HEALTH);
console.log('   Move Endpoint:', API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.MOVE);
console.log('   AI Agent: Perfect Minimax (backend/agents/perfect_agent.py)');
console.log('==========================================');

// DOM elements
const nameEntryScreen = document.getElementById('nameEntryScreen');
const gameScreen = document.getElementById('gameScreen');
const startGameBtn = document.getElementById('startGameBtn');
const playerXNameInput = document.getElementById('playerXName');
const cells = document.querySelectorAll('.cell');
const status = document.getElementById('status');
const resetBtn = document.getElementById('resetBtn');
const winModal = document.getElementById('winModal');
const winMessage = document.getElementById('winMessage');
const playAgainBtn = document.getElementById('playAgainBtn');
const newGameBtn = document.getElementById('newGameBtn');
const playerNamesDisplay = document.getElementById('playerNamesDisplay');
const labelX = document.getElementById('labelX');
const labelO = document.getElementById('labelO');
const slideMessage = document.getElementById('slideMessage');
const backBtn = document.getElementById('backBtn');

const winPatterns = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
];

// API Helper Functions
function convertBoardToAPI(board) {
    // Convert frontend board ('', 'X', 'O') to API format (0, 1, -1)
    return board.map(cell => {
        if (cell === 'X') return 1;
        if (cell === 'O') return -1;
        return 0;
    });
}

function convertBoardFromAPI(apiBoard) {
    // Convert API board (0, 1, -1) to frontend format ('', 'X', 'O')
    return apiBoard.map(cell => {
        if (cell === 1) return 'X';
        if (cell === -1) return 'O';
        return '';
    });
}

async function getAIMoveFromAPI() {
    try {
        const apiBoard = convertBoardToAPI(board);
        const apiUrl = API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.MOVE;
        
        console.log('[AI REQUEST] Calling Perfect Minimax Agent...');
        console.log('   API URL:', apiUrl);
        console.log('   Board State:', apiBoard);
        console.log('   Player: -1 (AI plays O)');
        
        const startTime = performance.now();
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board: apiBoard,
                player: -1 // AI is always player -1 (O)
            })
        });
        
        const endTime = performance.now();
        const responseTime = (endTime - startTime).toFixed(2);
        
        if (!response.ok) {
            console.error('[API ERROR] Request failed:', response.status, response.statusText);
            throw new Error(`API request failed: ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log('[AI RESPONSE] Perfect Minimax move received!');
        console.log('   AI Move:', data.move);
        console.log('   Updated Board:', data.board);
        console.log('   Response Time:', responseTime + 'ms');
        console.log('   Game Over:', data.game_over);
        if (data.winner !== null) {
            console.log('   Winner:', data.winner);
        }
        console.log('   Message:', data.message);
        
        return data;
        
    } catch (error) {
        console.error('[API ERROR] Failed to connect to backend:', error);
        console.error('   Troubleshooting: Check if backend is running at:', API_CONFIG.getBaseUrl());
        apiAvailable = false;
        showSlideMessage('API UNAVAILABLE - USING RANDOM AI', 3000);
        return null;
    }
}

async function checkAPIHealth() {
    try {
        const apiUrl = API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.HEALTH;
        
        console.log('[HEALTH CHECK] Testing backend connection...');
        console.log('   API URL:', apiUrl);
        
        const startTime = performance.now();
        
        const response = await fetch(apiUrl, {
            method: 'GET',
            timeout: 5000
        });
        
        const endTime = performance.now();
        const responseTime = (endTime - startTime).toFixed(2);
        
        if (response.ok) {
            const data = await response.json();
            apiAvailable = true;
            
            console.log('[HEALTH CHECK] Backend is ONLINE!');
            console.log('   Agent:', data.agent);
            console.log('   Message:', data.message);
            console.log('   Response Time:', responseTime + 'ms');
            console.log('   Connected to: backend/agents/perfect_agent.py');
            
            return true;
        }
    } catch (error) {
        console.warn('[HEALTH CHECK] Backend is OFFLINE');
        console.warn('   Attempted URL:', API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.HEALTH);
        console.warn('   Error:', error.message);
        console.warn('   Fallback: Using random AI moves');
        apiAvailable = false;
    }
    return false;
}

// Start game
startGameBtn.addEventListener('click', startGame);
playerXNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') startGame();
});

// Sliding message functions
function showSlideMessage(message, duration = 3000) {
    slideMessage.textContent = message;
    slideMessage.classList.remove('hide');
    slideMessage.classList.add('show');
    
    setTimeout(() => {
        slideMessage.classList.remove('show');
        slideMessage.classList.add('hide');
    }, duration);
}

function startGame() {
    const playerName = playerXNameInput.value.trim().toUpperCase() || 'PLAYER';
    
    playerNames.X = playerName;
    playerNames.O = 'AI';
    
    labelX.textContent = playerName;
    labelO.textContent = 'AI';
    playerNamesDisplay.textContent = `${playerName} VS AI`;
    
    // Hide any existing win modal
    winModal.classList.remove('active');
    
    nameEntryScreen.classList.add('hidden');
    gameScreen.classList.add('active');
    gameActive = true;
    isPlayerTurn = true;
    currentPlayer = 'X';
    // status.textContent = `${playerNames[currentPlayer]}'S TURN`;
    
    // Check API health on game start
    checkAPIHealth().then(isHealthy => {
        if (isHealthy) {
            showSlideMessage(`GAME STARTED! ${playerName} VS PERFECT AI`);
        } else {
            showSlideMessage(`GAME STARTED! ${playerName} VS RANDOM AI`);
        }
    });
}

// Game logic
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

function handleCellClick(e) {
    const index = e.target.dataset.index;
    
    console.log('[PLAYER MOVE] Clicked cell:', index, 'gameActive:', gameActive, 'isPlayerTurn:', isPlayerTurn);
    
    if (board[index] !== '' || !gameActive || !isPlayerTurn) return;
    
    makeMove(index, currentPlayer);
    
    console.log('[PLAYER MOVE] After move, board:', board);
    console.log('[PLAYER MOVE] Checking if player won...');
    
    const playerWon = checkWin(currentPlayer);
    const boardFull = board.every(cell => cell !== '');
    
    console.log('[PLAYER MOVE] Player won:', playerWon);
    console.log('[PLAYER MOVE] Board full:', boardFull);
    
    if (playerWon) {
        console.log('[PLAYER MOVE] Player wins! Showing modal...');
        gameActive = false;
        scores[currentPlayer]++;
        updateScores();
        showWinModal(`${playerNames[currentPlayer]} WINS!`);
        showSlideMessage(`${playerNames[currentPlayer]} WINS!`);
    } else if (boardFull) {
        console.log('[PLAYER MOVE] Draw game! Showing modal...');
        gameActive = false;
        scores.draw++;
        updateScores();
        showWinModal('DRAW GAME!');
        showSlideMessage('DRAW GAME!');
    } else {
        console.log('[PLAYER MOVE] Game continues, AI turn...');
        // Switch to AI turn
        isPlayerTurn = false;
        currentPlayer = 'O';
        // status.textContent = `${playerNames[currentPlayer]} IS THINKING...`;
        showSlideMessage('AI IS THINKING...', 1000);
        
        // AI makes move after a short delay
        setTimeout(() => {
            if (gameActive) {
                makeAIMove();
            }
        }, 1000);
    }
}

function makeMove(index, player) {
    board[index] = player;
    cells[index].innerHTML = `<span class="cell-content">${player}</span>`;
    cells[index].classList.add('taken');
}

async function makeAIMove() {
    if (!gameActive) return;
    
    // Get available moves
    const availableMoves = [];
    for (let i = 0; i < 9; i++) {
        if (board[i] === '') {
            availableMoves.push(i);
        }
    }
    
    if (availableMoves.length === 0) return;
    
    let aiMove;
    let gameOver = false;
    let winner = null;
    
    // Try to get move from API first
    if (apiAvailable) {
        const apiResult = await getAIMoveFromAPI();
        if (apiResult && typeof apiResult === 'object') {
            aiMove = apiResult.move;
            gameOver = apiResult.game_over;
            winner = apiResult.winner;
        } else {
            aiMove = apiResult;
        }
    }
    
    // Fallback to random move if API fails or is unavailable
    if (aiMove === null || aiMove === undefined) {
        aiMove = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    }
    
    // Make the move
    makeMove(aiMove, 'O');
    
    console.log('[AI MOVE] After AI move, board:', board);
    console.log('[AI MOVE] API gameOver:', gameOver, 'winner:', winner);
    
    // Check game state - use API result if available, otherwise use frontend check
    if (gameOver && winner !== null) {
        console.log('[AI MOVE] Using API game state');
        gameActive = false;
        if (winner === -1) {
            // AI wins
            console.log('[AI MOVE] AI wins! Showing modal...');
            scores.O++;
            updateScores();
            showWinModal(`${playerNames.O} WINS!`);
            showSlideMessage(`${playerNames.O} WINS!`);
        } else if (winner === 1) {
            // Player wins
            console.log('[AI MOVE] Player wins! Showing modal...');
            scores.X++;
            updateScores();
            showWinModal(`${playerNames.X} WINS!`);
            showSlideMessage(`${playerNames.X} WINS!`);
        } else {
            // Draw
            console.log('[AI MOVE] Draw game! Showing modal...');
            scores.draw++;
            updateScores();
            showWinModal('DRAW GAME!');
            showSlideMessage('DRAW GAME!');
        }
    } else {
        console.log('[AI MOVE] Using frontend game state check');
        const aiWon = checkWin('O');
        const boardFull = board.every(cell => cell !== '');
        console.log('[AI MOVE] AI won:', aiWon, 'Board full:', boardFull);
        
        if (aiWon) {
            console.log('[AI MOVE] AI wins! Showing modal...');
            gameActive = false;
            scores.O++;
            updateScores();
            showWinModal(`${playerNames.O} WINS!`);
            showSlideMessage(`${playerNames.O} WINS!`);
        } else if (boardFull) {
            console.log('[AI MOVE] Draw game! Showing modal...');
            gameActive = false;
            scores.draw++;
            updateScores();
            showWinModal('DRAW GAME!');
            showSlideMessage('DRAW GAME!');
        } else {
            console.log('[AI MOVE] Game continues, player turn...');
            // Switch back to player turn
            isPlayerTurn = true;
            currentPlayer = 'X';
            // status.textContent = `${playerNames[currentPlayer]}'S TURN`;
            showSlideMessage(`${playerNames[currentPlayer]}'S TURN`, 2000);
        }
    }
}

function checkWin(player) {
    return winPatterns.some(pattern => {
        return pattern.every(index => board[index] === player);
    });
}

function showWinModal(message) {
    console.log('[WIN MODAL] ==== SHOWING WIN MODAL ====');
    console.log('[WIN MODAL] Message:', message);
    console.log('[WIN MODAL] gameActive:', gameActive);
    console.log('[WIN MODAL] Current board:', board);
    
    winMessage.textContent = message;
    winModal.classList.add('active');
    
    console.log('[WIN MODAL] Modal class list:', winModal.classList.toString());
    console.log('[WIN MODAL] Modal display style:', window.getComputedStyle(winModal).display);
    // status.textContent = message;
}

function resetGame() {
    console.log('[RESET GAME] Resetting game state...');
    console.log('[RESET GAME] gameActive before reset:', gameActive);
    
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    gameActive = true;
    isPlayerTurn = true;
    
    console.log('[RESET GAME] Hiding modal...');
    winModal.classList.remove('active');
    console.log('[RESET GAME] Modal classes after remove:', winModal.classList.toString());
    
    cells.forEach(cell => {
        cell.innerHTML = '';
        cell.classList.remove('taken');
    });
    
    console.log('[RESET GAME] gameActive after reset:', gameActive);
    console.log('[RESET GAME] Reset complete!');
    // status.textContent = `${playerNames[currentPlayer]}'S TURN`;
    showSlideMessage('GAME RESET!');
}

function updateScores() {
    document.getElementById('scoreX').textContent = scores.X;
    document.getElementById('scoreO').textContent = scores.O;
    document.getElementById('scoreDraw').textContent = scores.draw;
}

function resetToNameEntry() {
    scores = { X: 0, O: 0, draw: 0 };
    updateScores();
    resetGame();
    gameScreen.classList.remove('active');
    nameEntryScreen.classList.remove('hidden');
    playerXNameInput.value = '';
    winModal.classList.remove('active');
    showSlideMessage('FRESH START!');
}

playAgainBtn.addEventListener('click', resetGame);
newGameBtn.addEventListener('click', resetToNameEntry);
resetBtn.addEventListener('click', resetGame);
backBtn.addEventListener('click', resetToNameEntry);

