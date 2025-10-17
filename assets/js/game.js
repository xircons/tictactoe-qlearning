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
    
    nameEntryScreen.classList.add('hidden');
    gameScreen.classList.add('active');
    gameActive = true;
    isPlayerTurn = true;
    currentPlayer = 'X';
    // status.textContent = `${playerNames[currentPlayer]}'S TURN`;
    
    showSlideMessage(`GAME STARTED! ${playerName} VS AI`);
}

// Game logic
cells.forEach(cell => {
    cell.addEventListener('click', handleCellClick);
});

function handleCellClick(e) {
    const index = e.target.dataset.index;
    
    if (board[index] !== '' || !gameActive || !isPlayerTurn) return;
    
    makeMove(index, currentPlayer);
    
    if (checkWin(currentPlayer)) {
        gameActive = false;
        scores[currentPlayer]++;
        updateScores();
        showWinModal(`${playerNames[currentPlayer]} WINS!`);
        showSlideMessage(`${playerNames[currentPlayer]} WINS!`);
    } else if (board.every(cell => cell !== '')) {
        gameActive = false;
        scores.draw++;
        updateScores();
        showWinModal('DRAW GAME!');
        showSlideMessage('DRAW GAME!');
    } else {
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

function makeAIMove() {
    if (!gameActive) return;
    
    // Get available moves
    const availableMoves = [];
    for (let i = 0; i < 9; i++) {
        if (board[i] === '') {
            availableMoves.push(i);
        }
    }
    
    if (availableMoves.length === 0) return;
    
    // Random AI move
    const randomIndex = availableMoves[Math.floor(Math.random() * availableMoves.length)];
    makeMove(randomIndex, 'O');
    
    if (checkWin('O')) {
        gameActive = false;
        scores.O++;
        updateScores();
        showWinModal(`${playerNames.O} WINS!`);
        showSlideMessage(`${playerNames.O} WINS!`);
    } else if (board.every(cell => cell !== '')) {
        gameActive = false;
        scores.draw++;
        updateScores();
        showWinModal('DRAW GAME!');
        showSlideMessage('DRAW GAME!');
    } else {
        // Switch back to player turn
        isPlayerTurn = true;
        currentPlayer = 'X';
        // status.textContent = `${playerNames[currentPlayer]}'S TURN`;
        showSlideMessage(`${playerNames[currentPlayer]}'S TURN`, 2000);
    }
}

function checkWin(player) {
    return winPatterns.some(pattern => {
        return pattern.every(index => board[index] === player);
    });
}

function showWinModal(message) {
    winMessage.textContent = message;
    winModal.classList.add('active');
    // status.textContent = message;
}

function resetGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    gameActive = true;
    isPlayerTurn = true;
    // status.textContent = `${playerNames[currentPlayer]}'S TURN`;
    winModal.classList.remove('active');
    cells.forEach(cell => {
        cell.innerHTML = '';
        cell.classList.remove('taken');
    });
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
}

playAgainBtn.addEventListener('click', resetGame);
newGameBtn.addEventListener('click', resetToNameEntry);
resetBtn.addEventListener('click', resetGame);
backBtn.addEventListener('click', resetToNameEntry);

