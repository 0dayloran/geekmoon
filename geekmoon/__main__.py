import argparse
import json
import os
import asyncio
from .requester import fetch, get_browser
from .utils import (
    check_redirect, get_activity, get_location, 
    save_to_txt, save_to_md, save_to_json, save_to_csv, 
    analyze_profile, get_exif_data
)

def generate_mutations(username):
    return list(set([
        username,
        f"{username}_",
        f"_{username}",
        f"{username}123",
        username.replace(".", ""),
        username.replace("_", "")
    ]))

async def search_site(site_name, site_data, username, browser):
    url = site_data["url"].format(username=username)
    html_content, final_url = await fetch(url, browser)

    if html_content and check_redirect(html_content, site_data.get("error_keywords", [])):
        activity = get_activity(html_content, site_data.get("activity_selector"))
        location = get_location(html_content, site_data.get("location_selector"))
        tags = analyze_profile(html_content)
        exif = get_exif_data(html_content, final_url)
        
        result_data = {
            "username": username,
            "site": site_name,
            "url": final_url,
            "activity": activity,
            "location": location,
            "tags": tags,
            "exif": exif
        }
        
        result_str = f"[+] ({username}) {site_name}: {final_url}"
        if activity: result_str += f" (Activity: {activity})"
        if location: result_str += f" (Location: {location})"
        if tags: result_str += f" (Tags: {', '.join(tags)})"
        if exif: result_str += f" (EXIF data found!)"
        print(result_str)
        
        return result_data
    return None

def get_site_categories(sites):
    categories = {"all": list(sites.keys())}
    for name, data in sites.items():
        cat = data.get("category", "other")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(name)
    return categories

async def async_main():
    print("--- GEEKMOON ---")
    print("For legal use only.")
    print("-" * 16)

    parser = argparse.ArgumentParser(description="Geekmoon - The Next-Gen OSINT Tool.")
    parser.add_argument("username", help="Username to search for.")
    parser.add_argument("--output-txt", help="Path to save results in a TXT file.")
    parser.add_argument("--output-md", help="Path to save results in a Markdown file.")
    parser.add_argument("--output-json", help="Path to save results in a JSON file.")
    parser.add_argument("--output-csv", help="Path to save results in a CSV file.")
    parser.add_argument("--recursive", action="store_true", help="Perform recursive search with username mutations.")
    parser.add_argument("--interactive", action="store_true", help="Choose site categories to scan.")
    args = parser.parse_args()

    package_dir = os.path.dirname(__file__)
    sites_path = os.path.join(package_dir, 'sites.json')
    with open(sites_path, "r") as f:
        all_sites = json.load(f)

    sites_to_scan = all_sites
    if args.interactive:
        categories = get_site_categories(all_sites)
        print("\nAvailable categories:")
        for i, cat in enumerate(categories.keys()):
            print(f"  {i}. {cat}")
        
        choices = input("Enter category numbers to scan (e.g., '0 2 3'): ")
        selected_indices = [int(c.strip()) for c in choices.split()]
        
        selected_sites = {}
        for i in selected_indices:
            cat_name = list(categories.keys())[i]
            for site_name in categories[cat_name]:
                selected_sites[site_name] = all_sites[site_name]
        sites_to_scan = selected_sites

    usernames_to_scan = [args.username]
    if args.recursive:
        usernames_to_scan.extend(generate_mutations(args.username))
        usernames_to_scan = list(set(usernames_to_scan))
        print(f"\nRecursive mode on. Scanning for: {', '.join(usernames_to_scan)}")

    browser = await get_browser()
    tasks = []
    for username in usernames_to_scan:
        for name, data in sites_to_scan.items():
            tasks.append(search_site(name, data, username, browser))
    
    results = await asyncio.gather(*tasks)
    await browser.close()

    found_results = [res for res in results if res]

    if args.output_txt: save_to_txt(found_results, args.output_txt)
    if args.output_md: save_to_md(found_results, args.output_md)
    if args.output_json: save_to_json(found_results, args.output_json)
    if args.output_csv: save_to_csv(found_results, args.output_csv)

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()