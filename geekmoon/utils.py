from bs4 import BeautifulSoup

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
    return element.text.strip() if element else None

def get_location(html_content, selector):
    if not selector:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
    element = soup.select_one(selector)
    return element.text.strip() if element else None