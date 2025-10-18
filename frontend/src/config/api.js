// API Configuration for Tic-Tac-Toe Game
const API_CONFIG = {
    // Production API URL - Your deployed Render backend
    PRODUCTION_URL: import.meta.env.VITE_API_PRODUCTION_URL || 'https://tictactoe-qlearning.onrender.com',
    
    // Local development URL (now points to Render.com for consistency)
    LOCAL_URL: import.meta.env.VITE_API_LOCAL_URL || 'https://tictactoe-qlearning.onrender.com',
    
    // Auto-detect environment
    getBaseUrl() {
        let url;
        // Always use production URL (Render.com) for consistency
        // This ensures both local development and production use the same backend
        url = this.PRODUCTION_URL;
        
        console.log(`Using API URL: ${url}`);
        return url;
    },
    
    // API endpoints
    ENDPOINTS: {
        HEALTH: '/api/health',
        MOVE: '/api/move',
        VALIDATE: '/api/validate'
    },
    
    // Request timeout (milliseconds)
    TIMEOUT: 10000,
    
    // Retry configuration
    MAX_RETRIES: 3,
    RETRY_DELAY: 1000
};

export default API_CONFIG;
