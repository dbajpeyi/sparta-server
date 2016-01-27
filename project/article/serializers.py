from rest_framework import serializers
from article.models import Article, LikedArticle
from account.serializers import ProfileSerializer
from account.models import Profile

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('ext_id', 'title','sport', 'posted_on', 'summary', 'img_url')


class LikedArticleSerializer(serializers.ModelSerializer):
    article = ArticleSerializer()
    profile = ProfileSerializer()
    class Meta:
        model = LikedArticle


