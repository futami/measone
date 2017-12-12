from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'conditions', views.ConditionViewSet)
router.register(r'entries', views.EntryViewSet)

from django.conf.urls import url
urlpatterns = []
urlpatterns += [
    url(r'^conditions/$', views.ConditionListView.as_view(), name='list'),
    url(r'^conditions/(?P<pk>\d+)$', views.ConditionDetailView.as_view(), name='detail'),
]

urlpatterns += [
    url(r'^serials/$', views.SerialListView.as_view(), name='serial_list'),
    url(r'^serials/(?P<pk>[-\w]+)$', views.SerialDetailView, name='serial_detail'),
]

urlpatterns += [
    url(r'^serials01/$', views.Serial01Index, name='serial01_list'),
    url(r'^serials01/(?P<serial_id>[-\w]+)$', views.Serial01Detail, name='serial01_detail'),
]

urlpatterns += [
    url(r'^serials02/$', views.Serial02Index, name='serial02_list'),
    url(r'^serials02/(?P<serial_id>[-\w]+)$', views.Serial02Detail, name='serial02_detail'),
]

urlpatterns += [
    url(r'^series/$', views.SeriesListView.as_view(), name='series_list'),
    url(r'^series/(?P<series_id>[-\w]+)$', views.SeriesDetailView, name='series_detail'),
]

# EntryListView is a view, not a viewset. need .as_view()
urlpatterns += [
    url(r'^entries/$', views.EntryListView.as_view(), name='entry_list'),
    url(r'^entries/(?P<pk>\d+)$', views.EntryDetailView.as_view(), name='entry_detail'),
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
