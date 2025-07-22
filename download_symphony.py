
import requests

url = "https://www.mfiles.co.uk/scores/beethoven-symphony5-1.mid"
response = requests.get(url)

if response.status_code == 200:
    with open("beethoven_symphony_5.mid", "wb") as f:
        f.write(response.content)
    print("Successfully downloaded and saved beethoven_symphony_5.mid")
else:
    print(f"Failed to download the file. Status code: {response.status_code}")
