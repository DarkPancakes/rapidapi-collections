#!/usr/bin/env python3
"""
Sirius Prediction Market API — Fetch & Display Trading Signals

Retrieves live trading signals from 28+ cross-platform sources,
filters by layer, and displays them as a formatted table.

Layers:
  L1 = Price lag arbitrage (Polymarket)
  L3 = Weather forecasts (NOAA/NHC/USGS)
  L4 = Kalshi cross-platform odds
  L5 = Sports (ESPN) + Kalshi politics
  L6 = News-driven signals

Usage:
  python get_signals.py              # all signals
  python get_signals.py --layer L1   # only price-lag signals
  python get_signals.py --min-gap 0.08  # only signals with gap >= 8%

Requirements:
  pip install requests
"""

import argparse
import sys
from datetime import datetime

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "sirius-prediction-market-api.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}/v1"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
}

# Layer labels for display
LAYER_NAMES = {
    "L1": "Price Lag",
    "L3": "Weather",
    "L4": "Kalshi",
    "L5": "Sports/Politics",
    "L6": "News",
}


def fetch_signals(limit=50, layer=None, min_gap=None):
    """Fetch signals from the Sirius API."""
    params = {"limit": limit}
    if layer:
        params["layer"] = layer
    if min_gap is not None:
        params["min_gap"] = min_gap

    resp = requests.get(f"{BASE_URL}/signals", headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def format_table(signals):
    """Print signals as a formatted ASCII table."""
    if not signals:
        print("No signals found.")
        return

    # Column widths
    cols = [
        ("Layer", 8),
        ("Market", 40),
        ("Side", 6),
        ("Odds", 7),
        ("Gap", 7),
        ("Age", 10),
    ]

    # Header
    header = " | ".join(name.ljust(width) for name, width in cols)
    separator = "-+-".join("-" * width for _, width in cols)
    print(header)
    print(separator)

    for s in signals:
        layer = s.get("layer", "?")
        layer_label = LAYER_NAMES.get(layer, layer)
        market = s.get("market", s.get("question", "Unknown"))
        if len(market) > 40:
            market = market[:37] + "..."
        side = s.get("side", s.get("direction", "?"))
        odds = s.get("odds", s.get("price", 0))
        gap = s.get("gap", 0)

        # Format age from timestamp
        ts = s.get("timestamp", s.get("detected_at", ""))
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                age_sec = (datetime.now(dt.tzinfo) - dt).total_seconds()
                if age_sec < 60:
                    age = f"{int(age_sec)}s ago"
                elif age_sec < 3600:
                    age = f"{int(age_sec / 60)}m ago"
                else:
                    age = f"{age_sec / 3600:.1f}h ago"
            except (ValueError, TypeError):
                age = ts[:10]
        else:
            age = "-"

        row = (
            f"{layer_label:<8} | "
            f"{market:<40} | "
            f"{str(side):<6} | "
            f"{odds:>6.1%} | "
            f"{gap:>6.1%} | "
            f"{age:<10}"
        )
        print(row)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch trading signals from Sirius Prediction Market API"
    )
    parser.add_argument(
        "--layer",
        choices=["L1", "L3", "L4", "L5", "L6"],
        help="Filter by signal layer",
    )
    parser.add_argument(
        "--min-gap",
        type=float,
        help="Minimum gap threshold (e.g. 0.05 for 5%%)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Max number of signals to fetch (default: 50)",
    )
    args = parser.parse_args()

    if API_KEY == "YOUR_RAPIDAPI_KEY":
        print("ERROR: Replace YOUR_RAPIDAPI_KEY with your actual key.")
        print("Get one at: https://rapidapi.com/louismichalot/api/sirius-prediction-market-api")
        sys.exit(1)

    print(f"Fetching signals (layer={args.layer or 'all'}, min_gap={args.min_gap or 'any'})...\n")

    data = fetch_signals(limit=args.limit, layer=args.layer, min_gap=args.min_gap)

    # The response may be a dict with a "signals" key or a list directly
    signals = data if isinstance(data, list) else data.get("signals", data.get("data", []))

    print(f"Found {len(signals)} signal(s):\n")
    format_table(signals)


if __name__ == "__main__":
    main()
