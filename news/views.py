# from unicodedata import category
from django.shortcuts import render
from django.views import View
from news.cron import get_news
from news.models import News



class HomeView(View):
    def get(self, request, *args, **kwargs):
        search_content = request.GET.get("search","")
        category=request.GET.get("category")

        filter = {
            
            "heading__icontains": search_content,
            "content__icontains": search_content,
        }
        if category:
            filter["news_cat"] = category

        base_qs = News.objects.filter(**filter)
        
        if not base_qs.exists():
            get_news()
        context = {
            "annapurna": base_qs.filter(
                source="annapurna"
            ),
            "india": base_qs.filter(
                source="india"
            ),
        }
        
        return render(request, 'news/index.html', context)

