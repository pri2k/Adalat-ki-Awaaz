import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from seo_publisher.models import Article
from django.conf import settings

def publish_to_wordpress():
    try:
        # Load credentials securely from Django settings
        wp_url = settings.WORDPRESS_URL
        wp_username = settings.WORDPRESS_USERNAME
        wp_password = settings.WORDPRESS_PASSWORD

        # Connect to WordPress
        wp = Client(wp_url, wp_username, wp_password)

        # Get unpublished articles
        articles = Article.objects.filter(published=False)
        for article in articles:
            post = WordPressPost()
            post.title = article.title
            post.content = article.content
            post.terms_names = {
                'category': ['General'],
                'post_tag': ['News']
            }
            post.post_status = 'publish'

            # Publish post
            wp.call(NewPost(post))
            article.published = True
            article.save()
            print(f"✅ Published: {article.title}")

    except Exception as e:
        print(f"❌ Error publishing article: {e}")
