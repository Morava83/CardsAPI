import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import Body, FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def wait_for_element(driver, by, value, timeout=100):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def wait_for_clickable(driver, by, value, timeout=100):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

@app.get("/")
async def root():
    return {"PokemonCardsAPI": "Welcome!"}

@app.post("/backgroundDemo")
async def getDeckList(decklist: Optional[str] = Body(None)):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
    
    try:
        # Get webpage
        driver.get('https://limitlesstcg.com/tools/imggen')

        # Locate and interact with the text area using the name attribute
        text_area = wait_for_element(driver, By.NAME, 'input')
        text_area.clear()

        # Input the decklist
        text_area.send_keys(decklist)

        # Wait for the "Submit" button to be clickable
        submit_button = wait_for_clickable(driver, By.XPATH, "//button[@type='submit' and text()='Submit']")
        
        # Scroll into view if needed
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)

        # Click the "Submit" button
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

        return {"image_urls": cards_urls}

    finally:
        # Ensure that the driver is always closed, even in case of an exception
        driver.quit()
