# Financial World PDF Scraper

A Python script to scrape all PDFs from the Financial World Delhi Edition website and package them into a single ZIP file.

---

## Features

- Automatically navigates all listing pages (pagination handled).
- Extracts article links and finds embedded PDFs.
- Downloads PDFs to a local folder.
- Creates a ZIP archive of all PDFs.

---

## Requirements

- Python 3.7+
- BeautifulSoup (`bs4`)
- requests
- lxml

Install dependencies:

```bash
pip install beautifulsoup4 requests lxml
```

Run the script:

```
python scrape.py
```

## Project Structure 📂

TIH_SCRAPING_ASSIGNMENT/
│
├── scrape.py
├── config.py
├── README.md
├── .gitignore
