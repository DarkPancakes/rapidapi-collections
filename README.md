# RapidAPI Collections

Postman collections and code examples for my RapidAPI APIs.

## APIs

### Sirius Prediction Market API
Real-time prediction market data from 28+ cross-platform sources — live Polymarket odds, algorithmic trading signals, sentiment analysis, sports odds, weather forecasts. Sorting, source filtering, pagination, equity curve.

- **RapidAPI:** [Sirius Prediction Market API](https://rapidapi.com/louismichalot/api/sirius-prediction-market-api)
- **npm:** [`sirius-prediction-api`](https://www.npmjs.com/package/sirius-prediction-api) — `npm install sirius-prediction-api`
- **PyPI:** [`sirius-prediction-api`](https://pypi.org/project/sirius-prediction-api/) — `pip install sirius-prediction-api`
- **Postman Collection:** [sirius-postman-collection.json](./sirius-postman-collection.json)
- **Free tier:** 50 requests/day

### Screenshot & PDF API
Screenshot URLs to PNG/JPEG/WebP, generate PDFs, extract metadata & OG tags, render HTML to images. Device presets (iPhone, iPad, Pixel, Galaxy), dark mode, JavaScript execution, configurable wait strategy. Powered by headless Chromium.

- **RapidAPI:** [Screenshot & PDF API](https://rapidapi.com/louismichalot/api/screenshot-pdf-api)
- **npm:** [`screenshot-pdf-api`](https://www.npmjs.com/package/screenshot-pdf-api) — `npm install screenshot-pdf-api`
- **PyPI:** [`screenshot-pdf-api`](https://pypi.org/project/screenshot-pdf-api/) — `pip install screenshot-pdf-api`
- **Postman Collection:** [screenshot-postman-collection.json](./screenshot-postman-collection.json)
- **Free tier:** 20 screenshots/day

### Text-to-Speech API
High-quality text-to-speech with 320+ neural voices in 75+ languages. SSML support, real-time streaming, batch processing, volume control, word-level timestamps. Voice filtering by gender, personality, category.

- **RapidAPI:** [Text-to-Speech API](https://rapidapi.com/louismichalot/api/text-to-speech-api)
- **npm:** [`rapidapi-tts`](https://www.npmjs.com/package/rapidapi-tts) — `npm install rapidapi-tts`
- **PyPI:** [`text-to-speech-api`](https://pypi.org/project/text-to-speech-api/) — `pip install text-to-speech-api`
- **Postman Collection:** [tts-postman-collection.json](./tts-postman-collection.json)
- **Free tier:** 50 requests/day

## Code Examples

Ready-to-run examples in Python, Node.js, and cURL. Replace `YOUR_RAPIDAPI_KEY` with your key and go.

### Python

| Example | Description |
|---------|-------------|
| [get_signals.py](./examples/python/get_signals.py) | Fetch trading signals, filter by layer/source, sort by gap/confidence |
| [screenshot.py](./examples/python/screenshot.py) | Capture a URL with device presets, dark mode, and JS execution |
| [market_monitor.py](./examples/python/market_monitor.py) | Poll markets every 60s, detect odds changes > 5%, print color-coded alerts |

```bash
# Install dependency
pip install requests

# Fetch all signals sorted by gap
python examples/python/get_signals.py --sort-by gap

# Only price-lag signals with gap >= 8%
python examples/python/get_signals.py --layer L1 --min-gap 0.08

# Screenshot as iPhone in dark mode
python examples/python/screenshot.py https://github.com --device iphone-14 --dark-mode

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

# Fetch signals sorted by confidence
node examples/node/getSignals.js --layer L1 --sort-by confidence

# Take a screenshot as iPad
node examples/node/screenshot.js https://github.com --device ipad-pro -o github.png
```

### cURL

| Example | Description |
|---------|-------------|
| [all_endpoints.sh](./examples/curl/all_endpoints.sh) | Every endpoint for all 3 APIs with example parameters |

```bash
# Run all endpoints
bash examples/curl/all_endpoints.sh

# Or copy individual commands from the script
```

## SDK Packages

### Sirius Prediction Market API

```bash
npm install sirius-prediction-api    # Node.js 18+
pip install sirius-prediction-api    # Python 3.8+
```

```javascript
// Node.js
import SiriusAPI from 'sirius-prediction-api';
const api = new SiriusAPI('YOUR_RAPIDAPI_KEY');
const signals = await api.signals({ layer: 'L1', min_gap: 0.05, sort_by: 'gap' });
```

```python
# Python
from sirius_prediction_api import SiriusAPI
api = SiriusAPI("YOUR_RAPIDAPI_KEY")
signals = api.signals(layer="L1", min_gap=0.05, sort_by="gap")
```

### Screenshot & PDF API

```bash
npm install screenshot-pdf-api    # Node.js 18+
pip install screenshot-pdf-api    # Python 3.8+
```

```javascript
// Node.js
import ScreenshotAPI from 'screenshot-pdf-api';
const api = new ScreenshotAPI('YOUR_RAPIDAPI_KEY');
const img = await api.screenshot('https://github.com', { device: 'iphone-14', dark_mode: true });
```

```python
# Python
from screenshot_pdf_api import ScreenshotAPI
api = ScreenshotAPI("YOUR_RAPIDAPI_KEY")
img = api.screenshot("https://github.com", device="iphone-14", dark_mode=True)
```

### Text-to-Speech API

```bash
npm install rapidapi-tts           # Node.js 18+
pip install text-to-speech-api     # Python 3.8+
```

```javascript
// Node.js
import TTSAPI from 'rapidapi-tts';
const api = new TTSAPI('YOUR_RAPIDAPI_KEY');
const audio = await api.tts({ text: 'Hello!', voice: 'en-US-AriaNeural', volume: '+20%' });
const stream = await api.stream({ text: 'Streaming!', voice: 'en-US-GuyNeural' });
const batch = await api.batch([
  { text: 'Hello', voice: 'en-US-AriaNeural' },
  { text: 'Bonjour', voice: 'fr-FR-DeniseNeural' },
]);
```

```python
# Python
from tts_api import TTSAPI
api = TTSAPI("YOUR_RAPIDAPI_KEY")
audio = api.tts("Hello!", voice="en-US-AriaNeural", volume="+20%")
stream = api.stream("Streaming!", voice="en-US-GuyNeural")
batch = api.batch([
    {"text": "Hello", "voice": "en-US-AriaNeural"},
    {"text": "Bonjour", "voice": "fr-FR-DeniseNeural"},
])
```

## Quick Start

### Python
```python
import requests

headers = {
    "X-RapidAPI-Key": "YOUR_KEY",
    "X-RapidAPI-Host": "sirius-prediction-market-api.p.rapidapi.com"
}

# Get trading signals sorted by gap
r = requests.get(
    "https://sirius-prediction-market-api.p.rapidapi.com/v1/signals",
    params={"sort_by": "gap", "limit": 10},
    headers=headers,
)
print(r.json())
```

### JavaScript
```javascript
const response = await fetch(
  "https://sirius-prediction-market-api.p.rapidapi.com/v1/signals?sort_by=gap&limit=10",
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
# Screenshot with iPhone preset + dark mode
curl -o screenshot.png \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: screenshot-pdf-api.p.rapidapi.com" \
  "https://screenshot-pdf-api.p.rapidapi.com/v1/screenshot?url=https://github.com&device=iphone-14&dark_mode=true"

# Text-to-Speech with volume
curl -o speech.mp3 \
  -X POST \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: text-to-speech-api8.p.rapidapi.com" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world!", "voice": "en-US-AriaNeural", "volume": "+20%", "format": "mp3"}' \
  "https://text-to-speech-api8.p.rapidapi.com/v1/tts"

# Stream TTS (Basic+)
curl -o stream.mp3 \
  -X POST \
  -H "X-RapidAPI-Key: YOUR_KEY" \
  -H "X-RapidAPI-Host: text-to-speech-api8.p.rapidapi.com" \
  -H "Content-Type: application/json" \
  -d '{"text": "Real-time streaming!", "voice": "en-US-GuyNeural"}' \
  "https://text-to-speech-api8.p.rapidapi.com/v1/tts/stream"
```
