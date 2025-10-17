// Game state
let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let gameActive = false;
let currentAgent = 'perfect_minimax';
let availableAgents = {};

// DOM elements
const cells = document.querySelectorAll('.cell');
const gameStatus = document.getElementById('gameStatus');
const currentAgentDisplay = document.getElementById('currentAgent');
const agentStatus = document.getElementById('agentStatus');
const resetBtn = document.getElementById('resetBtn');
const newGameBtn = document.getElementById('newGameBtn');

// Agent selection buttons
const perfectAgentBtn = document.getElementById('perfectAgent');
const qlearningAgentBtn = document.getElementById('qlearningAgent');
const hybridAgentBtn = document.getElementById('hybridAgent');

// Initialize debug logging
console.log('[GAME INIT] Tic-Tac-Toe with Multiple AI Agents');
console.log('[CONFIG] API Configuration loaded:');
console.log('   Environment:', window.location.hostname.includes('github.io') ? 'Production (GitHub Pages)' : 'Local Development');
console.log('   Backend URL:', API_CONFIG.getBaseUrl());
console.log('==========================================');

// Initialize game
async function initGame() {
    await checkAvailableAgents();
    setupEventListeners();
    resetGame();
}

// Check available agents from backend
async function checkAvailableAgents() {
    try {
        const response = await fetch(API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.AGENTS);
        const data = await response.json();
        availableAgents = data.agents;
        
        console.log('[AGENTS] Available agents:', availableAgents);
        
        // Update UI based on available agents
        updateAgentButtons();
        
    } catch (error) {
        console.error('[AGENTS] Failed to fetch available agents:', error);
        // Default to perfect minimax only
        availableAgents = {
            perfect_minimax: { available: true, name: "Perfect Minimax" }
        };
        updateAgentButtons();
    }
}

// Update agent selection buttons based on availability
function updateAgentButtons() {
    perfectAgentBtn.disabled = !availableAgents.perfect_minimax?.available;
    qlearningAgentBtn.disabled = !availableAgents.qlearning?.available;
    hybridAgentBtn.disabled = !availableAgents.hybrid?.available;
    
    // Update button text with availability status
    perfectAgentBtn.textContent = `Perfect Minimax ${availableAgents.perfect_minimax?.available ? '✓' : '✗'}`;
    qlearningAgentBtn.textContent = `Q-Learning ${availableAgents.qlearning?.available ? '✓' : '✗'}`;
    hybridAgentBtn.textContent = `Hybrid ${availableAgents.hybrid?.available ? '✓' : '✗'}`;
    
    // Show status message
    const availableCount = Object.values(availableAgents).filter(agent => agent.available).length;
    agentStatus.textContent = `${availableCount} agent(s) available`;
}

// Setup event listeners
function setupEventListeners() {
    // Cell clicks
    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });
    
    // Agent selection
    perfectAgentBtn.addEventListener('click', () => selectAgent('perfect_minimax'));
    qlearningAgentBtn.addEventListener('click', () => selectAgent('qlearning'));
    hybridAgentBtn.addEventListener('click', () => selectAgent('hybrid'));
    
    // Control buttons
    resetBtn.addEventListener('click', resetGame);
    newGameBtn.addEventListener('click', newGame);
}

// Select agent
function selectAgent(agentType) {
    if (!availableAgents[agentType]?.available) {
        console.warn(`[AGENT] ${agentType} is not available`);
        return;
    }
    
    currentAgent = agentType;
    
    // Update UI
    document.querySelectorAll('.agent-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(agentType + 'Agent').classList.add('active');
    
    currentAgentDisplay.textContent = `Current Agent: ${availableAgents[agentType].name}`;
    
    console.log(`[AGENT] Selected: ${agentType}`);
}

// Handle cell click
function handleCellClick(e) {
    const index = e.target.dataset.index;
    
    if (board[index] !== '' || !gameActive || currentPlayer !== 'X') return;
    
    makeMove(index, 'X');
    
    if (checkWin('X')) {
        gameActive = false;
        gameStatus.textContent = 'You win!';
        return;
    }
    
    if (board.every(cell => cell !== '')) {
        gameActive = false;
        gameStatus.textContent = 'Draw!';
        return;
    }
    
    // AI turn
    gameStatus.textContent = 'AI is thinking...';
    setTimeout(() => {
        if (gameActive) {
            makeAIMove();
        }
    }, 500);
}

// Make move
function makeMove(index, player) {
    board[index] = player;
    cells[index].textContent = player;
    cells[index].classList.add('taken');
}

// Make AI move
async function makeAIMove() {
    if (!gameActive) return;
    
    try {
        const apiBoard = convertBoardToAPI(board);
        const apiUrl = API_CONFIG.getBaseUrl() + API_CONFIG.ENDPOINTS.MOVE;
        
        console.log(`[AI REQUEST] Calling ${currentAgent} agent...`);
        console.log('   Board State:', apiBoard);
        
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                board: apiBoard,
                player: -1, // AI is always player -1 (O)
                agent: currentAgent
            })
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }
        
        const data = await response.json();
        
        console.log(`[AI RESPONSE] ${data.agent_used} move received!`);
        console.log('   AI Move:', data.move);
        console.log('   Agent Used:', data.agent_used);
        
        makeMove(data.move, 'O');
        
        if (checkWin('O')) {
            gameActive = false;
            gameStatus.textContent = `${data.agent_used} wins!`;
        } else if (board.every(cell => cell !== '')) {
            gameActive = false;
            gameStatus.textContent = 'Draw!';
        } else {
            gameStatus.textContent = 'Your turn!';
        }
        
    } catch (error) {
        console.error('[AI ERROR] Failed to get AI move:', error);
        gameStatus.textContent = 'AI Error - Game stopped';
        gameActive = false;
    }
}

// Convert frontend board to API format
function convertBoardToAPI(board) {
    return board.map(cell => {
        if (cell === 'X') return 1;
        if (cell === 'O') return -1;
        return 0;
    });
}

// Check for win
function checkWin(player) {
    const winPatterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ];
    
    return winPatterns.some(pattern => {
        return pattern.every(index => board[index] === player);
    });
}

// Reset game
function resetGame() {
    board = ['', '', '', '', '', '', '', '', ''];
    currentPlayer = 'X';
    gameActive = true;
    gameStatus.textContent = 'Your turn!';
    
    cells.forEach(cell => {
        cell.textContent = '';
        cell.classList.remove('taken');
    });
}

// New game
function newGame() {
    resetGame();
    // Keep current agent selection
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initGame);
