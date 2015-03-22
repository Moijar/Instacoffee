from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import *
import json
import serial

ttystring = '/dev/ttyACM0'
ser = serial.Serial(ttystring, 9600)

# Create your views here.
def index(request):
    # In case of GET-request load the site
    if request.method == 'GET':
        return render_to_response('index.html', {}, context_instance=RequestContext(request))

    # HTTP-Posts are used from Ajax-buttons to control the Arduino
    elif request.method == 'POST':
        if request.POST.has_key('client_response'):
            x = request.POST['client_response']
            ser.write(x)