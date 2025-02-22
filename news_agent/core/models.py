from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=100)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Summary(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE)
    summary = models.TextField()

    def __str__(self):
        return f"Summary of {self.article.title}"

class PublishedArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    seo_keywords = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title