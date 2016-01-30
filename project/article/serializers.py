from rest_framework import serializers
from article.models import Article, ArticleAction 
from account.serializers import ProfileSerializer
from account.models import Profile

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('ext_id', 'title','sport', 'posted_on', 'summary', 'img_url')

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'img_url', 'content', 'posted_on')

class ArticleActionSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    profile = ProfileSerializer()
    class Meta:
        model = ArticleAction


