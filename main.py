from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from fastapi import Body, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import time

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific requirements in a production environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"PokemonCardsAPI": "Welcome!"}

@app.get('/deck')
async def deckListBase():
    return {"Enter decklist as a query string"}

@app.post('/deck')
async def getDeckList(decklist: Optional[str] = Body(None)):

    # Setup webdriver
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service)

    # Get webpage
    driver.get('https://limitlesstcg.com/tools/imggen')
    
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

    #Make the card images larger
    cards_urls = [url.replace('XS.png', 'LG.png') for url in cards_urls]

    # Close the browser
    driver.quit()

    return {"image_urls": cards_urls}

