import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import logging

# --- Configuration ---
# It's good practice to set up logging to see what's happening.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Flipkart can block requests without a user-agent. This mimics a real browser.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

# Base URL for Flipkart
FLIPKART_BASE_URL = "https://www.flipkart.com"

# --- CSS Selectors ---
# These selectors are crucial and might change if Flipkart updates its website.
# If the script breaks, updating these is the first thing to check.
SEARCH_RESULTS_CONTAINER = "div._75nlfW" # The container for each product on the search page
PRODUCT_LINK_TAG = "a" # The 'a' tag within the container that holds the product link

PRODUCT_NAME_SELECTOR = "span.VU-ZEz" # The selector for the product's main title/name
PRODUCT_PRICE_SELECTOR = "div.Nx9bqj.CxhGGd" # The selector for the product price

# Selectors for individual reviews on a product page
REVIEW_CONTAINER_SELECTOR = "div.cPHDOP" # The main container for a single review
REVIEW_RATING_SELECTOR = "div.XQDdHH" # The rating (e.g., '5', '4')
REVIEW_TITLE_SELECTOR = "p.z9E0Ig" # The short title of the review (e.g., 'Excellent')
REVIEW_CONTENT_SELECTOR = "div.ZmyHeo" # The full text content of the review


def get_product_links(product_query: str) -> list:
    """
    Searches for a product on Flipkart and returns a list of individual product page URLs.

    Args:
        product_query: The name of the product to search for (e.g., "Smart Speakers").

    Returns:
        A list of full URLs to the product pages found.
    """
    search_query = product_query.replace(" ", "")
    search_url = f"{FLIPKART_BASE_URL}/search?q={search_query}"
    logging.info(f"Fetching search results from: {search_url}")

    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        soup = bs(response.text, "html.parser")
        product_containers = soup.select(SEARCH_RESULTS_CONTAINER)
        
        if not product_containers:
            logging.warning("No product containers found. The CSS selector might be outdated.")
            return []

        links = []
        for container in product_containers:
            link_tag = container.select_one(PRODUCT_LINK_TAG)
            if link_tag and 'href' in link_tag.attrs:
                product_path = link_tag['href']
                full_url = FLIPKART_BASE_URL + product_path
                links.append(full_url)
        
        logging.info(f"Found {len(links)} product links.")
        return list(set(links)) # Return unique links

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch search page: {e}")
        return []


def scrape_product_page(product_url: str) -> list:
    """
    Scrapes a single product page for its name, price, and all its reviews.

    Args:
        product_url: The URL of the product page to scrape.

    Returns:
        A list of dictionaries, where each dictionary represents one review.
        Returns an empty list if the page cannot be scraped.
    """
    try:
        response = requests.get(product_url, headers=HEADERS)
        response.raise_for_status()
        soup = bs(response.text, "html.parser")

        # --- Extract Product-level information (same for all reviews on this page) ---
        product_name_element = soup.select_one(PRODUCT_NAME_SELECTOR)
        product_name = product_name_element.text.strip() if product_name_element else "Name not found"

        product_price_element = soup.select_one(PRODUCT_PRICE_SELECTOR)
        product_price = product_price_element.text.strip() if product_price_element else "Price not found"

        # --- Extract all reviews ---
        reviews_data = []
        review_containers = soup.select(REVIEW_CONTAINER_SELECTOR)

        if not review_containers:
            logging.warning(f"No reviews found on {product_url}. The review selector might be wrong.")
            # Still add the product info if no reviews are present
            reviews_data.append({
                "Product URL": product_url,
                "Product Name": product_name,
                "Product Price": product_price,
                "Review Rating": "No Reviews",
                "Review Title": "No Reviews",
                "Review Content": "No Reviews"
            })
            return reviews_data
        
        for review in review_containers:
            rating_element = review.select_one(REVIEW_RATING_SELECTOR)
            rating = rating_element.text.strip() if rating_element else "N/A"
            
            title_element = review.select_one(REVIEW_TITLE_SELECTOR)
            title = title_element.text.strip() if title_element else "N/A"
            
            content_element = review.select_one(REVIEW_CONTENT_SELECTOR)
            # The content is sometimes nested, so we get all text inside the div
            content = ' '.join(content_element.stripped_strings) if content_element else "N/A"

            reviews_data.append({
                "Product URL": product_url,
                "Product Name": product_name,
                "Product Price": product_price,
                "Review Rating": rating,
                "Review Title": title,
                "Review Content": content,
            })
        
        return reviews_data

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch product page {product_url}: {e}")
        return []
    except Exception as e:
        logging.error(f"An error occurred while parsing {product_url}: {e}")
        return []


def save_to_csv(data: list, filename: str):
    """
    Saves a list of dictionaries to a CSV file.

    Args:
        data: A list of dictionaries to save.
        filename: The name of the output CSV file.
    """
    if not data:
        logging.warning("No data to save. The CSV file will not be created.")
        return

    # Use the keys from the first dictionary as headers
    headers = data[0].keys()

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Successfully saved {len(data)} rows to {filename}")
    except IOError as e:
        logging.error(f"Could not write to file {filename}: {e}")


def main():
    """Main function to run the scraper."""
    product_to_search = input("Enter the product you want to search for on Flipkart: ")
    
    if not product_to_search:
        print("Product name cannot be empty. Exiting.")
        return

    product_links = get_product_links(product_to_search)

    if not product_links:
        print("Could not find any products. Please check your search term or the script's selectors.")
        return

    all_product_data = []
    total_links = len(product_links)

    for i, link in enumerate(product_links, 1):
        logging.info(f"Scraping product {i}/{total_links}: {link}")
        product_reviews = scrape_product_page(link)
        if product_reviews:
            all_product_data.extend(product_reviews)
        # A small delay to be polite to Flipkart's servers
        time.sleep(1) 

    # Generate a clean filename from the search query
    output_filename = f"{product_to_search.replace(' ', '_').lower()}_reviews.csv"
    save_to_csv(all_product_data, output_filename)
    
    print(f"\n✅ Scraping complete! Data saved to '{output_filename}'")


if __name__ == "__main__":
    main()