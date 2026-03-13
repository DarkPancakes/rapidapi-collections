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

## Quick Start

### Import in Postman
1. Open Postman
2. Click **Import** → drag the `.json` file
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
