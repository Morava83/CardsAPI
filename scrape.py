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
Pokémon (12)
4 Comfey LOR 79
1 Sableye LOR 70
1 Cramorant LOR 50
1 Radiant Greninja ASR 46
1 Kyogre CEL 3
1 Roaring Moon ex PAR 124
1 Iron Hands ex PAR 70
1 Origin Forme Palkia V ASR 39
1 Origin Forme Palkia VSTAR ASR 40

Trainer (36)
4 Colress's Experiment LOR 155
4 Mirage Gate LOR 163
4 Battle VIP Pass FST 225
4 Nest Ball SVI 181
4 Switch Cart ASR 154
4 Escape Rope BST 125
3 Pokégear 3.0 SVI 186
3 Super Rod PAL 188
2 Energy Recycler BST 124
1 Hisuian Heavy Ball ASR 146
1 Pal Pad SVI 182
2 PokéStop PGO 68

Energy (12)
4 Water Energy 3
4 Darkness Energy 7
2 Psychic Energy 5
2 Lightning Energy 4
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

# Create a subset of image_urls (cards_urls) with "XS.png" in their name
cards_urls = [url for url in image_urls if 'XS.png' in url]

# Print URLs from cards_urls instead of image_urls
for url in cards_urls:
    print(url)

# Close the browser
driver.quit()
