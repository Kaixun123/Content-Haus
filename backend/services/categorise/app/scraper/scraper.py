# scraper/scraper.py
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
from dotenv import load_dotenv

load_dotenv()

def setup_webdriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Read ChromeDriver path from environment variable
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH')
    if not chromedriver_path:
        raise EnvironmentError("CHROMEDRIVER_PATH environment variable not set")
    
    if not os.path.isfile(chromedriver_path):
        raise ValueError(f"The path is not a valid file: {chromedriver_path}")
    
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def search_tiktok(driver, keyword):
    base_url = "https://www.tiktok.com"
    search_url = f"{base_url}/search?q={keyword}"
    driver.get(search_url)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tiktok-1w1pypo-DivItemContainer'))
        )
    except Exception as e:
        print("Error waiting for search results to load:", e)
    
    return driver.page_source

def extract_video_metadata(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    videos = []
    
    for video in soup.find_all('div', class_='tiktok-1w1pypo-DivItemContainer'):
        title = video.find('h3').get_text() if video.find('h3') else 'N/A'
        description = video.find('p').get_text() if video.find('p') else 'N/A'
        hashtags = [tag.get_text() for tag in video.find_all('a', class_='tiktok-yz6ijl-AStyledLink')]
        
        videos.append({
            'title': title,
            'description': description,
            'hashtags': hashtags
        })
    
    return videos

def store_data(videos, filename):
    with open(filename, 'w') as file:
        json.dump(videos, file, indent=4)
