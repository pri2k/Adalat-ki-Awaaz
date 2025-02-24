from django.contrib import admin
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'court', 'summary', 'url')  # Customize columns

# Or, simply:
# admin.site.register(Article)
