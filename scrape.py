from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Setup webdriver
webdriver_service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(service=webdriver_service, options=options)

# Get webpage
driver.get('https://limitlesstcg.com/tools/imggen')

decklist = """
3 Roaring Moon ex PAR 124
1 Squawkabilly ex PAL 169
1 Galarian Moltres V CRE 97
1 Brute Bonnet PAR 123
1 Radiant Greninja ASR 46
1 Morpeko PAR 121
1 Lumineon V BRS 40

4 Professor Sada's Vitality PAR 170
1 Iono PAL 185
1 Boss's Orders PAL 172
4 Battle VIP Pass FST 225
4 Dark Patch ASR 139
4 Cross Switcher FST 230
4 Earthen Vessel PAR 163
4 Energy Switch SVI 173
3 Ultra Ball SVI 196
2 Switch Cart ASR 154
1 Hisuian Heavy Ball ASR 146
1 Super Rod PAL 188
1 Pal Pad SVI 182
1 Canceling Cologne ASR 136
2 Ancient Booster Energy Capsule PAR 159
3 PokéStop PGO 68
1 Collapsed Stadium BRS 137

7 Darkness Energy 7
3 Water Energy 3
""" 

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

# Make the card images larger
cards_urls = [url.replace('XS.png', 'LG.png') for url in cards_urls]

# Close the browser
driver.quit()

# Print URLs from cards_urls instead of image_urls
for url in cards_urls:
    print(url)
