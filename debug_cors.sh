#!/bin/bash

echo "=========================================="
echo "CORS DEBUGGING TOOL"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

RENDER_URL="https://tictactoe-qlearning.onrender.com"
GITHUB_ORIGIN="https://xircons.github.io"

echo "1. Testing Render.com Backend Health..."
echo "----------------------------------------"

# Test basic connectivity
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "$RENDER_URL/api/health")
HTTP_CODE=$(echo "$HEALTH_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$HEALTH_RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Backend is responding${NC}"
    echo "Response: $RESPONSE_BODY"
else
    echo -e "${RED}✗ Backend returned status: $HTTP_CODE${NC}"
    echo "Response: $RESPONSE_BODY"
fi
echo ""

echo "2. Testing CORS Headers from Render.com..."
echo "----------------------------------------"

# Test CORS headers with GitHub Pages origin
CORS_TEST=$(curl -s -I \
  -H "Origin: $GITHUB_ORIGIN" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: Content-Type" \
  "$RENDER_URL/api/health")

echo "Full Response Headers:"
echo "$CORS_TEST"
echo ""

# Check for specific CORS headers
if echo "$CORS_TEST" | grep -qi "access-control-allow-origin"; then
    ALLOWED_ORIGIN=$(echo "$CORS_TEST" | grep -i "access-control-allow-origin" | cut -d' ' -f2- | tr -d '\r')
    echo -e "${GREEN}✓ CORS headers present${NC}"
    echo "Allowed Origin: $ALLOWED_ORIGIN"
    
    if echo "$ALLOWED_ORIGIN" | grep -q "$GITHUB_ORIGIN"; then
        echo -e "${GREEN}✓ GitHub Pages origin is allowed!${NC}"
    else
        echo -e "${RED}✗ GitHub Pages origin NOT allowed${NC}"
        echo -e "${YELLOW}Expected: $GITHUB_ORIGIN${NC}"
        echo -e "${YELLOW}Got: $ALLOWED_ORIGIN${NC}"
    fi
else
    echo -e "${RED}✗ NO CORS headers found!${NC}"
    echo -e "${YELLOW}This means Render.com is running OLD code without CORS fix${NC}"
fi
echo ""

echo "3. Checking Local Backend CORS Configuration..."
echo "----------------------------------------"

if [ -f "backend/main.py" ]; then
    echo "Checking backend/main.py for CORS origins..."
    if grep -q "https://xircons.github.io" backend/main.py; then
        echo -e "${GREEN}✓ CORS fix present in local code${NC}"
        echo "Found GitHub Pages origin in backend/main.py"
    else
        echo -e "${RED}✗ CORS fix NOT found in local code${NC}"
    fi
else
    echo -e "${RED}✗ backend/main.py not found${NC}"
fi
echo ""

echo "4. Checking Git Status..."
echo "----------------------------------------"

# Check if there are unpushed commits
UNPUSHED=$(git log origin/prototype..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')

if [ "$UNPUSHED" -gt 0 ]; then
    echo -e "${YELLOW}⚠ You have $UNPUSHED unpushed commit(s)${NC}"
    echo "Unpushed commits:"
    git log origin/prototype..HEAD --oneline
    echo ""
    echo -e "${YELLOW}→ Push these to GitHub to trigger Render deployment${NC}"
else
    echo -e "${GREEN}✓ All commits are pushed${NC}"
fi
echo ""

echo "5. Diagnosis & Solution..."
echo "----------------------------------------"

# Determine the issue
CORS_HEADERS_PRESENT=$(echo "$CORS_TEST" | grep -qi "access-control-allow-origin" && echo "yes" || echo "no")
CORS_FIX_IN_CODE=$(grep -q "https://xircons.github.io" backend/main.py 2>/dev/null && echo "yes" || echo "no")

if [ "$CORS_HEADERS_PRESENT" = "no" ] && [ "$CORS_FIX_IN_CODE" = "yes" ]; then
    echo -e "${RED}PROBLEM: Render.com is running OLD code${NC}"
    echo ""
    echo "The CORS fix exists in your local code but Render hasn't deployed it yet."
    echo ""
    echo -e "${GREEN}SOLUTION:${NC}"
    if [ "$UNPUSHED" -gt 0 ]; then
        echo "1. Push your commits to GitHub"
        echo "   → Use GitHub Desktop or: git push origin prototype"
    else
        echo "1. Manually trigger Render deployment:"
        echo "   → Go to: https://dashboard.render.com"
        echo "   → Find your service: tictactoe-qlearning"
        echo "   → Click 'Manual Deploy' → 'Deploy latest commit'"
    fi
    echo "2. Wait 3-5 minutes for deployment"
    echo "3. Run this script again to verify"
    
elif [ "$CORS_HEADERS_PRESENT" = "yes" ]; then
    echo -e "${GREEN}✓ CORS is configured correctly!${NC}"
    echo ""
    echo "The backend is properly configured. If your frontend still shows errors:"
    echo "1. Hard refresh your browser (Ctrl+Shift+R or Cmd+Shift+R)"
    echo "2. Clear browser cache"
    echo "3. Check browser console for other errors"
    
elif [ "$CORS_FIX_IN_CODE" = "no" ]; then
    echo -e "${RED}PROBLEM: CORS fix missing from code${NC}"
    echo ""
    echo "Your backend/main.py doesn't include the GitHub Pages origin."
    echo ""
    echo -e "${GREEN}SOLUTION:${NC}"
    echo "Update backend/main.py to include:"
    echo "  origins: ["
    echo "    \"https://xircons.github.io\","
    echo "    ..."
    echo "  ]"
fi

echo ""
echo "=========================================="
echo "Debug complete!"
echo "=========================================="

