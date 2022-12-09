from urllib.parse import urlparse
from bs4 import BeautifulSoup
from django_cron import CronJobBase, Schedule
import requests
from .models import News

ANNAPURNA_LINKS = [
    "https://annapurnatimes.com/archives/category/recent-news-2",
    "https://annapurnatimes.com/archives/category/sports",
    "https://annapurnatimes.com/archives/category/entertainment",
    "https://annapurnatimes.com/archives/category/economy",
]
toi_ent=[
    "https://timesofindia.indiatimes.com/entertainment/hindi/bollywood/news",
    "https://timesofindia.indiatimes.com/entertainment/english/hollywood/news"
    ]
toi_exp=["https://timesofindia.indiatimes.com/explainers/sports",
"https://timesofindia.indiatimes.com/explainers/business",
"https://timesofindia.indiatimes.com/explainers/gadgets",
"https://timesofindia.indiatimes.com/explainers/world"
]

toi_pol= "https://timesofindia.indiatimes.com/politics/news"

page=["https://timesofindia.indiatimes.com/briefs"]

def get_category(url, index):
    category_mapper = {
        "sports": "SPR",
        "entertainment": "ENT",
        "business": "BSN",
        "politics": "POL",
        "gadgets": "TCH",
        # "economy":"POL",
        
        
    }
    url_parse=urlparse(url)
    path = url_parse.path
    return category_mapper.get(path.split('/')[index], "OTHR")

def get_headings_from_scrapper(link, class_name):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, 'html5lib')
    if link in toi_exp:
        return  soup.find_all("li")
    else:
        return soup.find_all("div", {"class": class_name})


def get_news():
    for link in ANNAPURNA_LINKS:
        for  news_heading in get_headings_from_scrapper(link, "meta-info-container"):
            heading = getattr(news_heading.h3, 'text', "Babal News")
            if not News.objects.filter(heading=heading).exists():
                News.objects.create(
                    heading= heading,
                    image_url= news_heading.img["data-img-url"],
                    content = news_heading.text,
                    forward_link = news_heading.h3.a["href"],
                    source = "annapurna",
                    news_cat = get_category(link, 3)
                )
      
    
    for hth in get_headings_from_scrapper("https://timesofindia.indiatimes.com/briefs", "brief_box"):
        heading = getattr(hth.h2, 'text', "PK")
        if not News.objects.filter(heading=heading).exists():
            News.objects.create(
                heading= heading,
                image_url= hth.img["data-src"] if hth.img else "https://cdn.britannica.com/70/2970-050-796F522C/Flag-Nepal.jpg",
                content = hth.text,
                forward_link = "https://timesofindia.indiatimes.com/" + hth.h2.a["href"] if hth.h2 else "https://cdn.britannica.com/70/2970-050-796F522C/Flag-Nepal.jpg",
                source = "india"
            )

    for tent in toi_ent: 
        for  th in get_headings_from_scrapper(tent, "md_news_box"):
            heading = getattr(th.p, 'text', "Babal News")
            if not News.objects.filter(heading=heading).exists():
                News.objects.create(
                    heading= heading,
                    image_url= th.img["src"] if th.img else "",
                    content = th.text,
                    forward_link = "https://timesofindia.indiatimes.com/"+ th.a["href"] if th.a else "",
                    source = "india",
                    news_cat = get_category(tent, 1)
                
            )

    # for  x in get_headings_from_scrapper(toi_exp, ""):
       
    # # for  x in get_headings_from_scrapper(toi_tech, "2QMN9"):
    #     heading = getattr(x.h5, 'text', "Babal News")
    #     if not News.objects.filter(heading=heading).exists():
    #         News.objects.create(
    #             heading= heading,
    #             image_url= x.img["src"] if x.img else "",
    #             content = x.text,
    #             forward_link = "https://timesofindia.indiatimes.com/"+ x.a["href"] if x.a else "",
    #             source = "india",
    #             news_cat = get_category(toi_exp, 2)
    #             )

    for EXPS in toi_exp:
        for  z in get_headings_from_scrapper(EXPS, "pE3Ep"):
            heading = getattr(z.h5, 'text', "Babal News")
            if not News.objects.filter(heading=heading).exists():
                News.objects.create(
                    heading= heading,
                    image_url= z.img["src"],
                    content = z.text,
                    forward_link = "https://timesofindia.indiatimes.com/"+ z.a["href"] if z.a else "",
                    source = "india",
                    news_cat = get_category(EXPS, 2)
                )
        
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'news.my_cron_job'    # a unique code
