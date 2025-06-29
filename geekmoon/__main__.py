import argparse
import json
import os
from .requester import fetch
from .utils import check_redirect, get_activity, get_location

def main():
    parser = argparse.ArgumentParser(description="OSINT tool for searching usernames across social networks.")
    parser.add_argument("username", help="Username to search for.")
    args = parser.parse_args()
    username = args.username

    # Correctly locate sites.json within the package
    package_dir = os.path.dirname(__file__)
    sites_path = os.path.join(package_dir, 'sites.json')

    with open(sites_path, "r") as f:
        sites = json.load(f)

    for site_name, site_data in sites.items():
        url = site_data["url"].format(username=username)
        html_content, final_url = fetch(url)

        if html_content:
            if check_redirect(html_content, site_data.get("error_keywords", [])):
                activity = get_activity(html_content, site_data.get("activity_selector"))
                location = get_location(html_content, site_data.get("location_selector"))
                
                result = f"[+] {site_name}: {final_url}"
                if activity:
                    result += f" (Last Activity: {activity})"
                if location:
                    result += f" (Location: {location})"
                print(result)

if __name__ == "__main__":
    main()