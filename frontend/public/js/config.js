// API Configuration for Tic-Tac-Toe Game
const API_CONFIG = {
    // Production API URL (update this with your deployed backend URL)
    PRODUCTION_URL: 'https://tictactoe-qlearning.onrender.com',
    
    // Local development URL
    LOCAL_URL: 'http://localhost:5001',
    
    // Auto-detect environment
    getBaseUrl() {
        // Check if we're running on GitHub Pages
        if (window.location.hostname.includes('github.io')) {
            return this.PRODUCTION_URL;
        }
        // Check if we're running locally
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.LOCAL_URL;
        }
        // Default to production
        return this.PRODUCTION_URL;
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

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
