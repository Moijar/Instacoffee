from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import *
import json
import serial

ttystring = '/dev/ttyACM0'
#ser = serial.Serial(ttystring, 9600)

def index(request):
    # In case of GET-request load the site
    if request.method == 'GET':
        return render_to_response('index.html', {}, context_instance=RequestContext(request))

    # HTTP-Posts are used from Ajax-buttons to control the Arduino
    elif request.method == 'POST':
        if request.POST.has_key('command'):
            x = request.POST['command']
            if x == "power_on":
                print "power on"
                ser.write('0')
            elif x == "power_off":
                print "power off"
                ser.write('1')
            elif x.startswith("start_timer_on"):
                print x
            elif x == "start_timer_off":
                print x
            elif x == "shutdown_timer_on":
                print x
            elif x == "shutdown_timer_off":
                print x
            elif x == "tweet_switch_on":
                print x
            elif x == "tweet_switch_off":
                print x
            else:
                print x
