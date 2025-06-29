import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def fetch(url):
    driver = get_driver()
    try:
        driver.get(url)
        # Простая проверка на Cloudflare, можно усложнить
        if "Checking your browser" in driver.title:
            time.sleep(5) # Ждем прохождения проверки
        
        return driver.page_source, driver.current_url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None
    finally:
        driver.quit()