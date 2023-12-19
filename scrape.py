from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import tkinter as tk

# Function to handle window close event
def on_close():
    root.destroy()

# Setup webdriver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Get webpage
driver.get('https://limitlesstcg.com/tools/imggen')

# Prompt user to input the decklist
root = tk.Tk()
root.withdraw()  # Hide the main window

decklist = """
Pokémon (16)
3 Chien-Pao ex PAL 61
2 Frigibax PAL 57
1 Frigibax PAL 58
2 Bidoof CRZ 111
2 Bibarel BRS 121
2 Baxcalibur PAL 60
1 Radiant Greninja ASR 46
1 Manaphy BRS 41
1 Iron Hands ex PAR 70
1 Iron Bundle PAR 56

Trainer (35)
4 Irida ASR 147
1 Iono PAL 185
4 Battle VIP Pass FST 225
4 Nest Ball SVI 181
4 Ultra Ball SVI 196
4 Superior Energy Retrieval PAL 189
3 Rare Candy SVI 191
3 Super Rod PAL 188
2 Earthen Vessel PAR 163
1 Hisuian Heavy Ball ASR 146
1 Counter Catcher PAR 160
4 PokéStop PGO 68

Energy (9)
8 Water Energy 3
1 Lightning Energy 4
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

#Make the card images larger
cards_urls = [url.replace('XS.png', 'LG.png') for url in cards_urls]

# Close the browser
driver.quit()

# Create a custom Toplevel window with a wider Text widget for editable text
output_window = tk.Toplevel(root)
output_window.title("Card URLs")

text_widget = tk.Text(output_window, wrap="none", height=10, width=85)  # Adjust width here
text_widget.insert("1.0", "\n".join(cards_urls))
text_widget.pack()

# Make the text widget read-only
text_widget.configure(state="disabled")

# Allow selecting and copying text
text_widget.bind("<Button-1>", lambda event: text_widget.tag_add(tk.SEL, "1.0", tk.END))
text_widget.bind("<Control-c>", lambda event: root.clipboard_clear() or root.clipboard_append(text_widget.selection_get()))

# Bind window close event to on_close function
output_window.protocol("WM_DELETE_WINDOW", on_close)

# Print URLs from cards_urls instead of image_urls
for url in cards_urls:
    print(url)

# Run the Tkinter main loop
root.mainloop()