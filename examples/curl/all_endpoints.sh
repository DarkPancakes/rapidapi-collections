#!/usr/bin/env bash
# =============================================================================
# RapidAPI Collections — All Endpoints (cURL Examples)
#
# Complete reference for both APIs:
#   - Sirius Prediction Market API (8 endpoints)
#   - Screenshot & PDF API (6 endpoints)
#
# Usage:
#   1. Replace YOUR_RAPIDAPI_KEY below with your actual key
#   2. Run the whole script:  bash all_endpoints.sh
#   3. Or copy individual commands to test specific endpoints
#
# Get your key at:
#   https://rapidapi.com/louismichalot/api/sirius-prediction-market-api
#   https://rapidapi.com/louismichalot/api/screenshot-pdf-api
# =============================================================================

set -euo pipefail

API_KEY="YOUR_RAPIDAPI_KEY"

if [ "$API_KEY" = "YOUR_RAPIDAPI_KEY" ]; then
  echo "ERROR: Replace YOUR_RAPIDAPI_KEY with your actual RapidAPI key."
  echo "Edit this script or export RAPIDAPI_KEY in your shell."
  exit 1
fi

# Use env var override if available
API_KEY="${RAPIDAPI_KEY:-$API_KEY}"

SIRIUS_HOST="sirius-prediction-market-api.p.rapidapi.com"
SCREENSHOT_HOST="screenshot-pdf-api.p.rapidapi.com"

echo "=============================================="
echo " SIRIUS PREDICTION MARKET API"
echo "=============================================="

# ---------------------------------------------------------------------------
# 1. Health Check (Free) — No auth required
# ---------------------------------------------------------------------------
echo -e "\n--- 1. Health Check ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/health" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 2. Get Markets (Free) — All active prediction markets with live odds
# ---------------------------------------------------------------------------
echo -e "\n--- 2. Get Markets ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/markets" | python3 -m json.tool | head -40
echo "  ... (truncated)"

# ---------------------------------------------------------------------------
# 3. Get Signals (Free) — Trading signals from 28+ sources
#    Params: limit (1-500), layer (L1|L3|L4|L5|L6), min_gap (0-1)
# ---------------------------------------------------------------------------
echo -e "\n--- 3. Get Signals (all, limit 10) ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/signals?limit=10" | python3 -m json.tool

echo -e "\n--- 3b. Get Signals (L1 only, min gap 5%) ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/signals?layer=L1&min_gap=0.05&limit=5" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 4. Signals History (Free) — Past signals and trade outcomes
# ---------------------------------------------------------------------------
echo -e "\n--- 4. Signals History ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/signals/history" | python3 -m json.tool | head -40
echo "  ... (truncated)"

# ---------------------------------------------------------------------------
# 5. Get Sentiment (Free) — Fear & Greed, long/short ratios
# ---------------------------------------------------------------------------
echo -e "\n--- 5. Get Sentiment ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/sentiment" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 6. Get Sports Odds (Free) — ESPN + Kalshi live sports
# ---------------------------------------------------------------------------
echo -e "\n--- 6. Get Sports Odds ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/sports" | python3 -m json.tool | head -40
echo "  ... (truncated)"

# ---------------------------------------------------------------------------
# 7. Get Weather (Free) — Weather-linked prediction markets
# ---------------------------------------------------------------------------
echo -e "\n--- 7. Get Weather ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/weather" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 8. Get Odds Comparison (Free) — Cross-platform odds
# ---------------------------------------------------------------------------
echo -e "\n--- 8. Get Odds Comparison ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/odds" | python3 -m json.tool | head -40
echo "  ... (truncated)"

# ---------------------------------------------------------------------------
# 9. Get Performance (Basic tier) — Bot track record
# ---------------------------------------------------------------------------
echo -e "\n--- 9. Get Performance (Basic tier) ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/performance" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 10. Get Trades (Basic tier) — Recent trades with P&L
# ---------------------------------------------------------------------------
echo -e "\n--- 10. Get Trades (Basic tier) ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/trades" | python3 -m json.tool | head -40
echo "  ... (truncated)"

# ---------------------------------------------------------------------------
# 11. Get AI Brain (Pro tier) — AI reasoning engine
# ---------------------------------------------------------------------------
echo -e "\n--- 11. Get AI Brain (Pro tier) ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SIRIUS_HOST" \
  "https://$SIRIUS_HOST/v1/brain" | python3 -m json.tool


echo -e "\n\n=============================================="
echo " SCREENSHOT & PDF API"
echo "=============================================="

# ---------------------------------------------------------------------------
# 12. Health Check (Free)
# ---------------------------------------------------------------------------
echo -e "\n--- 12. Screenshot API Health ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  "https://$SCREENSHOT_HOST/v1/health" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 13. Screenshot URL as PNG (Free)
# ---------------------------------------------------------------------------
echo -e "\n--- 13. Screenshot (PNG) ---"
curl -s -o screenshot_github.png \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  "https://$SCREENSHOT_HOST/v1/screenshot?url=https://github.com&width=1280&height=800&format=png"
echo "Saved screenshot_github.png ($(wc -c < screenshot_github.png) bytes)"

# ---------------------------------------------------------------------------
# 14. Screenshot as JPEG with quality (Free)
# ---------------------------------------------------------------------------
echo -e "\n--- 14. Screenshot (JPEG, quality 90) ---"
curl -s -o screenshot_hn.jpg \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  "https://$SCREENSHOT_HOST/v1/screenshot?url=https://news.ycombinator.com&format=jpeg&quality=90"
echo "Saved screenshot_hn.jpg ($(wc -c < screenshot_hn.jpg) bytes)"

# ---------------------------------------------------------------------------
# 15. Full-page screenshot (Free)
# ---------------------------------------------------------------------------
echo -e "\n--- 15. Full-page screenshot ---"
curl -s -o screenshot_wiki_full.png \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  "https://$SCREENSHOT_HOST/v1/screenshot?url=https://en.wikipedia.org/wiki/API&full_page=true&format=png"
echo "Saved screenshot_wiki_full.png ($(wc -c < screenshot_wiki_full.png) bytes)"

# ---------------------------------------------------------------------------
# 16. Generate PDF (Basic tier)
# ---------------------------------------------------------------------------
echo -e "\n--- 16. Generate PDF (A4) ---"
curl -s -o github.pdf \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  "https://$SCREENSHOT_HOST/v1/pdf?url=https://github.com&format=A4&margin=normal"
echo "Saved github.pdf ($(wc -c < github.pdf) bytes)"

# ---------------------------------------------------------------------------
# 17. Extract Metadata & OG Tags (Basic tier)
# ---------------------------------------------------------------------------
echo -e "\n--- 17. Extract Metadata ---"
curl -s \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  "https://$SCREENSHOT_HOST/v1/metadata?url=https://github.com" | python3 -m json.tool

# ---------------------------------------------------------------------------
# 18. HTML to Image (Pro tier) — Render custom HTML/CSS
# ---------------------------------------------------------------------------
echo -e "\n--- 18. HTML to Image (Pro tier) ---"
curl -s -o html_render.png \
  -X POST \
  -H "X-RapidAPI-Key: $API_KEY" \
  -H "X-RapidAPI-Host: $SCREENSHOT_HOST" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<div style=\"padding:40px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;font-family:Arial;border-radius:16px\"><h1>Hello World</h1><p>Generated with Screenshot & PDF API</p></div>",
    "width": 800,
    "height": 400,
    "format": "png"
  }' \
  "https://$SCREENSHOT_HOST/v1/screenshot/html"
echo "Saved html_render.png ($(wc -c < html_render.png) bytes)"

echo -e "\n=============================================="
echo " Done! All endpoints tested."
echo "=============================================="
