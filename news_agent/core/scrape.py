import requests
from bs4 import BeautifulSoup
from core.models import Article

def scrape_bbc_news():
    url = "https://www.bbc.com/news"
    try:
        # Fetch the main news page
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all headlines
    headlines = soup.find_all("h3")
    if not headlines:
        print("No headlines found on the page.")
        return

    for headline in headlines:
        title = headline.text.strip()
        link = headline.find_parent("a")["href"]
        full_url = f"https://www.bbc.com{link}"

        try:
            # Fetch the article content
            article_response = requests.get(full_url)
            article_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching article {full_url}: {e}")
            continue

        # Parse the article content
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        content_div = article_soup.find("div", {"class": "ssrcss-11r1m41-RichTextContainer"})
        if not content_div:
            print(f"No content found for article: {title}")
            continue

        content = content_div.text.strip()

        # Save to database
        Article.objects.create(title=title, source="BBC", content=content)
        print(f"Saved article: {title}")

# Run the scraper
scrape_bbc_news()