from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
import logging
from article.models import *
from account.models import *
from datetime import datetime
from django.utils import timezone
import pytz
import json
from bs4 import BeautifulSoup
from django.core.cache import cache


class Command(BaseCommand):
    
    SPORTS = ['cricket', 'football']
    BASE_URL = settings.ARTICLE_URL
    NUM_PAGES = 2
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
        print "articles loaded into memory"


    def create_articles_for(self, sport):
        print "Creating articles for : %s" % sport
        for article in self.articles:
            obj, created = Article.objects.get_or_create(
                    title = article.get('title'),
                    defaults = {
                        'sport' : sport,
                        'posted_on' : article.get('posted'),
                        'img_url' : article.get('img'),
                        'content' : article.get('content'),
                        'summary' : article.get('summary')
                    }
            )

            if created:
                print "Creating article in redis"
                self.update_user_in_redis(obj)

    def update_user_in_redis(self, obj):
        users = Profile.objects.all()

        for user in users:
            print user
            if cache.has_key(user.ext_id):
                value = cache.get(user.ext_id)
                value.append(obj)
                cache.set(user.ext_id, value, timeout=None)
            else:
                print "No key"
                fresh_value = []
                fresh_value.append(obj)
                cache.set(user.ext_id, fresh_value, timeout=None)


    def create_sport(self):
        return Sport.objects.get_or_create(name=self.sport, defaults={'name' : self.sport})

    def load_articles_in_mem(self):
        for page in xrange(1,self.NUM_PAGES):
            print "printing page %s" % page
            url = "{0}{1}/page/{2}".format(self.BASE_URL, self.sport, page) 
            print "Getting URL: %s" % url 
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles_html = soup.findAll("div", { "class" : "articles" })
            latest_article = articles_html[0]
            json_articles = map(self.json_articles, articles_html)
            self.articles.extend(json_articles)

    def is_latest(self, latest_article):
        latest_db = Article.objects.order_by('-posted_on').first()
        if latest_db:
            if self.convert_datetime(self.get_date(latest_article)) > latest_db.posted_on:
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
            "img" :  self.get_image(article),
            "title" : self.get_title(article),
            "content" : self.get_content(article), 
            "summary" : self.get_summary(article),
            "posted": self.convert_datetime(self.get_date(article))
        }
        
        
    def get_content(self, article):
        detail_url = article.find('div', {'class' : 'title'}).find('a')['href']
        response = requests.get(detail_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paras = soup.find('div', {'class' : 'full-details'}).find_all('p')
        content = "\n".join(p.getText() for p in paras)
        return content

    def get_date(self, article):
        return article.find('div', {'class' : 'date'}).string.strip()

    def get_title(self, article):
        return article.find('div', {'class' : 'title'}).find('a').contents[0].strip()

    def get_summary(self, article):
        return article.find('p').string.strip()


    def get_image(self, article):
        return article.find('img')['src']


    def convert_datetime(self, date_str):
        return pytz.timezone(settings.TIME_ZONE).localize(datetime.strptime(date_str, "%B %d, %Y %I:%M %p"))


