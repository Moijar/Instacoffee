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
                data["powerButton"] = "on"
                print "power on"
                
            elif x == "power_off":
                data["powerButton"] = "off"
                print "power off"
            
            elif x == "start_time_on":
                data["startTimeButton"] = "on"
                print x
            elif x == "start_time_off":
                data["startTimeButton"] = "off"
                print x
                

            elif x == "tweet_switch_on":
                print x
            
            elif x == "tweet_switch_off":
                print x
            else:
                print x
            
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
            
            return HttpResponse (status=200)
            
@csrf_exempt
def backendLoop(request):

    with open('workfile') as data_file:
        data = json.load(data_file)
    
    # Prevent more than one loop
    if data["loopOn"] == "true":
        return HttpResponse (status=200)
    
    while(True):
        time.sleep(2)
        print "backendloop"
        
        # Read the workfile status every second
        with open('workfile') as data_file:
            data = json.load(data_file)
        
        # Prevent more than one loop
        data["loopOn"] = "true"
        # Check pan presence
        sensitivity = 0.1
        # Find out the magnetometer value and determine the presence of the coffee pan accordingly
        while (True):
            ser.flush()
            ser.write('3')
            gauss_str = ser.readline()
            gauss = float(gauss_str)
        
            if -0.1 < gauss < 0.5 and gauss != 0.0:
                break
        
        print gauss
    
        if (gauss > sensitivity):
            data["panPresence"] = "true"
        
        else:
            data["panPresence"] = "false"
        
        if data["powerButton"] == "off":
            ser.flush()
            ser.write('0')
        
        elif data["powerButton"] == "on":
            if data["panPresence"] == "true": # Check that the pan is present before turning on
                ser.write('1')
        
        # Parse the start time from 
        start_time = data["startTime"]
        (start_hour, start_minute) = start_time[:5].split(":")
          
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
             
        # Correct the time zone to Finland, Summer Time
        hour_int = int(current_hour)+3
            
        # Convert hour back to string for comparison
        current_hour = str(hour_int)
        
        if start_hour == current_hour and start_minute == current_minute and data["startTimeButton"] == "on" and data["panPresence"] == "true":
            ser.flush()
            ser.write('1')
            data["powerButton"] = "on"
            
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)

        
        with open('workfile', 'w') as outfile:
            json.dump(data, outfile)
                
@csrf_exempt
def presence(request):
    with open('workfile') as data_file:
        data = json.load(data_file)
        
    presence = data["panPresence"]  
    
    if data["panPresence"] == "true":
        presence = "true"
    else:
        presence = "false"
    
    with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
                
    return HttpResponse(presence)

@csrf_exempt    
def startTime(request):
    print "lol0"
    
    with open('workfile') as data_file:
        data = json.load(data_file)
    
    print "lol1"
    
    if request.GET.has_key('startT'):
        # Parse the start time from 
        x = request.GET['startT']
        start_time = x.replace("start_time: ", "")
        print "lol2"
        # Check that the string is in correct format
        if start_time.find(':') == -1:
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
            return HttpResponse("false", status=200)
        
        print "lol3"
        start_time = x.replace("start_time: ", "")
        
        data["startTime"] = start_time
        
        (start_hour, start_minute) = start_time[:5].split(":")
        
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
             
        # Correct the time zone to Finland, Summer Time
        hour_int = int(current_hour)+3
            
        # Convert hour back to string for comparison
        current_hour = str(hour_int)
        print "lol4"
        if start_hour == current_hour and start_minute == current_minute and data["startTimeButton"] == "on" and data["panPresence"] == "true":
            print "lol5"
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
            return HttpResponse("true", status=200)
           
    with open('workfile', 'w') as outfile:
        json.dump(data, outfile)    
        
    return HttpResponse("false", status=200)
    
@csrf_exempt    
def shutdownTimer(request):
    if request.GET.has_key('shutdownT'):
        # Parse the start time from 
        x = request.GET['shutdownT']
        shutdown_time = x.replace("shutdown_timer: ", "")
        
        # Check that the string is in correct format
        if shutdown_time.find(':') == -1:
            with open('workfile', 'w') as outfile:
                json.dump(data, outfile)
                
            return HttpResponse("false")
        
        (shutdown_hour_str, shutdown_minute_str, shutdown_second_str) = shutdown_time[:8].split(":")
        
        
        
        shutdown_hour = int(shutdown_hour_str)
        shutdown_minute = int(shutdown_minute_str)
        shutdown_second = int(shutdown_second_str)
        
        if shutdown_second > 0:
            shutdown_second = shutdown_second-1
        else:
            if shutdown_minute > 0:
                shutdown_minute = shutdown_minute-1
            else:
                if shutdown_hour > 0:
                    shutdown_hour = shutdown_hour-1
                 
                shutdown_minute = 59
                 
            shutdown_second = 59
        
        if shutdown_hour == 0 and shutdown_minute == 0 and shutdown_second == 0:
            ser.write('0')
            return HttpResponse("true")
        
        shutdown_hour_str = str(shutdown_hour)
        shutdown_minute_str = str(shutdown_minute)
        shutdown_second_str = str(shutdown_second)
        
        print shutdown_hour_str+shutdown_minute_str+shutdown_second_str
        return HttpResponse(shutdown_hour_str+":"+shutdown_minute_str+":"+shutdown_second_str)