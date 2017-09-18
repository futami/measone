from django.shortcuts import render

# Create your views here.
import django_filters
from rest_framework import viewsets, filters

from .models import Condition, Entry
from .serializer import ConditionSerializer, EntrySerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer   

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

from django.views import generic
class ConditionListView(generic.ListView):
    model = Condition
    paginate_by = 20

# はじめての Django アプリ作成、その 3 | Django documentation | Django 
# https://docs.djangoproject.com/ja/1.11/intro/tutorial03/
from django.http import HttpResponse
def index(request):
    latest_condition_list = Condition.objects.order_by('-created_at')
    output = ', '.join([c.description for c in latest_condition_list])
    return HttpResponse(output)
    
# はじめての Django アプリ作成、その 4 | Django documentation | Django 
# https://docs.djangoproject.com/ja/1.11/intro/tutorial04/


