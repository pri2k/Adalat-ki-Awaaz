import requests
from bs4 import BeautifulSoup
from dagster import asset
import re
import datetime

@asset
def starting_urls() -> list:
    """
    Returns the starting URL for LiveLaw's High Court section.
    """
    return ["https://www.livelaw.in/high-court"]

@asset
def find_story_urls(starting_urls: list) -> list:
    """
    Fetches the starting URL and extracts URLs for individual high court stories.
    This extraction targets article links that are expected to have specific patterns.
    """
    all_links = []
    for url in starting_urls:
        response = requests.get(url)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all anchor tags that likely represent story links.
        # This pattern might change based on the site's structure.
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # Filter for links that include the high court slug
            if re.search(r'/high-court/', href):
                # Normalize relative URLs
                if not href.startswith("http"):
                    href = f"https://www.livelaw.in{href}"
                all_links.append(href)
        
    # Remove duplicates and limit to the first 10 stories
    unique_links = list(dict.fromkeys(all_links))
    return unique_links[:10]

@asset
def extract_story_data(find_story_urls: list) -> list:
    """
    Extracts detailed information from each high court story URL.
    The extraction includes title, publication date, summary, and other details.
    """
    stories = []
    
    for url in find_story_urls:
        response = requests.get(url)
        if response.status_code != 200:
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title from <h1> or a primary header
        title_tag = soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        
        # Extract publication date: Try to find a <time> tag or a date element
        date_tag = soup.find("time")
        if date_tag and date_tag.has_attr("datetime"):
            date_str = date_tag["datetime"]
        elif date_tag:
            date_str = date_tag.get_text(strip=True)
        else:
            date_str = "No Date"
        
        # Parse date string if possible
        try:
            published_date = datetime.datetime.fromisoformat(date_str)
            published_date = published_date.strftime("%Y-%m-%d")
        except Exception:
            published_date = date_str
        
        # Extract summary: Look for meta description or a summary paragraph
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.has_attr("content"):
            summary = meta_desc["content"]
        else:
            # Fallback: try finding the first paragraph
            p_tag = soup.find("p")
            summary = p_tag.get_text(strip=True) if p_tag else "No Summary"
        
        # Extract additional details if available (e.g., court details or tags)
        court_info = "High Court"  # Static or extracted from the page if present
        
        # Optionally, extract author or other metadata
        author_tag = soup.find("span", class_=re.compile("author", re.I))
        author = author_tag.get_text(strip=True) if author_tag else "Unknown Author"
        
        stories.append({
            "title": title,
            "published_date": published_date,
            "summary": summary,
            "court": court_info,
            "author": author,
            "url": url,
        })
    
    return stories

@asset
def save_stories(extract_story_data: list) -> str:
    """
    Saves the extracted stories to a JSON file.
    """
    import json
    output_file = "high_court_stories.json"
    with open(output_file, "w") as f:
        json.dump(extract_story_data, f, indent=4)
    return f"Data saved to {output_file}"
