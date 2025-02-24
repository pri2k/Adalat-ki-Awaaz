import pandas as pd
from seo_publisher.models import Article
from datetime import datetime
from django.utils.timezone import make_aware
import csv
import pytz

def parse_publish_date(date_str):
    if not date_str or date_str.lower() == "not found":
        print(f"Replacing missing/invalid publish_date: {date_str} with current date.")
        return make_aware(datetime.now(), pytz.UTC)  

    formats = ["%d %b %Y %I:%M %p", "%Y-%m-%d", "%d %b %Y"]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return make_aware(dt, pytz.UTC)  # Convert to timezone-aware datetime
        except ValueError:
            continue

    print(f"Invalid publish_date format '{date_str}', using current date.")
    return make_aware(datetime.now(), pytz.UTC)

def import_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8-sig") as file:  # Use utf-8-sig to remove BOM
        reader = csv.DictReader(file)

        for row in reader:
          
            title = row.get("title", "").strip()
            court = row.get("court", "").strip()  
            summary = row.get("summary", "").strip()  
            url = row.get("url", "").strip() 
            publish_date_str = row.get("date", "").strip() 
            publish_date = parse_publish_date(publish_date_str)

            if not title:
                print(f"Skipping row due to missing title: {row}")
                continue

            Article.objects.create(
                title=title,
                court=court, 
                summary=summary, 
                url=url,
                publish_date=publish_date
            )
            print(f"Imported: {title}")

    print("CSV import completed successfully.")
