---

**FlipTrack Notebook – Flipkart Price & Review Tracker in One Click**

---

## 📄 `README.md`

# FlipTrack Notebook – Flipkart Price & Review Tracker in One Click

**FlipTrack Notebook** is a Jupyter Notebook project that helps users instantly track product prices, ratings, reviews, and links from Flipkart by simply entering the product name. It uses web scraping with BeautifulSoup and exports all relevant product data into an Excel file for easy comparison and analysis.

## ✅ Key Features

- 🧠 One-click product search via Jupyter Notebook
- 🔗 Auto-generation of direct Flipkart product links
- 💬 Fetches product name, price, rating, and customer reviews
- 📁 Automatically exports the data to `product_data.xlsx`
- 📊 Designed for quick analysis in Excel or Google Sheets

## 🧰 Tech Used

- **Python**
- **Jupyter Notebook**
- **BeautifulSoup (bs4)**
- **requests**
- **pandas**
- **openpyxl** (for writing Excel files)

## 🚀 How to Use

1. **Clone or download** this repository.
2. Open the notebook `FlipTrack.ipynb` using **Jupyter Notebook** or **JupyterLab**.
3. Run the first cell to install and import all libraries.
4. Modify the `product = "your product name"` line with the item you want to search (e.g., `"iPhone 14"`).
5. Run all cells in the notebook (`Kernel > Restart & Run All`).
6. The notebook will:
    - Display key product details
    - Show a clickable product link
    - Save everything in an Excel file called `product_data.xlsx`
7. Python automates script - app.py : using `Flask` 

## 📁 Output Example

| Product Name        | Price    | Rating | Reviews                              | Link                              |
|---------------------|----------|--------|---------------------------------------|-----------------------------------|
| iPhone 14 (128 GB)  | ₹64,999  | 4.5★   | "Amazing phone, great performance..." | [Open in Flipkart](https://www.flipkart.com/...) |

## 🔧 Requirements

Install the required packages before running the notebook:

```bash
pip install beautifulsoup4 requests pandas openpyxl
````

> Or use the first cell in the notebook – it handles imports and installations automatically.

## 📌 Notes

* Flipkart may occasionally change their website structure. If scraping fails, inspect the HTML and update the BeautifulSoup selectors accordingly.
* This project is for educational and personal use. Be mindful of Flipkart's [Terms of Use](https://www.flipkart.com/pages/terms).

## 📄 License

This project is licensed under the MIT License.

---

> Created with ❤️ by Vishnu and Team

```

---
