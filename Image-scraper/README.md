
# 🖼️ Image Scraper using Flask, BeautifulSoup & More

This project is a web-based image scraping tool built with **Flask**, **BeautifulSoup**, and other Python libraries. It allows you to scrape and download images from Google or any public website by providing a search term or URL.

## 🚀 Features

* Scrape images from Google or other websites
* Use a simple Flask interface to submit search terms or links
* Automatically saves all downloaded images into a local folder
* Supports extension with additional scraping tools like `requests`, `selenium`, and `methane`
* Flexible scraping: works for various types of media and websites

## 🧰 Tech Stack

* **Python 3.x**
* **Flask** – for the web interface
* **BeautifulSoup** – for parsing HTML content
* **requests / selenium** – for fetching web pages (depending on implementation)
* **os / shutil** – for directory and file handling

## 📦 Installation

1. Clone the repo:  git clone https://github.com/VishnukumarWDS/Projects/tree/main/Image-scraper
2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage

1. Run the Flask app:

   ```bash
   python app.py
   ```

2. Open your browser and go to:

   ```
   http://localhost:8000
   ```

3. Enter your search term or a website URL, and click "Fetch Images".

4. Images will be downloaded and saved to a folder (e.g., `static/images/`).

## 📁 Output

All scraped images will be stored in a structured folder within your project directory. Each query gets its own subfolder.

## ⚠️ Disclaimer

This tool is intended for educational and personal use only. Scraping websites can violate their terms of service. Always check the site's **robots.txt** and terms before scraping.
