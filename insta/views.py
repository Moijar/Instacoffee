from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

import serial

# Liittyy examplee
from django.http import *
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
import socket

ttystring = '/dev/ttyACM0'
ser = serial.Serial(ttystring, 9600)

# Create your views here.
def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
    #return HttpResponse("Hello, wld.")

def hello(request):
    return HttpResponse('Hello World!')

def home(request):
    return render_to_response('index.html', {'variable': 'world'})

def turnon(request):
    if request.POST.has_key('client_response'):
        x = request.POST['client_response']
    ser.write(x)
    return HttpResponse('Ledi vilkkuu 5x')

def main(request):
   return render_to_response('ajaxexample.html', context_instance=RequestContext(request))

def ajax(request):
   if request.POST.has_key('client_response'):
        x = request.POST['client_response']
        y = socket.gethostbyname(x)
        response_dict = {}
        response_dict.update({'server_response': y })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
   else:
        return render_to_response('ajaxexample.html', context_instance=RequestContext(request))
