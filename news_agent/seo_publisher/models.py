from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    publish_date = models.DateTimeField()
    court = models.CharField(max_length=255, blank=True, null=True)  
    summary = models.TextField(blank=True, null=True) 
    url = models.URLField(default="https://example.com")  
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
