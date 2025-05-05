import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_fashion_data(article):
    """Mengambil data fashion dari elemen artikel."""
    try:
        title_tag = article.find('h3', class_='product-title')
        price_tag = article.find('span', class_='price')
        
        title = title_tag.text.strip() if title_tag else "No Title"
        price = price_tag.text.strip() if price_tag else "No Price"

        rating_tag = article.find('p', string=lambda t: t and "Rating:" in t)
        rating_raw = rating_tag.text.strip().replace("Rating:", "") if rating_tag else "Not Rated"
        match = re.search(r"[\d.]+", rating_raw)
        rating = match.group(0) if match else "Not Rated"

        colors_tag = article.find('p', string=lambda t: t and "Colors" in t)
        colors = colors_tag.text.strip().split(" ")[0] if colors_tag else "Unknown"

        size_tag = article.find('p', string=lambda t: t and "Size:" in t)
        size = size_tag.text.strip().split(":")[1].strip() if size_tag and "Size:" in size_tag.text else "Unknown"

        gender_tag = article.find('p', string=lambda t: t and "Gender:" in t)
        gender = gender_tag.text.strip().split(":")[1].strip() if gender_tag and "Gender:" in gender_tag.text else "Unknown"

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender
        }
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None


def scrape_fashion(base_url):
    """Mengambil data fashion dari beberapa halaman."""
    data = []
    page_number = 1

    while True:
        # Tentukan URL untuk halaman pertama atau halaman berikutnya
        url = base_url if page_number == 1 else f"{base_url}page{page_number}"
        print(f"Scraping halaman: {url}")

        content = fetching_content(url)
        if content:
            soup = BeautifulSoup(content, "html.parser")
            articles = soup.find_all('div', class_='collection-card')
            for article in articles:
                fashion_data = extract_fashion_data(article)
                if fashion_data:
                    data.append(fashion_data)

            # Cek apakah ada tombol "Next" untuk melanjutkan ke halaman berikutnya
            next_button = soup.find('li', class_='next')
            if next_button and not next_button.get('class', [''])[0] == 'disabled':
                page_number += 1
            else:
                break  # Berhenti jika tidak ada tombol "Next"
        else:
            break  # Berhenti jika ada kesalahan

    return data

def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = 'https://example.com/page{}'
    all_fashion_data = scrape_fashion(BASE_URL)
    df = pd.DataFrame(all_fashion_data)
    print(df)
    df.to_csv('fashion_data.csv', index=False)

if __name__ == '__main__':
    main()