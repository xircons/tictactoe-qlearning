// Create pixel grid background with sky gradient
function createPixelGrid() {
    const pixelGrid = document.getElementById('pixel-grid');
    if (!pixelGrid) return;
    
    // Detect if mobile device
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                     window.innerWidth <= 768 || 
                     ('ontouchstart' in window);
    
    // Set grid size based on device type
    const gridSize = isMobile ? 16 : 32;
    const totalPixels = gridSize * gridSize;
    
    // Update CSS grid columns/rows
    pixelGrid.style.gridTemplateColumns = `repeat(${gridSize}, 1fr)`;
    pixelGrid.style.gridTemplateRows = `repeat(${gridSize}, 1fr)`;
    
    // Color palette for sky gradient (lightest to darkest)
    const colors = [
        '#20303f', '#202b38', '#1d2835', '#1a2530', 
        '#17202a', '#141d26', '#10171f', '#0d1419', '#0a1015'
    ];
    
    // Helper function to interpolate between two hex colors
    function interpolateColor(color1, color2, factor) {
        const c1 = parseInt(color1.slice(1), 16);
        const c2 = parseInt(color2.slice(1), 16);
        
        const r1 = (c1 >> 16) & 0xff;
        const g1 = (c1 >> 8) & 0xff;
        const b1 = c1 & 0xff;
        
        const r2 = (c2 >> 16) & 0xff;
        const g2 = (c2 >> 8) & 0xff;
        const b2 = c2 & 0xff;
        
        const r = Math.round(r1 + (r2 - r1) * factor);
        const g = Math.round(g1 + (g2 - g1) * factor);
        const b = Math.round(b1 + (b2 - b1) * factor);
        
        return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
    }
    
    // Generate pixels based on grid size
    const fragment = document.createDocumentFragment();
    
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col < gridSize; col++) {
            const pixel = document.createElement('div');
            pixel.className = 'pixel';
            
            // Calculate color based on row (vertical gradient)
            const rowFactor = row / (gridSize - 1); // 0 to 1
            
            // Determine which color segment we're in
            const colorIndex = Math.floor(rowFactor * (colors.length - 1));
            const nextColorIndex = Math.min(colorIndex + 1, colors.length - 1);
            const segmentFactor = (rowFactor * (colors.length - 1)) - colorIndex;
            
            // Interpolate between colors
            let baseColor = interpolateColor(colors[colorIndex], colors[nextColorIndex], segmentFactor);
            
            // Add slight horizontal variation for natural look (±5% brightness)
            const horizontalVariation = (col / (gridSize - 1)) * 0.1 - 0.05; // -0.05 to +0.05
            const variation = 1 + horizontalVariation;
            
            // Apply variation to color
            const colorInt = parseInt(baseColor.slice(1), 16);
            const r = Math.min(255, Math.max(0, Math.round(((colorInt >> 16) & 0xff) * variation)));
            const g = Math.min(255, Math.max(0, Math.round(((colorInt >> 8) & 0xff) * variation)));
            const b = Math.min(255, Math.max(0, Math.round((colorInt & 0xff) * variation)));
            
            const finalColor = '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0');
            pixel.style.backgroundColor = finalColor;
            
            fragment.appendChild(pixel);
        }
    }
    
    pixelGrid.appendChild(fragment);
    console.log(`[PIXEL GRID] Created ${totalPixels} pixels (${gridSize}×${gridSize}) with sky gradient`);
}

// Mobile detection and styling
function detectMobile() {
    const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
                     window.innerWidth <= 768 || 
                     ('ontouchstart' in window);
    
    if (isMobile) {
        document.body.classList.add('mobile-device');
        const phoneContainer = document.querySelector('.phone-container');
        if (phoneContainer) {
            phoneContainer.classList.add('mobile-style');
            console.log('[MOBILE] Mobile styles applied! Phone container:', phoneContainer.className);
            
            // Create stars within phone-screen for mobile
            createMobileStars();
        }
        console.log('[MOBILE] Mobile device detected - applying mobile styles');
    } else {
        console.log('[DESKTOP] Desktop device detected - using phone container');
    }
}

// Create stars within phone-screen for mobile devices
function createMobileStars() {
    const phoneScreen = document.querySelector('.phone-screen');
    if (phoneScreen) {
        // Remove existing mobile stars if any
        const existingStars = phoneScreen.querySelector('.mobile-stars');
        if (existingStars) {
            existingStars.remove();
        }
        
        // Create mobile stars container
        const mobileStarsContainer = document.createElement('div');
        mobileStarsContainer.className = 'mobile-stars';
        mobileStarsContainer.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        `;
        
        // Generate stars for mobile
        for (let i = 0; i < 60; i++) {
            const star = document.createElement('div');
            star.className = 'mobile-star';
            star.style.cssText = `
                position: absolute;
                width: 3px;
                height: 3px;
                background: white;
                box-shadow: 0 0 0 1px white, 0 0 5px 1px rgba(255, 255, 255, 0.5);
                animation: twinkle 3s infinite;
                animation-delay: ${Math.random() * 3}s;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
            `;
            mobileStarsContainer.appendChild(star);
        }
        
        // Insert stars at the beginning of phone-screen
        phoneScreen.insertBefore(mobileStarsContainer, phoneScreen.firstChild);
        console.log('[MOBILE] Mobile stars created within phone-screen');
    }
}

// Apply pixel grid and mobile detection on load
document.addEventListener('DOMContentLoaded', () => {
    createPixelGrid();
    detectMobile();
});

// Mobile keyboard detection
function handleMobileKeyboard() {
    if (window.innerWidth <= 768) {
        const initialHeight = window.innerHeight;
        const welcomeTitle = document.querySelector('.welcome-title');
        
        function checkKeyboard() {
            const currentHeight = window.innerHeight;
            const heightDifference = initialHeight - currentHeight;
            
            // Detect keyboard early - when height reduced by more than 20px (0-10% of keyboard animation)
            if (heightDifference > 20) {
                if (welcomeTitle) {
                    welcomeTitle.style.margin = '0px 0px 80px 0px';
                    console.log('[MOBILE] Keyboard detected early - adjusting welcome title margin');
                }
            } else {
                if (welcomeTitle) {
                    welcomeTitle.style.margin = '60px 0px 40px 0px';
                    console.log('[MOBILE] Keyboard hidden - restoring welcome title margin');
                }
            }
        }
        
        // Check on resize (keyboard show/hide)
        window.addEventListener('resize', checkKeyboard);
        
        // Check on focus/blur of input (keyboard show/hide)
        const playerInput = document.getElementById('playerXName');
        if (playerInput) {
            playerInput.addEventListener('focus', checkKeyboard);
            playerInput.addEventListener('blur', checkKeyboard);
        }
    }
}

// Apply keyboard detection on load
document.addEventListener('DOMContentLoaded', handleMobileKeyboard);

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
    showSlideMessage('BACK TO MAIN!');
}

playAgainBtn.addEventListener('click', resetGame);
newGameBtn.addEventListener('click', resetToNameEntry);
resetBtn.addEventListener('click', resetGame);
backBtn.addEventListener('click', resetToNameEntry);

