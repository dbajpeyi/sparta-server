from django.shortcuts import render
from article.models import *
from account.models import *
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from article.serializers import ArticleSerializer
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework_jwt.authentication import jwt_get_username_from_payload 
from rest_framework.authentication import get_authorization_header


class ArticleList(APIView):

    def get(self, request, format=None):
        auth = get_authorization_header(request).split()[1]
        payload = jwt_decode_handler(auth)
        username = jwt_get_username_from_payload(payload)
        user = self.get_user_for(username)
        if self.redis_data_for(user):
            serializer = ArticleSerializer(self.redis_data_for(user), many=True)

        serializer = ArticleSerializer(self.get_db_articles_for(user), many=True)
        return Response(serializer.data)

    def redis_data_for(self, user):
        if cache.has_key(user.ext_id):
            return cache.get(user.ext_id)

    def get_user_for(self, username):
        return Profile.objects.get(user = User.objects.get(username = username))

    def get_db_articles_for(self, user):
        liked_articles = LikedArticle.objects.filter(profile = user)
        return Article.objects.exclude(likedarticle__in = liked_articles)
                

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



