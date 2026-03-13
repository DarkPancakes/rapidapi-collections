#!/usr/bin/env python3
"""
Sirius Prediction Market API — Real-Time Market Monitor

Polls prediction markets every 60 seconds and alerts when any market's
odds change by more than a configurable threshold (default 5%).

Great for:
  - Detecting breaking news that moves prediction markets
  - Spotting sudden odds shifts before they stabilize
  - Building automated trading signals on top of the API

Usage:
  python market_monitor.py                    # default 5% threshold, 60s interval
  python market_monitor.py --threshold 0.03   # alert on 3% moves
  python market_monitor.py --interval 30      # poll every 30 seconds

Requirements:
  pip install requests
"""

import argparse
import sys
import time
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


def fetch_markets():
    """Fetch all active prediction markets."""
    resp = requests.get(f"{BASE_URL}/markets", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    # Normalize: API may return list or dict with "markets" key
    markets = data if isinstance(data, list) else data.get("markets", data.get("data", []))
    return markets


def build_odds_map(markets):
    """Build a dict of market_id -> (question, odds) from the API response."""
    odds = {}
    for m in markets:
        mid = m.get("id", m.get("condition_id", m.get("question", "")))
        question = m.get("question", m.get("title", str(mid)))
        price = m.get("yes_price", m.get("odds", m.get("price", None)))
        if mid and price is not None:
            odds[mid] = (question, float(price))
    return odds


def detect_changes(prev, current, threshold):
    """Compare two odds snapshots and return significant changes."""
    alerts = []
    for mid, (question, new_odds) in current.items():
        if mid in prev:
            _, old_odds = prev[mid]
            delta = new_odds - old_odds
            if abs(delta) >= threshold:
                direction = "UP" if delta > 0 else "DOWN"
                alerts.append({
                    "question": question,
                    "old_odds": old_odds,
                    "new_odds": new_odds,
                    "delta": delta,
                    "direction": direction,
                })
    return alerts


def print_alert(alert):
    """Print a formatted alert for an odds movement."""
    arrow = "^" if alert["direction"] == "UP" else "v"
    color_start = "\033[92m" if alert["direction"] == "UP" else "\033[91m"
    color_end = "\033[0m"

    print(
        f"  {color_start}{arrow} {alert['direction']:>4}{color_end} "
        f"{alert['old_odds']:>6.1%} -> {alert['new_odds']:>6.1%} "
        f"({alert['delta']:+.1%})  "
        f"{alert['question'][:60]}"
    )


def monitor(threshold, interval):
    """Main monitoring loop."""
    print(f"Market Monitor started")
    print(f"  Threshold: {threshold:.0%} | Poll interval: {interval}s")
    print(f"  Press Ctrl+C to stop\n")

    # Initial snapshot
    print("Taking initial snapshot...")
    markets = fetch_markets()
    prev_odds = build_odds_map(markets)
    print(f"Tracking {len(prev_odds)} markets.\n")

    poll_count = 0
    total_alerts = 0

    try:
        while True:
            time.sleep(interval)
            poll_count += 1
            now = datetime.now().strftime("%H:%M:%S")

            try:
                markets = fetch_markets()
                current_odds = build_odds_map(markets)
            except requests.RequestException as e:
                print(f"[{now}] Poll #{poll_count} - API error: {e}")
                continue

            alerts = detect_changes(prev_odds, current_odds, threshold)

            if alerts:
                total_alerts += len(alerts)
                print(f"[{now}] Poll #{poll_count} - {len(alerts)} ALERT(s):")
                for a in sorted(alerts, key=lambda x: abs(x["delta"]), reverse=True):
                    print_alert(a)
                print()
            else:
                print(f"[{now}] Poll #{poll_count} - No significant changes ({len(current_odds)} markets)")

            # Update snapshot for next comparison
            prev_odds = current_odds

    except KeyboardInterrupt:
        print(f"\nStopped. {poll_count} polls, {total_alerts} total alerts.")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor prediction markets for odds changes"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.05,
        help="Minimum odds change to trigger alert (default: 0.05 = 5%%)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Polling interval in seconds (default: 60)",
    )
    args = parser.parse_args()

    if API_KEY == "YOUR_RAPIDAPI_KEY":
        print("ERROR: Replace YOUR_RAPIDAPI_KEY with your actual key.")
        print("Get one at: https://rapidapi.com/louismichalot/api/sirius-prediction-market-api")
        sys.exit(1)

    monitor(threshold=args.threshold, interval=args.interval)


if __name__ == "__main__":
    main()
