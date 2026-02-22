from django.shortcuts import render
from django.http import JsonResponse
from .script import scrape_imdb_news
from .models import News
# Create your views here.

def run_scraper(request):
    # from .script import scrape_imdb_news
    scrape_imdb_news()
    return JsonResponse({
        "status":True,
        "message":"scraper executed"
    })

def index(request):
    # from .models import News
    return render(request, 'index.html', context ={
        "news_data": News.objects.all()
    })