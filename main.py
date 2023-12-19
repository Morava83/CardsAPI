# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from fastapi import Body, FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from typing import Optional

# app = FastAPI()

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this to your specific requirements in a production environment
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get('/')
# async def root():
#     return {"PokemonCardsAPI": "Welcome!"}

# @app.get('/deck')
# async def deckListBase():
#     return {"Enter decklist as a query string"}

# @app.post('/deck')
# async def getDeckList(decklist: Optional[str] = Body(None)):

#     # Load less of Browser GUI
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument('--disable-web-security')
#     chrome_options.add_argument('--allow-running-insecure-content')

#     # Setup webdriver
#     webdriver_service = Service(ChromeDriverManager().install())
#     driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

#     try:
#         # Get webpage
#         driver.get('https://limitlesstcg.com/tools/imggen')

#         # Locate and interact with the text area using the name attribute
#         text_area = driver.find_element(By.NAME, 'input')
#         text_area.clear()

#         # Input the decklist
#         text_area.send_keys(decklist)

#         # Locate and click the "Submit" button
#         submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Submit']")
#         submit_button.click()

#         # Get all images
#         images = driver.find_elements(By.TAG_NAME, 'img')

#         # Extract URLs
#         image_urls = [img.get_attribute('src') for img in images]

#         # Create a subset of image_urls (cards_urls) with "XS.png" in their name
#         cards_urls = [url for url in image_urls if 'XS.png' in url]

#         # Make the card images larger
#         cards_urls = [url.replace('XS.png', 'LG.png') for url in cards_urls]

#         return {"image_urls": cards_urls}

#     finally:
#         # Close the browser
#         driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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

def create_webdriver():
    # Create and return a new WebDriver instance
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    webdriver_service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=webdriver_service, options=chrome_options)

def close_webdriver(driver):
    # Close the WebDriver instance, handling potential exceptions
    try:
        driver.quit()
    except Exception as e:
        print(f"Error while closing WebDriver: {e}")

@app.get('/')
async def root():
    return {"PokemonCardsAPI": "Welcome!"}

@app.get('/deck')
async def deckListBase():
    return {"Enter decklist as a query string"}

@app.post('/deck')
async def getDeckList(decklist: Optional[str] = Body(None)):

    retries = 3  # Number of times to retry the entire process
    retry_delay = 2  # Seconds to wait between retries
    driver = None

    for attempt in range(1, retries + 1):
        try:
            # Create WebDriver
            driver = create_webdriver()

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

            # Make the card images larger
            cards_urls = [url.replace('XS.png', 'LG.png') for url in cards_urls]

            return {"image_urls": cards_urls}

        except Exception as e:
            print(f"Error in attempt {attempt}: {e}")
            time.sleep(retry_delay)
        finally:
            # Close the browser on success or exception
            close_webdriver(driver)

    # If all attempts fail, raise an HTTPException
    raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
