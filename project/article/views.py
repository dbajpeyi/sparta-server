from django.shortcuts import render
from article.models import Article, ArticleAction 
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from article.serializers import * 
from account.utils import *
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class ArticleList(APIView):

    RESULTS_PER_PAGE = 10

    def get(self, request, format=None):
        user = get_user_from(request)
        if self.redis_data_for(user):
            serializer = ArticleSerializer(self.redis_data_for(user), many=True)
        serializer = ArticleSerializer(self.get_db_articles_for(user), many=True)
        return Response(serializer.data)

    def redis_data_for(self, user):
        if cache.has_key(user.ext_id):
            articles = cache.get(user.ext_id)
            return self.paginate_result(articles)

    def get_db_articles_for(self, user):
        actioned_articles = ArticleAction.objects.filter(profile = user).values_list('article', flat=True)
        articles = Article.objects.exclude(articleaction__article__in = actioned_articles).order_by('-posted_on')
        return self.paginate_result(articles)

    def paginate_result(self, objects):
        page = self.request.query_params.get('page')
        paginator = Paginator(objects, self.RESULTS_PER_PAGE)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects =paginator.page(paginator.num_pages)
        return objects 

                
class LikedArticleListView(ListAPIView):

    serializer_class = ArticleActionSerializer

    def get_queryset(self):
        user = get_user_from(self.request)
        return ArticleAction.objects.filter(profile=user, is_liked=True)


class ArticleActionView(APIView):


    def remove_from_redis(self, key, article):
        articles = cache.get(key)
        articles.remove(article)
        cache.set(key, articles, timeout=None)

    def post(self, request, format=None):
        user = get_user_from(request)
        article = Article.objects.get(ext_id = request.data.get('ext_id'))
        is_liked = request.data.get('is_liked')
        self.remove_from_redis(user.ext_id, article)
        article_action, created = ArticleAction.objects.get_or_create(
                    profile = user,
                    article = article,
                    is_liked= is_liked
                )
        serializer = ArticleActionSerializer(instance = article_action)
        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message' : 'Already liked/unliked article'}, status=status.HTTP_200_OK)

class ArticleDetailView(RetrieveAPIView):

    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.all()
    lookup_field = 'ext_id'



class ReadArticleView(APIView):

    def put(self, request, ext_id, format=None):
        user = get_user_from(request)
        article = Article.objects.get(ext_id = ext_id)
        article_action = ArticleAction.objects.get(profile=user, article=article)
        article_action.is_read=True
        article_action.save()
        serializer = ArticleActionSerializer(instance = article_action)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



        

