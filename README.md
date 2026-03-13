# RapidAPI Collections

Postman collections and code examples for my RapidAPI APIs.

## APIs

### Sirius Prediction Market API
Real-time prediction market data from 28+ cross-platform sources — live Polymarket odds, algorithmic trading signals, sentiment analysis, sports odds, weather forecasts.

- **RapidAPI:** [Sirius Prediction Market API](https://rapidapi.com/louismichalot/api/sirius-prediction-market-api)
- **Postman Collection:** [sirius-postman-collection.json](./sirius-postman-collection.json)
- **Free tier:** 50 requests/day

### Screenshot & PDF API
Screenshot URLs to PNG/JPEG/WebP, generate PDFs, extract metadata & OG tags, render HTML to images. Powered by headless Chromium.

- **RapidAPI:** [Screenshot & PDF API](https://rapidapi.com/louismichalot/api/screenshot-pdf-api)
- **Postman Collection:** [screenshot-postman-collection.json](./screenshot-postman-collection.json)
- **Free tier:** 20 screenshots/day

## Code Examples

Ready-to-run examples in Python, Node.js, and cURL. Replace `YOUR_RAPIDAPI_KEY` with your key and go.

### Python

| Example | Description |
|---------|-------------|
| [get_signals.py](./examples/python/get_signals.py) | Fetch trading signals, filter by layer (L1-L6), display as formatted table |
| [screenshot.py](./examples/python/screenshot.py) | Capture a URL as PNG/JPEG/WebP with custom viewport, full-page, and delay options |
| [market_monitor.py](./examples/python/market_monitor.py) | Poll markets every 60s, detect odds changes > 5%, print color-coded alerts |

```bash
# Install dependency
pip install requests

# Fetch all signals
python examples/python/get_signals.py

# Only price-lag signals with gap >= 8%
python examples/python/get_signals.py --layer L1 --min-gap 0.08

# Screenshot a URL
python examples/python/screenshot.py https://github.com --format jpeg --quality 90

# Monitor markets for big moves
python examples/python/market_monitor.py --threshold 0.03 --interval 30
```

### Node.js

| Example | Description |
|---------|-------------|
| [getSignals.js](./examples/node/getSignals.js) | Fetch and display trading signals with formatted table output |
| [screenshot.js](./examples/node/screenshot.js) | Capture URLs to image files with full CLI options |

```bash
# Requires Node.js 18+ (native fetch)

# Fetch signals
node examples/node/getSignals.js --layer L1

# Take a screenshot
node examples/node/screenshot.js https://github.com --full-page -o github.png
```

### cURL

| Example | Description |
|---------|-------------|
| [all_endpoints.sh](./examples/curl/all_endpoints.sh) | Every endpoint for both APIs with example parameters |

```bash
# Run all endpoints
bash examples/curl/all_endpoints.sh

# Or copy individual commands from the script
```

## Quick Start

### Import in Postman
1. Open Postman
2. Click **Import** -> drag the `.json` file
3. Set the `rapidApiKey` variable to your RapidAPI key
4. Start testing

### Python
```python
import requests

headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "sirius-prediction-market-api.p.rapidapi.com"
}

# Get trading signals
r = requests.get("https://sirius-prediction-market-api.p.rapidapi.com/v1/signals", headers=headers)
print(r.json())
```

### JavaScript
```javascript
const response = await fetch(
  "https://sirius-prediction-market-api.p.rapidapi.com/v1/signals",
  {
    headers: {
      "X-RapidAPI-Key": "YOUR_KEY",
      "X-RapidAPI-Host": "sirius-prediction-market-api.p.rapidapi.com"
    }
  }
);
const data = await response.json();
console.log(data);
```

### cURL
```bash
# Screenshot
curl -o screenshot.png \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: screenshot-pdf-api.p.rapidapi.com" \
  "https://screenshot-pdf-api.p.rapidapi.com/v1/screenshot?url=https://github.com"
```
