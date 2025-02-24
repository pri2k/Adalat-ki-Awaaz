import requests
from bs4 import BeautifulSoup
from dagster import asset

@asset
def starting_urls() -> list:
    """
    Returns the list of starting URLs.
    """
    return ["https://www.livelaw.in/top-stories"]


@asset
def find_more_urls(starting_urls: list) -> list:
    """
    Look for links to high court judgments and case status detail pages 
    from the starting URL(s). Ingest up to 10 pages.
    """
    all_links = []
    for url in starting_urls:
        response = requests.get(url)
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Grab up to 10 relevant links
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "high-court" in href:  # Simple filter to find relevant links
                # Normalize relative URLs
                if not href.startswith("http"):
                    href = f"https://www.livelaw.in{href}"
                links.append(href)
        
        # Limit to 10
        all_links.extend(links[:10])
    
    return all_links[:10]


@asset
def extract_data(find_more_urls: list) -> list:
    """
    Extract data (title, date, court, summary, url) from each link's full HTML.
    """
    data = []

    for url in find_more_urls:
        response = requests.get(url)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")

        title_element = soup.find("h1")
        date_element = soup.find("time")
        meta_desc = soup.find("meta", {"name": "description"})

        title = title_element.get_text(strip=True) if title_element else "No Title"
        date = date_element.get_text(strip=True) if date_element else "No Date"
        court = "Unknown Court"  # For demonstration only
        summary = meta_desc["content"] if meta_desc else "No Summary"

        data.append({
            "title": title,
            "date": date,
            "court": court,
            "summary": summary,
            "url": url
        })

    return data
