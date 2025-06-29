from bs4 import BeautifulSoup
import dateparser
import re

def save_to_txt(results, filename):
    with open(filename, "w") as f:
        for res in results:
            f.write(f"Site: {res['site']}\n")
            f.write(f"URL: {res['url']}\n")
            if res['activity']:
                f.write(f"Last Activity: {res['activity']}\n")
            if res['location']:
                f.write(f"Location: {res['location']}\n")
            f.write("-" * 20 + "\n")
    print(f"\nResults saved to {filename}")

def save_to_md(results, filename):
    with open(filename, "w") as f:
        f.write("# Geekmoon Scan Results\n\n")
        for res in results:
            f.write(f"## {res['site']}\n")
            f.write(f"- **URL:** [{res['url']}]({res['url']})\n")
            if res['activity']:
                f.write(f"- **Last Activity:** {res['activity']}\n")
            if res['location']:
                f.write(f"- **Location:** {res['location']}\n")
            f.write("\n")
    print(f"\nResults saved to {filename}")

def check_redirect(html_content, error_keywords):
    for keyword in error_keywords:
        if keyword.lower() in html_content.lower():
            return False
    return True

def get_activity(html_content, selector):
    if not selector:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.select_one(selector)
    if not element:
        return None

    text = element.text.strip()
    
    # Try to parse date with dateparser
    parsed_date = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'past'})
    if parsed_date:
        return parsed_date.strftime('%Y-%m-%d %H:%M:%S')

    # Fallback to regex for common patterns like "last seen 2 hours ago"
    match = re.search(r'(?i)(last seen|online|active) (.+)', text)
    if match:
        return match.group(2).strip()

    return text

def get_location(html_content, selector):
    if not selector:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.select_one(selector)
    return element.text.strip() if element else None
import json
import csv

def save_to_json(results, filename):
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")

def save_to_csv(results, filename):
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to {filename}")
INTEREST_KEYWORDS = {
    "infosec": ["infosec", "cybersecurity", "hacking", "pentest", "ctf"],
    "crypto": ["crypto", "bitcoin", "ethereum", "blockchain", "nft"],
    "development": ["python", "javascript", "developer", "coding", "software"],
    "gaming": ["gaming", "gamer", "esports", "twitch", "steam"],
    "design": ["design", "ui/ux", "photoshop", "illustrator", "figma"]
}

def analyze_profile(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text().lower()
    found_tags = set()
    for category, keywords in INTEREST_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                found_tags.add(category)
    return list(found_tags)
import exifread
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import urljoin

def get_exif_data(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find a potential avatar image (this is a heuristic)
    img_tag = soup.find("img", {"src": re.compile(r'avatar|profile|user', re.I)})
    if not img_tag:
        return None

    img_url = img_tag.get('src')
    if not img_url:
        return None

    # Make sure the URL is absolute
    img_url = urljoin(base_url, img_url)

    try:
        response = requests.get(img_url, stream=True, timeout=5)
        response.raise_for_status()
        
        image_data = BytesIO(response.content)
        tags = exifread.process_file(image_data)
        
        if not tags:
            return None

        exif_info = {}
        for tag, value in tags.items():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail'): # Exclude thumbnails
                exif_info[str(tag)] = str(value)
        
        return exif_info if exif_info else None

    except (requests.RequestException, IOError) as e:
        print(f"Could not process image {img_url}: {e}")
        return None