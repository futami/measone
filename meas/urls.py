from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'conditions', views.ConditionViewSet)
router.register(r'entries', views.EntryViewSet)

from django.conf.urls import url
urlpatterns = [
    url(r'^conditions/$', views.ConditionListView.as_view(), name='list'),
    url(r'^condition/(?P<pk>\d+)$', views.ConditionDetailView.as_view(), name='detail'),
]

# はじめての Django アプリ作成、その 3 | Django documentation | Django 
# https://docs.djangoproject.com/ja/1.11/intro/tutorial03/
#urlpatterns += [
#    url(r'^$', views.index, name='index'),
#]

# はじめての Django アプリ作成、その 4 | Django documentation | Django 
# https://docs.djangoproject.com/ja/1.11/intro/tutorial04/
urlpatterns += [
    url(r'^$', views.ConditionListView.as_view(), name='index'),
]
