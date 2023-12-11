import requests

home = requests.get("http://127.0.0.1:8000/")

print(home.json())


base = requests.get("http://127.0.0.1:8000/Deck")

print(base.json())

url = "http://127.0.0.1:8000/Deck"
decklist = "hi"  # Your single-line string

payload = {"decklist": decklist}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=decklist, headers=headers)
print(response.json())