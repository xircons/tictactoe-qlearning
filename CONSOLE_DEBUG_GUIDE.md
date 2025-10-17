# Console Debug Guide 🐛

## Browser Console Logging for Backend Debugging

Your Tic-Tac-Toe game now includes comprehensive console logging to help you debug the connection between your frontend and the Perfect Minimax AI backend.

## How to View Console Logs

1. **Open Developer Tools**:
   - **Chrome/Edge**: Press `F12` or `Ctrl+Shift+J` (Windows) / `Cmd+Option+J` (Mac)
   - **Firefox**: Press `F12` or `Ctrl+Shift+K` (Windows) / `Cmd+Option+K` (Mac)
   - **Safari**: Press `Cmd+Option+C`

2. **Click on the "Console" tab**

3. **Play the game** - logs will appear in real-time!

## What You'll See

### 📦 On Page Load (Initialization)

```
🎮 [GAME INIT] Tic-Tac-Toe with Perfect Minimax AI
📦 [CONFIG] API Configuration loaded:
   🌍 Environment: Production (GitHub Pages)
   📡 Backend URL: https://tictactoe-qlearning.onrender.com
   🔗 Health Endpoint: https://tictactoe-qlearning.onrender.com/api/health
   🎯 Move Endpoint: https://tictactoe-qlearning.onrender.com/api/move
   🤖 AI Agent: Perfect Minimax (backend/agents/perfect_agent.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 🏥 When Game Starts (Health Check)

**✅ If Backend is Online:**
```
🏥 [HEALTH CHECK] Testing backend connection...
   📡 API URL: https://tictactoe-qlearning.onrender.com/api/health
✅ [HEALTH CHECK] Backend is ONLINE!
   🤖 Agent: Perfect Minimax AI
   💬 Message: Tic-Tac-Toe API is running
   ⏱️  Response Time: 1234.56ms
   🔗 Connected to: backend/agents/perfect_agent.py
```

**⚠️ If Backend is Offline:**
```
🏥 [HEALTH CHECK] Testing backend connection...
   📡 API URL: https://tictactoe-qlearning.onrender.com/api/health
⚠️  [HEALTH CHECK] Backend is OFFLINE
   📡 Attempted URL: https://tictactoe-qlearning.onrender.com/api/health
   ❌ Error: Failed to fetch
   🔄 Fallback: Using random AI moves
```

### 🤖 When AI Makes a Move

**✅ Successful API Call:**
```
🤖 [AI REQUEST] Calling Perfect Minimax Agent...
   📡 API URL: https://tictactoe-qlearning.onrender.com/api/move
   📊 Board State: [1, 0, 0, 0, 0, 0, 0, 0, 0]
   🎮 Player: -1 (AI plays O)
✅ [AI RESPONSE] Perfect Minimax move received!
   🎯 AI Move: 4
   📊 Updated Board: [1, 0, 0, 0, -1, 0, 0, 0, 0]
   ⏱️  Response Time: 567.89ms
   🏆 Game Over: false
   💬 Message: AI plays position 4
```

**❌ Failed API Call:**
```
🤖 [AI REQUEST] Calling Perfect Minimax Agent...
   📡 API URL: https://tictactoe-qlearning.onrender.com/api/move
   📊 Board State: [1, 0, 0, 0, 0, 0, 0, 0, 0]
   🎮 Player: -1 (AI plays O)
❌ [API ERROR] Request failed: 502 Bad Gateway
❌ [API ERROR] Failed to connect to backend: Error: API request failed: 502
   🔧 Troubleshooting: Check if backend is running at: https://tictactoe-qlearning.onrender.com
```

## 🔍 Debugging Tips

### 1. **Check Environment Detection**
Look at the initialization logs to confirm:
- ✅ Correct environment detected (Production vs Local)
- ✅ Correct backend URL being used

### 2. **Monitor Response Times**
- **< 100ms**: Excellent (local or cached)
- **100-500ms**: Good (typical API response)
- **500-2000ms**: Slow (backend might be waking up from sleep)
- **> 2000ms**: Very slow (check Render.com status)

### 3. **Watch for API Availability**
- If you see "Backend is OFFLINE", check:
  1. Is your Render.com service running?
  2. Did the free tier spin down? (Wait 30-50s for first request)
  3. Is there a CORS error? (Should be configured correctly)

### 4. **Verify Board States**
The logs show:
- **Board State** before AI move: `[1, 0, 0, 0, 0, 0, 0, 0, 0]`
- **Updated Board** after AI move: `[1, 0, 0, 0, -1, 0, 0, 0, 0]`

Where:
- `1` = X (Player)
- `-1` = O (AI)
- `0` = Empty

## 🎯 Common Issues & Solutions

### Issue 1: "Backend is OFFLINE" on First Load
**Cause**: Render free tier spins down after inactivity  
**Solution**: Wait 30-50 seconds and try again. First request wakes up the service.

### Issue 2: CORS Error
**Cause**: Backend not configured for your domain  
**Solution**: Already configured! Should work automatically.

### Issue 3: Random AI Instead of Perfect AI
**Cause**: Backend connection failed  
**Solution**: Check console logs for error details. Backend might be starting up.

### Issue 4: Slow Response Times
**Cause**: Backend waking up from sleep or network latency  
**Solution**: Normal for first request. Subsequent requests will be faster.

## 🚀 Testing Locally

To test with local backend:

1. **Start local backend**:
   ```bash
   cd backend
   source ../venv/bin/activate
   python main.py
   ```

2. **Open `index.html` locally**:
   ```bash
   cd frontend/public
   python -m http.server 8080
   ```

3. **Check console** - Should show:
   ```
   🌍 Environment: Local Development
   📡 Backend URL: http://localhost:5001
   ```

## 📊 Performance Benchmarks

Typical response times:
- **Health Check**: 50-200ms
- **AI Move (Minimax)**: 100-500ms
- **First Request (Cold Start)**: 30-50 seconds

## 🎮 Happy Debugging!

Now you can see exactly what's happening when your frontend talks to your Perfect Minimax AI backend!

---

**Questions or Issues?**
Check the console logs first - they'll tell you exactly what's going on! 🔍

