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
                
                # Shutdown timer
        
                shutdown_time = data["shutdownTimer"]
                (shutdown_hour_str, shutdown_minute_str) = shutdown_time[:8].split(":")

                shutdown_hour = int(shutdown_hour_str)
                shutdown_minute = int(shutdown_minute_str)
                
                
                # Find out the current time
                now = datetime.datetime.now()
                current_hour = now.strftime("%H")
                current_minute = now.strftime("%M")

                # Correct the time zone to Finland, Summer Time
                current_hour_int = int(current_hour)+3
                
                # Cast minutes to int
                current_minute_int = int(current_minute)
                
                
                # Calculate the turn off hour
                turnOff_minute = current_minute_int + shutdown_minute
                turnOff_hour = current_hour_int + shutdown_hour
                
                if turnOff_minute >= 60:
                    turnOff_minute = turnOff_minute - 60
                    turnOff_hour = turnOff_hour + 1
         
                if turnOff_hour >= 24:
                    turnOff_hour = turnOff_hour - 24
            
                turnOff_hour_str = str(turnOff_hour)
                turnOff_minute_str = str(turnOff_minute)
                
                data["turnOffTime"] = turnOff_hour_str + ":" + turnOff_minute_str
                
                
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
        
        # Read the workfile status every second
        with open('workfile') as data_file:
            data = json.load(data_file)
                
        # Prevent more than one loop
        #data["loopOn"] = "true"
        # Check pan presence
        gauss_sensitivity = 0.1
        # Find out the magnetometer value and determine the presence of the coffee pan accordingly
        while (True):
            ser.write('3')
            gauss_str = ser.readline()
            gauss = float(gauss_str)
            if -0.5 < gauss < 0.5 and gauss != 0.0:
                break
    
        if (gauss > gauss_sensitivity):
            data["panPresence"] = "true"
        
        else:
            data["panPresence"] = "false"
        
        # Parse the start time from 
        start_time = data["startTime"]
        (start_hour, start_minute) = start_time[:5].split(":")
          
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
             
        # Correct the time zone to Finland, Summer Time
        hour_int = int(current_hour)+3        
        
        smaller = False
        
        if hour_int < 10:
            smaller = True
            
        # Convert hour back to string for comparison
        current_hour = str(hour_int)
        
        if smaller:
            current_hour = "0" + current_hour
        
        # Check if the time is the same as with turnOffTime
        if data["turnOffTime"] == current_hour + ":" + current_minute:
            ser.flush()
            ser.write('0')
            data["powerButton"] = "off"
        
        # Shutdown timer
        shutdown_time = data["shutdownTimer"]
        (shutdown_hour_str, shutdown_minute_str) = shutdown_time[:8].split(":")

        shutdown_hour = int(shutdown_hour_str)
        shutdown_minute = int(shutdown_minute_str)
        
        current_hour_int = int(current_hour) 
        current_minute_int = int(current_minute) 
        
        
        # Start time
        if start_hour == current_hour and start_minute == current_minute and data["startTimeButton"] == "on" and data["panPresence"] == "true":
            ser.flush()
            ser.write('1')
            data["powerButton"] = "on"
            
            # Set the time for turning the coffee maker off
            
            turnOff_minute = current_minute_int + shutdown_minute
            turnOff_hour = current_hour_int + shutdown_hour
            if turnOff_minute >= 60:
                turnOff_minute = turnOff_minute - 60
                turnOff_hour = turnOff_hour + 1
         
            if turnOff_hour >= 24:
                turnOff_hour = turnOff_hour - 24
            
            turnOff_hour_str = str(turnOff_hour)
            turnOff_minute_str = str(turnOff_minute)
        
            data["turnOffTime"] = turnOff_hour_str + ":" + turnOff_minute_str
           
        # Power button off
        if data["powerButton"] == "off":
            data["coffeeReady"] = "false"
            data["readyTime"] = ""
            ser.flush()
            ser.write('0')
        
        # Power button on
        elif data["powerButton"] == "on":
            if data["panPresence"] == "true": # Check that the pan is present before turning on
                ser.flush()
                ser.write('1')
                
                # Determine the time when coffee will be ready
                distance_sensitivity = 10
                minutesToReady = 0
        
                values = []
                while len(values) < 10:
                    ser.write('4')
                    distance_str = ser.readline()
                    distance = float(distance_str)
                    values.append(distance)
                        
                # Calculate the average of 10 distance values
                average = sum(values)/float(len(values))
        
                if average > distance_sensitivity and data["readyTime"] == "":
                    ready_minute = current_minute_int + minutesToReady
                    ready_hour = current_hour_int
            
                    if ready_minute >= 60:
                        ready_minute = ready_minute - 60
                        ready_hour = ready_hour + 1
         
                    if ready_hour >= 24:
                        ready_hour = ready_hour - 24
            
                    ready_hour_str = str(ready_hour)
                    ready_minute_str = str(ready_minute)
        
                    if int(ready_hour_str) < 10:
                        ready_hour_str = "0" + ready_hour_str
                    
                    if int(ready_minute_str) < 10:
                        ready_minute_str = "0" + ready_minute_str
                        
                    data["readyTime"] = ready_hour_str + ":" + ready_minute_str
        
        # Check if the coffee is ready now
        if data["readyTime"] == current_hour + ":" + current_minute and data["coffeeReady"] == "false":
            data["coffeeReady"] = "true"
            print "yes ready"
        
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
                
    return HttpResponse(presence, status=200)

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
            return HttpResponse("false", status=200)
        
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
        
        if start_hour == current_hour and start_minute == current_minute and data["startTimeButton"] == "on" and data["panPresence"] == "true":
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
            return HttpResponse("false")
        
        with open('workfile') as data_file:
            data = json.load(data_file)
        
        data["shutdownTimer"] = shutdown_time
        
        with open('workfile', 'w') as outfile:
            json.dump(data, outfile)
            
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
             
        # Correct the time zone to Finland, Summer Time
        hour_int = int(current_hour)+3
        
        smaller = False
        
        if hour_int < 10:
            smaller = True
            
        # Convert hour back to string for comparison
        current_hour = str(hour_int)
        if data["turnOffTime"] == current_hour + ":" + current_minute:
            return HttpResponse("true")
        
        return HttpResponse(status=200)

@csrf_exempt        
def ready(request):
    with open('workfile') as data_file:
        data = json.load(data_file)

    return HttpResponse(data["coffeeReady"], status=200)