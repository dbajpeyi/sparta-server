from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
import logging
from article.models import *
from account.models import *
from datetime import datetime
from django.utils import timezone
import pytz
from bs4 import BeautifulSoup


class Command(BaseCommand):
    
    SPORTS = ['cricket', 'football']
    BASE_URL = settings.ARTICLE_URL
    NUM_PAGES = 5
    articles = []

    def handle(self, *args, **options):
        
        logger = logging.getLogger('load_articles')
        for sport in self.SPORTS:
            logger.info('setting sport')
            self.sport = sport
            self.load_articles_in_mem()
            obj, created = self.create_sport()
            self.create_articles_for(obj)
        logger.info("Articles loaded in memory %s" % len(self.articles))


    def create_articles_for(self, obj):
        return



    def create_sport(self):
        return Sport.objects.get_or_create(name=self.sport, defaults={'name' : self.sport})

    def load_articles_in_mem(self):
        for page in xrange(1,self.NUM_PAGES):
            url = "{0}{1}/page/{2}".format(self.BASE_URL, self.sport, page) 
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles_html = soup.findAll("div", { "class" : "articles" })
            latest_article = articles_html[0]
            if self.is_latest(latest_article):
                json_articles = map(self.json_articles, articles_html)
                self.articles.extend(json_articles)
            else:
                break

    def is_latest(self, latest_article):
        latest_db = Article.objects.order_by('-posted_on').first()
        if latest_db:
            if self.get_date(latest_article) > latest_db.posted_on:
                return True
            else:
                return False
        else:
            return True

    def get_date(self, article):
        return self.convert_datetime(
               article.find('div', 
               {'class' : 'date'}).string.strip()
           )


    def json_articles(self, article):
        return {
            "img" : article.find('img')['src'],
            "title" : article.find('div', {'class' : 'title'}).find('a').contents[0],
            "summary" : article.find('p').string.strip(),
            "posted": self.convert_datetime(
                article.find('div', {'class' : 'date'}).string.strip() ,
            )
        }


    def convert_datetime(self, date_str):
        return pytz.timezone(settings.TIME_ZONE).localize(datetime.strptime(date_str, "%B %d, %Y %I:%M %p"))


