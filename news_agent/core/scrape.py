import requests
from bs4 import BeautifulSoup
from .models import Article

def scrape_bbc_news():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for headline in soup.find_all("h3"):
        title = headline.text
        link = headline.find_parent("a")["href"]
        full_url = f"https://www.bbc.com{link}"

        # Fetch article content
        article_response = requests.get(full_url)
        article_soup = BeautifulSoup(article_response.text, "html.parser")
        content = article_soup.find("div", {"class": "ssrcss-11r1m41-RichTextContainer"}).text

        # Save to database
        Article.objects.create(title=title, source="BBC", content=content)

# Run the scraper
scrape_bbc_news()