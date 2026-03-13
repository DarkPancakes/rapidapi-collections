#!/usr/bin/env node
/**
 * Sirius Prediction Market API — Fetch & Display Trading Signals (Node.js)
 *
 * Retrieves live trading signals from 28+ cross-platform sources,
 * optionally filters by layer, and prints a formatted table.
 *
 * Layers:
 *   L1 = Price lag arbitrage (Polymarket)
 *   L3 = Weather forecasts (NOAA/NHC/USGS)
 *   L4 = Kalshi cross-platform odds
 *   L5 = Sports (ESPN) + Kalshi politics
 *   L6 = News-driven signals
 *
 * Usage:
 *   node getSignals.js              # all signals
 *   node getSignals.js --layer L1   # price-lag signals only
 *   node getSignals.js --min-gap 0.08  # gap >= 8%
 *
 * Requirements: Node.js 18+ (native fetch)
 */

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const API_KEY = "YOUR_RAPIDAPI_KEY";
const API_HOST = "sirius-prediction-market-api.p.rapidapi.com";
const BASE_URL = `https://${API_HOST}/v1`;

const LAYER_NAMES = {
  L1: "Price Lag",
  L3: "Weather",
  L4: "Kalshi",
  L5: "Sports/Pol",
  L6: "News",
};

// ---------------------------------------------------------------------------
// CLI argument parsing (no dependencies needed)
// ---------------------------------------------------------------------------
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { limit: 50, layer: null, minGap: null };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--layer":
        opts.layer = args[++i];
        break;
      case "--min-gap":
        opts.minGap = parseFloat(args[++i]);
        break;
      case "--limit":
        opts.limit = parseInt(args[++i], 10);
        break;
      case "--help":
        console.log("Usage: node getSignals.js [--layer L1|L3|L4|L5|L6] [--min-gap 0.05] [--limit 50]");
        process.exit(0);
    }
  }
  return opts;
}

// ---------------------------------------------------------------------------
// API
// ---------------------------------------------------------------------------
async function fetchSignals({ limit, layer, minGap }) {
  const params = new URLSearchParams({ limit: String(limit) });
  if (layer) params.set("layer", layer);
  if (minGap !== null) params.set("min_gap", String(minGap));

  const url = `${BASE_URL}/signals?${params}`;
  const resp = await fetch(url, {
    headers: {
      "X-RapidAPI-Key": API_KEY,
      "X-RapidAPI-Host": API_HOST,
    },
  });

  if (!resp.ok) {
    throw new Error(`API returned ${resp.status}: ${await resp.text()}`);
  }

  return resp.json();
}

// ---------------------------------------------------------------------------
// Display
// ---------------------------------------------------------------------------
function formatAge(timestamp) {
  if (!timestamp) return "-";
  try {
    const dt = new Date(timestamp);
    const ageSec = (Date.now() - dt.getTime()) / 1000;
    if (ageSec < 60) return `${Math.floor(ageSec)}s ago`;
    if (ageSec < 3600) return `${Math.floor(ageSec / 60)}m ago`;
    return `${(ageSec / 3600).toFixed(1)}h ago`;
  } catch {
    return timestamp.slice(0, 10);
  }
}

function pct(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function printTable(signals) {
  if (!signals.length) {
    console.log("No signals found.");
    return;
  }

  // Header
  const header =
    "Layer".padEnd(10) + " | " +
    "Market".padEnd(42) + " | " +
    "Side".padEnd(6) + " | " +
    "Odds".padStart(7) + " | " +
    "Gap".padStart(7) + " | " +
    "Age".padEnd(10);

  const sep = "-".repeat(10) + "-+-" +
    "-".repeat(42) + "-+-" +
    "-".repeat(6) + "-+-" +
    "-".repeat(7) + "-+-" +
    "-".repeat(7) + "-+-" +
    "-".repeat(10);

  console.log(header);
  console.log(sep);

  for (const s of signals) {
    const layer = LAYER_NAMES[s.layer] || s.layer || "?";
    let market = s.market || s.question || "Unknown";
    if (market.length > 42) market = market.slice(0, 39) + "...";
    const side = String(s.side || s.direction || "?");
    const odds = s.odds ?? s.price ?? 0;
    const gap = s.gap ?? 0;
    const age = formatAge(s.timestamp || s.detected_at);

    console.log(
      layer.padEnd(10) + " | " +
      market.padEnd(42) + " | " +
      side.padEnd(6) + " | " +
      pct(odds).padStart(7) + " | " +
      pct(gap).padStart(7) + " | " +
      age.padEnd(10)
    );
  }
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function main() {
  if (API_KEY === "YOUR_RAPIDAPI_KEY") {
    console.error("ERROR: Replace YOUR_RAPIDAPI_KEY with your actual key.");
    console.error("Get one at: https://rapidapi.com/louismichalot/api/sirius-prediction-market-api");
    process.exit(1);
  }

  const opts = parseArgs();
  console.log(`Fetching signals (layer=${opts.layer || "all"}, min_gap=${opts.minGap ?? "any"})...\n`);

  const data = await fetchSignals(opts);
  const signals = Array.isArray(data) ? data : (data.signals || data.data || []);

  console.log(`Found ${signals.length} signal(s):\n`);
  printTable(signals);
}

main().catch((err) => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
