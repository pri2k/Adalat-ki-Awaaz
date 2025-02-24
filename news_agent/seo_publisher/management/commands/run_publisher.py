from django.core.management.base import BaseCommand
from seo_publisher.import_data import import_csv
from seo_publisher.publish_to_wordpress import publish_to_wordpress

class Command(BaseCommand):
    help = "Run the SEO publisher workflow"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Step 1: Import data
        self.stdout.write("Importing data from CSV...")
        import_csv(file_path)

        # Step 2: Publish articles to WordPress
        self.stdout.write("Publishing articles to WordPress...")
        publish_to_wordpress()

        self.stdout.write(self.style.SUCCESS("Workflow completed!"))