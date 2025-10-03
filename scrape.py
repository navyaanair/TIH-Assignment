
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from zipfile import ZipFile
from config.py import BASE_URL, HEADERS, PDF_FOLDER, ZIP_FILE, TOTAL_PAGES


# --- FUNCTIONS ---
def get_listing_url(page):
    """Generate the URL for a given listing page."""
    if page == 1:
        return urljoin(BASE_URL, "/delhi-edition")
    return urljoin(BASE_URL, f"/delhi-edition/page/{page}/")


def collect_article_links():
    """Scrape all article links from the listing pages."""
    article_links = set()

    for page in range(1, TOTAL_PAGES + 1):
        url = get_listing_url(page)
        print(f"Scraping listing page: {url}")
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"Failed to load page: {e}")
            continue

        soup = BeautifulSoup(resp.text, "lxml")
        # Filter specific structure: <a> inside div.rt-detail h3.entry-title
        for a in soup.select("div.rt-detail h3.entry-title a"):
            href = a.get("href")
            if href:
                article_links.add(urljoin(BASE_URL, href))

    return sorted(article_links)


def collect_pdf_links(article_links):
    """Visit each article and extract PDF links."""
    pdf_links = set()

   
    for idx, article in enumerate(article_links, 1):
        print(f"[{idx}/{len(article_links)}] Visiting: {article}")
        try:
            resp = requests.get(article, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            print(f"Failed to load article: {e}")
            continue

        soup = BeautifulSoup(resp.text, "lxml")

        # Check for <object> tags containing PDFs
        for obj in soup.find_all("object", type="application/pdf"):
            data = obj.get("data")
            if data and ".pdf" in data:
                pdf_links.add(urljoin(BASE_URL, data))

        # Check for direct <a> links to PDFs
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().endswith(".pdf"):
                pdf_links.add(urljoin(BASE_URL, href))

    return sorted(pdf_links)


def download_pdfs(pdf_links):
    """Download all PDFs into a folder."""
    os.makedirs(PDF_FOLDER, exist_ok=True)

    for i, pdf_url in enumerate(pdf_links, 1):
        parsed = urlparse(pdf_url)
        fname = os.path.basename(parsed.path) or f"file_{i}.pdf"
        out_path = os.path.join(PDF_FOLDER, fname)
        print(f"[{i}/{len(pdf_links)}] Downloading: {pdf_url} -> {out_path}")
        try:
            with requests.get(pdf_url, headers=HEADERS, stream=True, timeout=30) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            print(f"Failed to download: {e}")


def zip_pdfs():
    """Zip all PDFs into a single archive."""
    with ZipFile(ZIP_FILE, "w") as zf:
        for f in os.listdir(PDF_FOLDER):
            zf.write(os.path.join(PDF_FOLDER, f), arcname=f)
    


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    article_links = collect_article_links()
    pdf_links = collect_pdf_links(article_links)
    download_pdfs(pdf_links)
    zip_pdfs()
