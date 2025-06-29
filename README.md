# Geekmoon - The Next-Gen OSINT Tool

**Geekmoon** is a revolutionary OSINT tool for searching usernames across social networks and websites. It's built for speed, power, and deep analysis, leaving other tools behind.

**Created by:** [0dayloran on GitHub](https://github.com/0dayloran) | [0dayloran on Twitter](https://twitter.com/0dayloran)

---

## 🔥 Key Features That Crush the Competition

*   **Blazing-Fast Async Scans:** Geekmoon uses an asynchronous core to scan dozens of sites simultaneously. It's one of the fastest username checkers in the world.
*   **Massive Site Support:** Searches over 350+ websites, with a focus on both international and Russian-speaking communities.
*   **Smart Anti-Bot Evasion:** Uses a real browser engine (`pyppeteer`) to bypass Cloudflare, captchas, and other anti-bot protections that stop other tools.
*   **Recursive Search (Username Mutation):** If the primary username isn't found, Geekmoon can automatically generate and check variations (`user` -> `user_`, `user123`) to uncover hidden profiles. Use the `--recursive` flag.
*   **Profile Interest Analysis:** Geekmoon doesn't just find pages; it analyzes their content for keywords and tags the profile with potential interests like `infosec`, `crypto`, `gaming`, etc.
*   **Avatar EXIF Data Extraction:** The tool attempts to download profile pictures and extract hidden EXIF metadata, which can reveal GPS coordinates, camera models, and timestamps.
*   **Interactive Category Selection:** Don't want to scan all 350+ sites? Use the `--interactive` flag to choose specific categories to scan (e.g., `coding`, `social`, `russian`).
*   **Multiple Export Formats:** Save your results in human-readable or machine-readable formats.
    *   `--output-txt`: Plain text report.
    *   `--output-md`: Markdown report.
    *   `--output-json`: For integration with other tools.
    *   `--output-csv`: For spreadsheet analysis.

## Installation

```bash
# Make sure you have Google Chrome installed
# Then, install from GitHub:
pip install git+https://github.com/0dayloran/geekmoon.git
```

## Usage

**Basic Scan:**
```bash
geekmoon <username>
```

**Recursive Scan & Save to Markdown:**
```bash
geekmoon <username> --recursive --output-md <username>.md
```

**Interactive Scan for Gaming & Coding Sites:**
```bash
geekmoon <username> --interactive
# Then follow the prompts to select categories
```

## License

This project is licensed under the MIT License. For legal use only.