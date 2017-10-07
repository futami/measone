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
# genericを使ったListViewは <app>/<model>_list.html というdefaultのtemplateを使う
# template_name で指定できる
# ListViewは、自動的に生成されるコンテキスト変数は <model>_list になります。
# context_object_name 属性を与えると指定できる 
from django.views import generic
class ConditionListView(generic.ListView):
#    template_name = 'app_name/index.html'
#    context_object_name = 'latest_question_list'
    model = Condition
#    def get_queryset(self):
#        """Return the last five published questions."""
#        return Condition.objects.order_by('-created_at')[:5]

class ConditionDetailView(generic.DetailView):
    model = Condition
#    def get_queryset(self):
#        return Condition.objects.filter(condition.id=pk)

