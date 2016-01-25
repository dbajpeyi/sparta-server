from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
import logging
from article.models import *
from account.models import *


class Command(BaseCommand):
    
    SPORTS = ['cricket', 'football']
    BASE_URL = settings.ARTICLE_URL

    def handle(self, *args, **options):
        
        urls = ["%s%s"%(self.BASE_URL, sport) for sport in self.SPORTS]
        for url in urls:
            self.create_articles(url)



