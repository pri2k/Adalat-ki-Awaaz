import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost
from wordpress_xmlrpc.methods import posts
from seo_publisher.models import Article
from django.conf import settings

def generate_seo_title(article):
    """Generate an SEO-friendly title, including the court name if available."""
    if article.court:
        return f"{article.title} - {article.court} Ruling"
    return f"{article.title} - Legal Update"

def generate_meta_description(article):
    """Generate an SEO-optimized meta description from the summary."""
    return article.summary[:160] if article.summary else "Latest legal updates and news."

def publish_to_wordpress():
    try:
    
        wp_url = settings.WORDPRESS_URL
        wp_username = settings.WORDPRESS_USERNAME
        wp_password = settings.WORDPRESS_PASSWORD

        wp = Client(wp_url, wp_username, wp_password)

        articles = Article.objects.filter(published=False)
        for article in articles:
            post = WordPressPost()
            post.title = generate_seo_title(article)  
            post.content = f"<p><strong>Court:</strong> {article.court or 'Not specified'}</p>" \
                           f"<p>{article.summary}</p>" \
                           f"<p>🔗 <a href='{article.url}' target='_blank'>Read full case</a></p>"


            post.terms_names = {
                'category': ['Legal Updates'],
                'post_tag': [article.court or 'Unknown Court', 'Legal News', 'Latest']
            }
            post.post_status = 'publish'

            post_id = wp.call(NewPost(post))
            
            seo_metadata = {
                'seo_title': generate_seo_title(article),
                'meta_description': generate_meta_description(article),
                'canonical_url': article.url 
            }
            
            for key, value in seo_metadata.items():
                wp.call(EditPost(post_id, {'custom_fields': [{'key': key, 'value': value}]}))

            article.published = True
            article.save()
            print(f"✅ Published: {article.title}")

    except Exception as e:
        print(f"❌ Error publishing article: {e}")
