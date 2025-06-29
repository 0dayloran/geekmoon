# Geekmoon

Geekmoon is a powerful OSINT tool for searching usernames across a vast number of social networks and websites. It's inspired by Sherlock and designed for both English and Russian-speaking environments.

## Features

- **Extensive Site Support:** Searches over 150+ websites (currently configured with a subset, easily expandable).
- **Anti-Bot Evasion:** Uses Selenium with a real browser (Chrome Headless) to bypass Cloudflare and other anti-DDoS protections.
- **Smart Verification:** Automatically checks for "Not Found" or "404" keywords in the page's HTML to reduce false positives.
- **User Activity:** Displays the user's last activity next to the found profile link.
- **Geolocation:** Shows the user's location if specified in their profile.

## Installation

You can install Geekmoon using pip:

```bash
pip install .
```

Or, if you want to install it from GitHub:

```bash
pip install git+https://github.com/yourusername/geekmoon.git
```

## Usage

To search for a username, simply run:

```bash
geekmoon <username>
```

Example:

```bash
geekmoon johnsmith
```

## Extending the Site List

You can easily add more websites to search by editing the `geekmoon/sites.json` file. Follow the existing format:

```json
{
  "Site Name": {
    "url": "https://sitename.com/{username}",
    "error_keywords": ["Keyword 1", "Keyword 2"],
    "activity_selector": "css.selector.for.activity",
    "location_selector": "css.selector.for.location"
  }
}
```

## License

This project is licensed under the MIT License.