import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup

# Path to the Chrome executable for the desired version
chrome_path = r"C:\Users\jscam\OneDrive\Documents\Programming\Chrome_driver\chrome-win64\chrome-win64\chrome.exe"

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_path

# Set up the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Navigate to Google Search
search_keyword = "adidas"
driver.get("https://www.google.com/search?q=" + search_keyword)

# Define the number of times to scroll
scroll_count = 5

# Simulate continuous scrolling using JavaScript
for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the new results to load

page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

search_results = soup.find_all('div', class_='tF2Cxc')
for result in search_results:
    title = result.h3.text
    link = result.a['href']
    print(f"Title: {title}")
    print(f"Link: {link}")
    print("\n")

# Close the webdriver
driver.quit()
