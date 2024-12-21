from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os

app = Flask(__name__)
CORS(app)

# Function to scrape event data
def scrape_event_data():
    party_list = [
        "https://www.bookmyballoons.in/product-category/birthday-decoration",
        "https://www.bookmyballoons.in/product-category/wedding-decoration",
        "https://www.bookmyballoons.in/services/baby-shower-decoration-in-bangalore",
        "https://www.bookmyballoons.in/services/welcome-baby-decoration-in-bangalore",
        "https://www.bookmyballoons.in/services/bachelor-party-decoration-in-bangalore"
    ]

    all_event_images = []
    all_event_names = []
    all_event_links = []

    for url in party_list:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        find_data = soup.find_all("div", {"class": "woo-buttons-on-img"})

        for data in find_data:
            try:
                event_image = data.img["data-src"]
                event_name = data.img['alt']
                event_link = data.a['href']

                all_event_images.append(event_image)
                all_event_names.append(event_name)
                all_event_links.append(event_link)
            except Exception as e:
                print(f"Error parsing data: {e}")

    # Create a DataFrame
    data = {
        'Event Name': all_event_names,
        'Event Image': all_event_images,
        'Event Link': all_event_links
    }
    df = pd.DataFrame(data)

    # Save to Excel
    output_file = 'event_data.xlsx'
    df.to_excel(output_file, index=False)

    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['GET'])
def scrape():
    try:
        data = scrape_event_data()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/download', methods=['GET'])
def download():
    file_path = 'event_data.xlsx'
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"status": "error", "message": "File not found"})

if __name__ == '__main__':
    app.run(debug=True)
