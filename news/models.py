from turtle import heading
from django.db import models
# from news.forms import NewsForm
from datetime import datetime
class News(models.Model):
    NEWS_CAT_CHOICES = (
        ('TCH', 'Technology'),
        ('SPR', 'Sports'),
        ('BSN', 'Business'),
        ('ENT', 'Entertainment'),
        ('POL', 'Politics'),
        ('OTHR','Others')
    )
    heading=models.CharField(max_length=1000)
    image_url = models.URLField(max_length=1000)
    content = models.TextField(max_length=6000)
    source = models.CharField(max_length=255)
    forward_link = models.URLField(max_length=1000)
    news_cat = models.CharField(
        max_length=50, 
        choices=NEWS_CAT_CHOICES, 
        null=False, 
        blank=False,
    )

    def __str__(self):
        return f"[{self.source}] " + self.heading
class news_cron(models.Model):
    news_cron1 = models.BigIntegerField(unique=True, primary_key=True)
    fetched_at = models.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        self.id = self.news_cron1 # replacing the id(primary key) as the hackernews id
        super(news_cron, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.news_cron1)