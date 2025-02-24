from dagster import repository, with_resources
from assets import starting_urls, find_more_urls, extract_data

@repository
def scraper_repository():
    """
    Repository that includes our assets. 
    You can optionally define resources or schedules here as well.
    """
    return [starting_urls, find_more_urls, extract_data]
