#!/usr/bin/env python3
"""
Screenshot & PDF API — Capture a URL and save to file

Takes a screenshot of any URL and saves it as PNG, JPEG, or WebP.
Supports full-page capture, custom viewport, delay for JS rendering,
and CSS selector targeting.

Usage:
  python screenshot.py https://github.com
  python screenshot.py https://news.ycombinator.com -o news.jpg --format jpeg --quality 90
  python screenshot.py https://en.wikipedia.org --full-page
  python screenshot.py https://example.com --delay 3 --width 1920 --height 1080

Requirements:
  pip install requests
"""

import argparse
import os
import sys

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
API_KEY = "YOUR_RAPIDAPI_KEY"
API_HOST = "screenshot-pdf-api.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}/v1"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST,
}

FORMAT_EXTENSIONS = {"png": ".png", "jpeg": ".jpg", "webp": ".webp"}


def take_screenshot(url, width=1280, height=800, fmt="png", quality=85,
                    full_page=False, delay=0, selector=None):
    """Capture a screenshot via the API and return raw image bytes."""
    params = {
        "url": url,
        "width": width,
        "height": height,
        "format": fmt,
    }
    if fmt in ("jpeg", "webp"):
        params["quality"] = quality
    if full_page:
        params["full_page"] = "true"
    if delay > 0:
        params["delay"] = delay
    if selector:
        params["selector"] = selector

    resp = requests.get(f"{BASE_URL}/screenshot", headers=HEADERS, params=params)
    resp.raise_for_status()

    content_type = resp.headers.get("Content-Type", "")
    if "image" not in content_type and "application/octet" not in content_type:
        # API returned JSON error
        print(f"API error: {resp.text}")
        sys.exit(1)

    return resp.content


def default_filename(url, fmt):
    """Generate a sensible filename from the URL."""
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace(".", "_").replace(":", "_")
    ext = FORMAT_EXTENSIONS.get(fmt, f".{fmt}")
    return f"screenshot_{domain}{ext}"


def main():
    parser = argparse.ArgumentParser(
        description="Take a screenshot of a URL using Screenshot & PDF API"
    )
    parser.add_argument("url", help="URL to capture")
    parser.add_argument("-o", "--output", help="Output filename (auto-generated if omitted)")
    parser.add_argument("--format", choices=["png", "jpeg", "webp"], default="png", help="Image format")
    parser.add_argument("--quality", type=int, default=85, help="JPEG/WebP quality (1-100)")
    parser.add_argument("--width", type=int, default=1280, help="Viewport width in pixels")
    parser.add_argument("--height", type=int, default=800, help="Viewport height in pixels")
    parser.add_argument("--full-page", action="store_true", help="Capture the full scrollable page")
    parser.add_argument("--delay", type=int, default=0, help="Wait N seconds before capture (0-5)")
    parser.add_argument("--selector", help="CSS selector to capture a specific element")
    args = parser.parse_args()

    if API_KEY == "YOUR_RAPIDAPI_KEY":
        print("ERROR: Replace YOUR_RAPIDAPI_KEY with your actual key.")
        print("Get one at: https://rapidapi.com/louismichalot/api/screenshot-pdf-api")
        sys.exit(1)

    output = args.output or default_filename(args.url, args.format)

    print(f"Capturing {args.url} ...")
    print(f"  Format: {args.format} | Viewport: {args.width}x{args.height} | Full page: {args.full_page}")

    image_data = take_screenshot(
        url=args.url,
        width=args.width,
        height=args.height,
        fmt=args.format,
        quality=args.quality,
        full_page=args.full_page,
        delay=args.delay,
        selector=args.selector,
    )

    with open(output, "wb") as f:
        f.write(image_data)

    size_kb = len(image_data) / 1024
    print(f"Saved to {output} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
