import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url):
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan requests terhadap {url}: {e}")
        return None

def extract_product_data(card):

    details = card.find('div', class_='product-details')
    if not details:
        return None

    title_element = details.find('h3', class_='product-title')
    title = title_element.text.strip() if title_element else None

    price_container = details.find('div', class_='price-container')
    price = price_container.text.strip() if price_container else None

    p_tags = details.find_all('p')
    rating, colors, size, gender = None, None, None, None

    for p in p_tags:
        text = p.text.strip()
        if text.startswith("Rating:"):
            rating = text
        elif text.endswith("Colors") or text.endswith("Colors:"):
            colors = text
        elif text.startswith("Size:"):
            size = text
        elif text.startswith("Gender:"):
            gender = text
            
    timestamp = datetime.now().isoformat()

    product = {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "timestamp": timestamp
    }
    return product

def scrape_products(delay=1):

    BASE_URL = "https://fashion-studio.dicoding.dev/?page={}"
    data = []
    
    for page_number in range(1, 51):
        url = BASE_URL.format(page_number)
        print(f"Scraping halaman: {url}")

        try:
            content = fetching_content(url)
            if content:
                soup = BeautifulSoup(content, "html.parser")
                product_cards = soup.find_all('div', class_='collection-card')
                
                if not product_cards:
                    print(f"Tidak menemukan produk di halaman {page_number}. Mungkin halaman terakhir.")
                    break 

                for card in product_cards:
                    product = extract_product_data(card)
                    if product:
                        data.append(product)
                
                time.sleep(delay) 
            else:
                print(f"Gagal mengambil konten dari halaman {page_number}. Melanjutkan...")
                continue

        except Exception as e:
            print(f"An error occurred during scraping on page {page_number}: {e}")
            continue 

    return data