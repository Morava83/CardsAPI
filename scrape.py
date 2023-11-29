from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Setup webdriver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Get webpage
driver.get('https://limitlesstcg.com/tools/imggen')

# Locate and interact with the text area using the name attribute
text_area = driver.find_element(By.NAME, 'input')
text_area.clear()

# Input the decklist
decklist = """
Pokémon (17.6)
3.38 Ralts ASR 60
3.00 Kirlia SIT 68

Trainer (30.41)
3.90 Level Ball BST 129
3.62 Iono PAL 185

Energy (12)
9.97 Psychic Energy 5
2.03 Reversal Energy PAL 192
"""

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

# Print URLs
for url in image_urls:
    print(url)

# Close the browser
driver.quit()
