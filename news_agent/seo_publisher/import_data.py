import pandas as pd
from seo_publisher.models import Article
from datetime import datetime
from django.utils.timezone import make_aware
import csv
import pytz

def parse_publish_date(date_str):

    if not date_str or date_str.lower() == "not found":
        print(f"Replacing missing/invalid publish_date: {date_str} with current date.")
        return make_aware(datetime.now(), pytz.UTC)  # Use current date if missing or invalid

    formats = ["%d %b %Y %I:%M %p", "%Y-%m-%d", "%d %b %Y"]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return make_aware(dt, pytz.UTC)  # Convert to timezone-aware datetime
        except ValueError:
            continue

    # If none of the formats worked, use the current date as fallback
    print(f"Invalid publish_date format '{date_str}', using current date.")
    return make_aware(datetime.now(), pytz.UTC)

def import_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8-sig") as file:  # Use utf-8-sig to remove BOM
        reader = csv.DictReader(file)

        for row in reader:
            # print("Raw Row Data:", row)
            title = row.get("Title", "").strip()
            author = row.get("author", "").strip()
            content = row.get("Content", "").strip()
            url = row.get("url", "").strip()
            publish_date_str = row.get("publish_date", "").strip()
            publish_date = parse_publish_date(publish_date_str)

            if not title:
                print(f"Skipping row due to missing title: {row}")
                continue

            # Create and save the article
            Article.objects.create(
                title=title,
                author=author,
                content=content,
                url=url,
                publish_date=publish_date
            )
            print(f"Imported: {title}")

    print("CSV import completed successfully.")
