from django.shortcuts import render

# Create your views here.
import django_filters
from rest_framework import viewsets, filters
from rest_framework import status
from rest_framework.response import Response

from .models import Condition, Entry
from .serializer import ConditionSerializer, EntrySerializer

class ConditionViewSet(viewsets.ModelViewSet):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer  
    #print('message 100')
    
    def create(self, request, *args, **kwargs):
        conditions = request.data
        is_many = isinstance(conditions, list)

        if not is_many:
            #import pdb; pdb.set_trace()
            return super(ConditionViewSet, self).create(request, *args, **kwargs)
        else:
            for condition in conditions:
                serializer = self.get_serializer(data=condition)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(condition)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class EntryViewSet(viewsets.ModelViewSet):
    # https://stackoverflow.com/questions/33866396/django-rest-framework-json-array-post
    # Django REST framework JSON array post
    # https://stackoverflow.com/questions/19253363/named-json-array-in-django-rest-framework
    # Named JSON array in Django REST Framework
    # https://stackoverflow.com/questions/45917656/bulk-create-using-listserializer-of-django-rest-framework
    # bulk create using ListSerializer of Django Rest Framework

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    def create(self, request, *args, **kwargs):
        entries = request.data
        is_many = isinstance(entries, list)
        if not is_many:
            return super(EntryViewSet, self).create(request, *args, **kwargs)
        else:
            for entry in entries:
                serializer = self.get_serializer(data=entry)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(entry)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
    def get_queryset(self):
        return Condition.objects.order_by('-created_at')
 #       return Condition.objects.order_by('-created_at')[:5]

class ConditionDetailView(generic.DetailView):
    model = Condition
#    def get_queryset(self):
#        return Condition.objects.filter(condition.id=pk)

class SerialListView(generic.ListView):
    model = Condition
    template_name = 'meas/serial_list.html'
    def get_queryset(self):
        return Condition.objects.values('serial').distinct()
  
class SerialDetailView(generic.DetailView):
    #model = Condition
    template_name = 'meas/serial_detail.html'
    def get_queryset(self):
        return Condition.objects.filter(serial = pk)         

class SeriesListView(generic.ListView):
    model = Condition
    template_name = 'meas/series_list.html'
    def get_queryset(self):
        return Condition.objects.values('series').distinct()

class SeriesDetailView(generic.DetailView):
    model = Condition
    template_name = 'meas/series_detail.html'
    def get_queryset(self):
#        return Condition.objects.filter(series = self.kwargs.get("series"))
#        return Condition.objects.filter(serial = 'B301')
#        dt = datetime.datetime.strptime(pk, "%y%m%d%H%M%S")
        return Condition.objects.get(series = pk)

# get 1 object, filter multi objects
from django.shortcuts import get_object_or_404
def SerialDetailView(request, pk):
    condition = Condition.objects.filter(serial=pk)
    #condition = get_object_or_404(Condition, serial = pk)
    return render(request, 'meas/serial_detail.html', {'condition': condition})
    


class EntryListView(generic.ListView):
    model = Entry
    paginate_by = 20

class EntryDetailView(generic.DetailView):
    model = Entry