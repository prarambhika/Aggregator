from rest_framework import serializers
from .models import news_cron

class NewsIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = news_cron
        fields = ('news_cron1',)