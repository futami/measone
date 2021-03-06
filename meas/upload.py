# Djangoでファイルアップローダを作る - Qiita
# https://qiita.com/nnsnodnb/items/f7b1b0b7f2099e403947

#from django.http import HttpResponseRedirect
#from django.shortcuts import render, redirect
from django.shortcuts import render
#from django.template.context_processors import csrf
#from django.conf import settings
#from upload_form.models import FileNameModel
import sys, os
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'


from .views import ConditionViewSet
from django.test import Client
import json
from .ulid2 import get_ulid_time

def form(request):
    if request.method != 'POST':
        return render(request, 'meas/upload_form.html')

    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

    file = open(path)
    line = file.readline()

    client = Client()
    while line:
        if 'description' in line:
            line = json.loads(line)
            line['created_at'] = get_ulid_time(line['ulid'])
            #import pdb; pdb.set_trace()
            response = client.post('/api/conditions/', line, format='json')
        else:
            line = json.loads(line)
            line['created_at'] = get_ulid_time(line['ulid'])
            response = client.post('/api/entries/', line, format='json')
        line = file.readline()
    
    file.close()

def complete(request):
    return render(request, 'meas/upload_complete.html')


# def UploadFile(request):