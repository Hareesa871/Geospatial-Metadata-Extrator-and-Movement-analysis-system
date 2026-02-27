import requests
from bs4 import BeautifulSoup
import os


def scrape_images(url, save_folder="images"):
    os.makedirs(save_folder, exist_ok=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    images = soup.find_all("img")

    for index, img in enumerate(images[:5]):
        img_url = img.get("src")

        if img_url and img_url.startswith("http"):
            try:
                img_data = requests.get(img_url).content
                with open(f"{save_folder}/scraped_{index}.jpg", "wb") as f:
                    f.write(img_data)
                print(f"Downloaded scraped_{index}.jpg")
            except:
                continue