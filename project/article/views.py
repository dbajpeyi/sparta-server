from django.shortcuts import render
from article.models import Article, ArticleAction 
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from article.serializers import * 
from article.utils import *


class ArticleList(APIView):

    def get(self, request, format=None):
        user = get_user_from(request)
        if self.redis_data_for(user):
            serializer = ArticleSerializer(self.redis_data_for(user), many=True)
        serializer = ArticleSerializer(self.get_db_articles_for(user), many=True)
        return Response(serializer.data)

    def redis_data_for(self, user):
        if cache.has_key(user.ext_id):
            return cache.get(user.ext_id)

    def get_db_articles_for(self, user):
        liked_articles = ArticleAction.objects.filter(profile = user, is_liked=True).values_list('article', flat=True)
        #TODO: In case redis flops, This query needs to only give the latest and the nonliked stuff
        return Article.objects.exclude(articleaction__article__in = liked_articles)
                


class ArticleActionView(APIView):

    def remove_from_redis(self, key, article):
        articles = cache.get(key)
        articles.remove(article)
        cache.set(key, articles)

    def post(self, request, format=None):
        user = get_user_from(request)
        article = Article.objects.get(ext_id = request.data.get('ext_id'))
        self.remove_from_redis(user.ext_id, article)
        is_liked = request.data.get('is_liked')
        article_action, created = ArticleAction.objects.get_or_create(
                    profile = user,
                    article = article,
                    is_liked= is_liked
                )
        serializer = ArticleActionSerializer(instance = article_action)
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message' : 'Already liked/unliked article'}, status=status.HTTP_200_OK)
        

