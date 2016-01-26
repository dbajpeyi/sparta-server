from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
import logging
from article.models import *
from account.models import *
from datetime import datetime
from bs4 import BeautifulSoup


class Command(BaseCommand):
    
    SPORTS = ['cricket', 'football']
    BASE_URL = settings.ARTICLE_URL
    NUM_PAGES = 5

    def handle(self, *args, **options):
        
        logger = logging.getLogger('load_articles')
        for sport in self.SPORTS:
            logger.info('setting sport')
            self.sport = sport
            obj, created = self.create_sport()
            self.create_articles(obj)


    def create_sport(self):
        return Sport.objects.get_or_create(name=self.sport, defaults={'name' : self.sport})

    def create_articles(self, sport_obj):
        for page in xrange(1,self.NUM_PAGES):
            url = "{0}{1}/page/{2}".format(self.BASE_URL, self.sport, page) 
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.findAll("div", { "class" : "articles" })
            json_articles = map(self.json_articles, articles)
            for a in json_articles:
                print a

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
       return  datetime.strptime(date_str, "%B %d, %Y %I:%M %p")


