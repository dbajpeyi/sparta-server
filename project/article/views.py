from django.shortcuts import render
from article.models import *
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
        liked_articles = LikedArticle.objects.filter(profile = user)
        #TODO: In case redis flops, This query needs to only give the latest and the nonliked stuff
        return Article.objects.exclude(likedarticle__in = liked_articles)
                


class LikeUnlikeBase(APIView):

    def get_201_done(self, serializer):
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_200_exists(self, message):
        return Response({'message' : message}, status=status.HTTP_200_OK)


class LikeArticle(LikeUnlikeBase):

    def post(self, request, format=None):
        user = get_user_from(request)
        article = Article.objects.get(ext_id = request.POST.get('ext_id'))
        liked_article, created = LikedArticle.objects.get_or_create(
                    profile = user,
                    article = article 
                )
        serializer = LikedArticleSerializer(instance = liked_article)
        if created:
            return self.get_201_done(serializer)
        return self.get_200_exists("Already liked")
        
class UnlikeArticle(LikeUnlikeBase):

    def post(self, request, format=None):
        user = get_user_from(request)
        article = Article.objects.get(ext_id = request.POST.get('ext_id'))
        unliked_article, created = UnlikedArticle.objects.get_or_create(
                    profile = user,
                    article = article 
                )
        serializer = UnlikedArticleSerializer(instance = liked_article)
        if created:
            return self.get_201_done(serializer)
        return self.get_200_exists("Already unliked")
        

