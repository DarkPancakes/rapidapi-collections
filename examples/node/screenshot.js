#!/usr/bin/env node
/**
 * Screenshot & PDF API — Capture a URL and save to file (Node.js)
 *
 * Takes a screenshot of any URL and saves it locally.
 * Supports PNG, JPEG, WebP, full-page capture, and custom viewports.
 *
 * Usage:
 *   node screenshot.js https://github.com
 *   node screenshot.js https://news.ycombinator.com --format jpeg --quality 90 -o news.jpg
 *   node screenshot.js https://en.wikipedia.org --full-page
 *   node screenshot.js https://example.com --delay 3 --width 1920 --height 1080
 *
 * Requirements: Node.js 18+ (native fetch + fs)
 */

import { writeFile } from "node:fs/promises";

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const API_KEY = "YOUR_RAPIDAPI_KEY";
const API_HOST = "screenshot-pdf-api.p.rapidapi.com";
const BASE_URL = `https://${API_HOST}/v1`;

const FORMAT_EXT = { png: ".png", jpeg: ".jpg", webp: ".webp" };

// ---------------------------------------------------------------------------
// CLI argument parsing
// ---------------------------------------------------------------------------
function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {
    url: null,
    output: null,
    format: "png",
    quality: 85,
    width: 1280,
    height: 800,
    fullPage: false,
    delay: 0,
    selector: null,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("http")) {
      opts.url = arg;
    } else
      switch (arg) {
        case "-o":
        case "--output":
          opts.output = args[++i];
          break;
        case "--format":
          opts.format = args[++i];
          break;
        case "--quality":
          opts.quality = parseInt(args[++i], 10);
          break;
        case "--width":
          opts.width = parseInt(args[++i], 10);
          break;
        case "--height":
          opts.height = parseInt(args[++i], 10);
          break;
        case "--full-page":
          opts.fullPage = true;
          break;
        case "--delay":
          opts.delay = parseInt(args[++i], 10);
          break;
        case "--selector":
          opts.selector = args[++i];
          break;
        case "--help":
          console.log(
            "Usage: node screenshot.js <url> [-o file] [--format png|jpeg|webp] [--quality 85] " +
              "[--width 1280] [--height 800] [--full-page] [--delay 2] [--selector '.main']"
          );
          process.exit(0);
      }
  }

  if (!opts.url) {
    console.error("Error: URL is required. Run with --help for usage.");
    process.exit(1);
  }

  return opts;
}

// ---------------------------------------------------------------------------
// API
// ---------------------------------------------------------------------------
async function takeScreenshot(opts) {
  const params = new URLSearchParams({
    url: opts.url,
    width: String(opts.width),
    height: String(opts.height),
    format: opts.format,
  });
  if (opts.format !== "png") params.set("quality", String(opts.quality));
  if (opts.fullPage) params.set("full_page", "true");
  if (opts.delay > 0) params.set("delay", String(opts.delay));
  if (opts.selector) params.set("selector", opts.selector);

  const resp = await fetch(`${BASE_URL}/screenshot?${params}`, {
    headers: {
      "X-RapidAPI-Key": API_KEY,
      "X-RapidAPI-Host": API_HOST,
    },
  });

  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`API returned ${resp.status}: ${body}`);
  }

  const contentType = resp.headers.get("content-type") || "";
  if (!contentType.includes("image") && !contentType.includes("octet")) {
    const body = await resp.text();
    throw new Error(`Unexpected response: ${body}`);
  }

  return Buffer.from(await resp.arrayBuffer());
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function main() {
  if (API_KEY === "YOUR_RAPIDAPI_KEY") {
    console.error("ERROR: Replace YOUR_RAPIDAPI_KEY with your actual key.");
    console.error("Get one at: https://rapidapi.com/louismichalot/api/screenshot-pdf-api");
    process.exit(1);
  }

  const opts = parseArgs();

  // Auto-generate filename if not provided
  const domain = new URL(opts.url).hostname.replace(/\./g, "_");
  const ext = FORMAT_EXT[opts.format] || `.${opts.format}`;
  const output = opts.output || `screenshot_${domain}${ext}`;

  console.log(`Capturing ${opts.url} ...`);
  console.log(`  Format: ${opts.format} | Viewport: ${opts.width}x${opts.height} | Full page: ${opts.fullPage}`);

  const imageData = await takeScreenshot(opts);
  await writeFile(output, imageData);

  const sizeKb = (imageData.length / 1024).toFixed(1);
  console.log(`Saved to ${output} (${sizeKb} KB)`);
}

main().catch((err) => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
