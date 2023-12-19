from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fastapi import Body, FastAPI
from typing import Optional

app = FastAPI()

@app.get('/')
async def root():
    return {"PokemonCardsAPI": "Welcome!"}

@app.get('/Deck')
async def deckListBase():
    return {"Enter decklist as a query string"}


@app.post('/Deck')
async def getDeckList(decklist: Optional[str] = Body(None)):

    #Load less of Browser GUI
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Setup webdriver
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    
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

    return {"image urls": cards_urls}
