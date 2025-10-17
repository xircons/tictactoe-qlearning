#!/bin/bash

echo "🧪 Testing Tic-Tac-Toe Backend API"
echo "=================================="

# Test 1: Health Check
echo "1. Testing Health Check..."
response=$(curl -s -H "Origin: https://xircons.github.io" http://localhost:5001/api/health)
if echo "$response" | grep -q "Perfect Minimax AI"; then
    echo "   ✅ Health check passed"
else
    echo "   ❌ Health check failed"
    echo "   Response: $response"
fi

# Test 2: CORS Headers
echo "2. Testing CORS Headers..."
cors_origin=$(curl -s -H "Origin: https://xircons.github.io" -I http://localhost:5001/api/health | grep -i "access-control-allow-origin")
if echo "$cors_origin" | grep -q "xircons.github.io"; then
    echo "   ✅ CORS headers correct"
else
    echo "   ❌ CORS headers missing"
    echo "   Headers: $cors_origin"
fi

# Test 3: AI Move
echo "3. Testing AI Move..."
move_response=$(curl -s -H "Origin: https://xircons.github.io" -H "Content-Type: application/json" \
    -X POST -d '{"board": [0, 1, -1, 0, 0, 0, 0, 0, 0], "player": -1}' \
    http://localhost:5001/api/move)
if echo "$move_response" | grep -q '"move"'; then
    echo "   ✅ AI move successful"
    echo "   Response: $move_response"
else
    echo "   ❌ AI move failed"
    echo "   Response: $move_response"
fi

echo ""
echo "🎮 Local Backend Test Complete!"
echo "Next: Push to GitHub to deploy CORS fix to Render"
