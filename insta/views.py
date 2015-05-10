from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import *
from django.views.decorators.csrf import csrf_exempt

import json
import serial
import datetime
import time
import json

ttystring = '/dev/ttyACM0'
ser = serial.Serial(ttystring, 9600)

@csrf_exempt
def index(request):
    with open('workfile') as data_file:
        data = json.load(data_file)
    
    print data["startTime"]
    # In case of GET-request load the site
    if request.method == 'GET':
        return render_to_response('index.html', {}, context_instance=RequestContext(request))

    # HTTP-Posts are used from Ajax-buttons to control the Arduino. The template is sending POST-requests to the view at least once every second, so this is also used as the loop function.
    elif request.method == 'POST':
        if request.POST.has_key('command'):
            x = request.POST['command']
            
            if x == "power_on":
                if data["panPresence"] == "true": # Check that the pan is present before turning on
                    ser.write('1')
                    print "power on"
                    
                    
            elif x == "power_off":
                ser.write('0')
                print "power off"
            
            elif x == "start_time_on":
                data["startTime"] = "on"
                print x
            elif x == "start_time_off":
                data["startTime"] = "off"
                print x
            elif x.startswith("start_time:"):
                print x
                
                # Parse the start time from 
                start_time = x.replace("start_time: ", "")
                (start_hour, start_minute) = start_time[:5].split(":")
                
                # Find out the current time
                now = datetime.datetime.now()
                current_hour = now.strftime("%H")
                current_minute = now.strftime("%M")
                
                # Correct the time zone to Finland, Summer Time
                hour_int = int(current_hour)+3
                
                # Convert hour back to string for comparison
                current_hour = str(hour_int)
                
                # Compare the current time to start time. If it matches, turn the coffee maker on
                if start_hour == current_hour and start_minute == current_minute and data["startTime"] == "on" and data["panPresence"] == "true":
                    ser.write('1')

            elif x == "shutdown_timer:":
                print x
            
            elif x == "shutdown_timer_off":
                print x
            
            elif x == "tweet_switch_on":
                print x
            
            elif x == "tweet_switch_off":
                print x
            else:
                print x
            
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
                
@csrf_exempt
def presence(request):
    with open('workfile') as data_file:
        data = json.load(data_file)
        
    presence = data["panPresence"]
    sensitivity = 0.1
    # Find out the magnetometer value and determine the presence of the coffee pan accordingly
    while (True):
        ser.flush()
        ser.write('3')
        gauss_str = ser.readline()
        gauss = float(gauss_str)
        
        if -0.1 < gauss < 0.5:
            break
    
    print gauss
    
    if (gauss > sensitivity):
        presence = "true"
        data["panPresence"] = "true"
    else:
        presence = "false"
        data["panPresence"] = "false"
    
    with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
                
    return HttpResponse(presence)

@csrf_exempt    
def startTime(request):
    
    with open('workfile') as data_file:
        data = json.load(data_file)
    
    if request.GET.has_key('startT'):
        # Parse the start time from 
        x = request.GET['startT']
        start_time = x.replace("start_time: ", "")
        
        # Check that the string is in correct format
        if start_time.find(':') == -1:
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
                
            return HttpResponse("false")
        
        (start_hour, start_minute) = start_time[:5].split(":")
                
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
                
       # Correct the time zone to Finland, Summer Time
        hour_int = int(current_hour)+3
                
       # Convert hour back to string for comparison
        current_hour = str(hour_int)
                
        # Compare the current time to start time. If it matches, turn the coffee maker on
        
        print start_hour + ":" + start_minute
        
        if start_hour == current_hour and start_minute == current_minute and data["startTime"] == "on" and data["panPresence"] == "true":
            ser.flush()
            ser.write('1')
            
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
                
            return HttpResponse("true")
        
        with open('workfile', 'w') as outfile:
            json.dump(data, outfile)    
                
    return HttpResponse("false")