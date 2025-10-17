// API Configuration for Tic-Tac-Toe Game
const API_CONFIG = {
    // Production API URL - Your deployed Render backend
    PRODUCTION_URL: 'https://tictactoe-qlearning.onrender.com',
    
    // Local development URL
    LOCAL_URL: 'http://localhost:5001',
    
    // Auto-detect environment
    getBaseUrl() {
        let url;
        // Check if we're running on GitHub Pages
        if (window.location.hostname.includes('github.io')) {
            url = this.PRODUCTION_URL;
        }
        // Check if we're running locally
        else if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            url = this.LOCAL_URL;
        }
        // Default to production
        else {
            url = this.PRODUCTION_URL;
        }
        
        console.log(`🌐 Using API URL: ${url}`);
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

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
