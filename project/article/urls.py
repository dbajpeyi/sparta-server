from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from article import views

urlpatterns = [
    url(r'^articles', views.ArticleList.as_view()),
    #url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)