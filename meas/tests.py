from django.test import TestCase

# http://nwpct1.hatenablog.com/entry/how-to-write-unittest-on-django
# Create your tests here.

from django.core.urlresolvers import resolve
from meas.views import ConditionListView, ConditionDetailView
from meas.views import EntryListView, EntryDetailView
from meas.views import SerialListView, SerialDetailView
from meas.views import SeriesListView, SeriesDetailView

class UrlResolveTests(TestCase):
    def test_condition_list_view(self):
        found = resolve('/meas/conditions/')
        self.assertEqual(found.func.__name__, ConditionListView.as_view().__name__)

    def test_condition_detail_view(self):
        found = resolve('/meas/conditions/1')
        self.assertEqual(found.func.__name__, ConditionDetailView.as_view().__name__)

    def test_entry_list_view(self):
        found = resolve('/meas/entries/')
        self.assertEqual(found.func.__name__, EntryListView.as_view().__name__)

    def test_serial_list_view(self):
        found = resolve('/meas/serials/')
        self.assertEqual(found.func.__name__, SerialListView.as_view().__name__)

    def test_series_list_view(self):
        found = resolve('/meas/series/')
        self.assertEqual(found.func.__name__, SeriesListView.as_view().__name__)

# https://qiita.com/hys/items/19a03aaac87a93e0d539
# Djangoでfactory_boyを使ってテストをする２

from django.http import HttpRequest
from django.template.loader import render_to_string
from meas.views import ConditionListView

class HtmlTests(TestCase):
    def a_test_condition_list_reqest_html(self):
        request = HttpRequest()
        response = ConditionListView(request)
        expected_html = render_to_string('meas/condition_list.html', {'books': []})
        self.assertEqual(response.content.decode(), expected_html)

# http://www.django-rest-framework.org/api-guide/testing/
# Testing

from rest_framework.test import APIRequestFactory

# Using the standard RequestFactory API to create a form POST request
factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'})



from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from meas.models import Condition, Entry

class ConditionAPITests(APITestCase):
    def test_create_condition(self):
        """
        Ensure we can create a new account object.
        """
#        url = reverse('condition-list')
        data = {
            "description": "B301_test L0 Nothing",
            "condition": "L0",
            "serial": "B301",
            "lane": "0",
            "series": "20171111085905",
            "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
        }
        response = self.client.post('/api/conditions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Condition.objects.count(), 1)
        self.assertEqual(Condition.objects.get().serial, 'B301')
        self.assertEqual(Condition.objects.get().series, '20171111085905')

    def test_create_entry(self):
        data = {
            "description": "B301_test L0 Nothing",
            "condition": "L0",
            "serial": "B301",
            "lane": "0",
            "series": "20171111085905",
            "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
        }
        response = self.client.post('/api/conditions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = {
            "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
            "item": "SNR",
            "value": "6.94",
            "unit": "dB",
        }
        response = self.client.post('/api/entries/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entry.objects.count(), 1)


#        response = self.client.get('/users/4/')
#        self.assertEqual(response.data, {'id': 4, 'username': 'lauren'})

#        response = self.client.get('/users/4/')
#        self.assertEqual(json.loads(response.content), {'id': 4, 'username': 'lauren'})

#        view = UserDetail.as_view()
#        request = factory.get('/users/4')
#        response = view(request, pk='4')
#        response.render()  # Cannot access `response.content` without this.
#        self.assertEqual(response.content, '{"username": "lauren", "id": 4}')

#class SmokeTest(TestCase):
#    def test_bad_maths(self):
#        self.assertEqual(1+1, 3)  # 失敗