from dagster import repository
from assets import starting_urls, find_story_urls, extract_story_data, save_stories

@repository
def scraper_repository():
    """
    Registers the assets for scraping the High Court section.
    """
    return [starting_urls, find_story_urls, extract_story_data, save_stories]
