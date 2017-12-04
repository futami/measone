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

from django.test import Client
def create_condition_data():
    client = Client()
    data = {
        "description": "B301_test L0 Nothing",
        "condition": "L0",
        "serial": "B301",
        "lane": "0",
        "series": "20171111085905",
        "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
    }
    response = client.post('/api/conditions/', data, format='json')
    
def create_condition_and_entry_data():
    client = Client()
    data = {
        "description": "B301_test L0 Nothing",
        "condition": "L0",
        "serial": "B301",
        "lane": "0",
        "series": "20171111085905",
        "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
    }
    response = client.post('/api/conditions/', data, format='json')
    data = {
        "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
        "item": "SNR",
        "value": "6.94",
        "unit": "dB",
    }
    response = client.post('/api/entries/', data, format='json')


class HtmlTests(TestCase):
    def sample_test_condition_list_reqest_html(self):
        request = HttpRequest()
        response = ConditionListView(request)
        expected_html = render_to_string('meas/condition_list.html', {'books': []})
        self.assertEqual(response.content.decode(), expected_html)

    def test_condition_list_request_html(self):
        response = self.client.get('/meas/conditions/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/condition_list.html')
        #print(response['Content-Type'])         # text/html; charset=utf-8
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        #print(response.content)         # raw html
        self.assertContains(response, 'There are no condition in the library.')
        self.assertNotContains(response, 'description')
        #self.assertNotContains(response, 'condition')
        self.assertNotContains(response, 'series')
        self.assertNotContains(response, 'uuid')
        #print(response.context) # context is a variable name for django template 

        create_condition_data()

        response = self.client.get('/meas/conditions/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertContains(response, 'description', count=1)
        #self.assertContains(response, 'condition')
        self.assertContains(response, 'series', count=1)
        self.assertContains(response, 'uuid', count=1)
        #print(response.context['series']) # django template context
    
    def test_condition_detail_request_html(self):
        create_condition_data()

        response = self.client.get('/meas/conditions/1')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/condition_detail.html')
        #print(response.content)
        #print(response.context)

    #
    # Entry
    #
    def atest_entry_list_request_html(self):
        response = self.client.get('/meas/entries/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/entry_list.html')

    #
    # Serial
    #
    def test_serial_list_request_html(self):
        response = self.client.get('/meas/serials/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/serial_list.html')
        #print(response.content)
        self.assertNotContains(response, 'description')

        create_condition_and_entry_data()

        response = self.client.get('/meas/serials/')
        self.failUnlessEqual(response.status_code, 200)
        #print(response.content)
        self.assertContains(response, 'B301')
        self.assertQuerysetEqual(response.context['condition_list'], ["{'serial': 'B301'}"])

    
    def test_serial_detail_request_html(self):
        response = self.client.get('/meas/serials/B301')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/serial_detail.html')
        self.assertNotContains(response, 'description')
        #print(response.content)

        create_condition_and_entry_data()

        response = self.client.get('/meas/serials/B301')
        self.failUnlessEqual(response.status_code, 200)
        #print(response.content)
        self.assertContains(response, 'description', count=1)
        self.assertQuerysetEqual(response.context['condition'], ['<Condition: Condition object>'])
        self.assertEqual(response.context['condition'].count, 1)

    #
    # Series
    #
    def test_series_list_request_html(self):
        response = self.client.get('/meas/series/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/series_list.html')
    
    def atest_series_detail_request_html(self):
        response = self.client.get('/meas/series/20171111085905')
        self.failUnlessEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meas/series_detail.html')

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

    def test_create_multi_conditions(self):
        """
        Ensure we can create a new account object.
        """
#        url = reverse('condition-list')
        data = [{
            "description": "B301_test L0 Nothing",
            "condition": "L0",
            "serial": "B301",
            "lane": "0",
            "series": "20171111085905",
            "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
        },
        {
            "description": "B315_test",
            "condition": "L3",
            "serial": "B315",
            "lane": "4",
            "series": "20171109141055",
            "uuid": "685E790C-3E15-4882-A81F-917097FEFEDD",
        }
        ]
        response = self.client.post('/api/conditions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Condition.objects.count(), 2)
        #self.assertEqual(Condition.objects.get().serial, 'B301')
        #self.assertEqual(Condition.objects.get().series, '20171111085905')

class EntryAPITests(APITestCase):
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

    def test_create_multi_entries(self):
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

        data = [{
            "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
            "item": "SNR",
            "value": "6.94",
            "unit": "dB",
        },
        {
            "uuid": "1990e31b-928c-4619-9c64-acd882a416d9",
            "item": "Vcc_PSU",
            "value": "3.698",
            "unit": "V"
        }]

        response = self.client.post('/api/entries/', data, format='json')
        self.assertEqual(Entry.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        #self.assertEqual(Entry.objects.count(), 1)


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