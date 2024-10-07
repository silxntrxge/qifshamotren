import sys
import site
import itertools
import random
import os
import json
import time
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

def get_emails(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@gmail\.com'
    return re.findall(email_pattern, text)

def save_emails(emails, output_file='emails.txt'):
    print(f"Saving {len(emails)} emails to {output_file}...")
    try:
        with open(output_file, 'w') as f:
            for email in emails:
                f.write(email + '\n')
        print("Emails saved successfully.")
    except Exception as e:
        print(f"Error saving emails: {e}")

def send_to_webhook(emails, webhook_url):
    print(f"Sending {len(emails)} emails to webhook: {webhook_url}")
    try:
        response = requests.post(webhook_url, json={'emails': emails})
        response.raise_for_status()
        print("Emails sent to webhook successfully.")
    except Exception as e:
        print(f"Error sending emails to webhook: {e}")

def initialize_driver():
    print("Initializing Selenium WebDriver...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = "/opt/chrome-linux64/chrome"
        
        service = Service(executable_path="/opt/chrome-linux64/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("WebDriver initialized successfully.")
        return driver
    except Exception as e:
        print(f"Error initializing WebDriver: {e}")
        sys.exit(1)

def generate_urls(names, domain, niches, num_pages=5):
    print("Generating URLs...")
    urls = []
    for name in names:
        for niche in niches:
            for page in range(1, num_pages + 1):
                url = f"https://www.google.com/search?q=%22{name}%22+%22{domain}%22+%22{niche}%22&start={page}"
                urls.append(url)
    print(f"Generated {len(urls)} URLs.")
    return urls

def scrape_emails_from_url(driver, url):
    print(f"Scraping emails from URL: {url}")
    driver.get(url)
    time.sleep(2)  # Wait for the page to load
    page_source = driver.page_source
    emails = get_emails(page_source)
    print(f"Found {len(emails)} emails on this page.")
    return set(emails)

def scrape_emails(names, domain, niches, webhook_url=None):
    print("Starting the scraper...")
    names = [name.strip() for name in names.split(',') if name.strip()]
    niches = [niche.strip() for niche in niches.split(',') if niche.strip()]
    
    driver = initialize_driver()
    
    urls = generate_urls(names, domain, niches)
    all_emails = set()

    for url in urls:
        try:
            emails = scrape_emails_from_url(driver, url)
            all_emails.update(emails)
        except Exception as e:
            print(f"Error scraping URL {url}: {e}")
    
    driver.quit()
    print("WebDriver closed.")
    
    email_list = list(all_emails)
    save_emails(email_list)
    
    if webhook_url:
        send_to_webhook(email_list, webhook_url)
    
    print(f"Scraper finished successfully. Total emails collected: {len(email_list)}")
    return email_list

if __name__ == "__main__":
    # This block will not be executed when imported as a module
    pass