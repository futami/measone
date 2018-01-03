# Djangoでファイルアップローダを作る - Qiita
# https://qiita.com/nnsnodnb/items/f7b1b0b7f2099e403947

from django.http import HttpResponseRedirect
#from django.shortcuts import render, redirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.conf import settings
#from upload_form.models import FileNameModel
import sys, os
UPLOADE_DIR = os.path.dirname(os.path.abspath(__file__)) + '/static/files/'

def form(request):
    if request.method != 'POST':
        return render(request, 'meas/upload_form.html')

    file = request.FILES['file']
    path = os.path.join(UPLOADE_DIR, file.name)
    destination = open(path, 'wb')

    for chunk in file.chunks():
        destination.write(chunk)

#    insert_data = FileNameModel(file_name = file.name)
#    insert_data.save()

#    return redirect('meas:upload_complete')
    return HttpResponseRedirect('/meas/upload_complete/')

def complete(request):
    return render(request, 'meas/upload_complete.html')


# def UploadFile(request):