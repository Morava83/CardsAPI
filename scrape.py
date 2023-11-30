from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import tkinter as tk
from tkinter import simpledialog

# Setup webdriver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Get webpage
driver.get('https://limitlesstcg.com/tools/imggen')

# Prompt user to input the decklist
root = tk.Tk()
root.withdraw()  # Hide the main window

decklist = simpledialog.askstring("Input", "Paste your decklist here:")

# Locate and interact with the text area using the name attribute
text_area = driver.find_element(By.NAME, 'input')
text_area.clear()

# Input the decklist
text_area.send_keys(decklist)

# Locate and click the "Submit" button
submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Submit']")
submit_button.click()

# Wait for a moment to ensure the submission is processed
time.sleep(2)

# Get all images
images = driver.find_elements(By.TAG_NAME, 'img')

# Extract URLs
image_urls = [img.get_attribute('src') for img in images]

# Create a subset of image_urls (cards_urls) with "XS.png" in their name
cards_urls = [url for url in image_urls if 'XS.png' in url]

# Print URLs from cards_urls instead of image_urls
for url in cards_urls:
    print(url)

# Close the browser
driver.quit()
