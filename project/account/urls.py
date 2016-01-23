from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from account import views

urlpatterns = [
    url(r'^signup', views.SignUp.as_view()),
    url(r'^login', views.Login.as_view()),
    #url(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
