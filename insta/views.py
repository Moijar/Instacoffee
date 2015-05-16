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
import tweepy
from subprocess import call
from insta.models import coffeeMaker

ttystring = '/dev/ttyACM0'
ser = serial.Serial(ttystring, 9600)

@csrf_exempt
def index(request):
    # In case of GET-request load the site
    if request.method == 'GET':
        device = coffeeMaker.objects.filter(name='Insta').get()
        
        return render_to_response('index.html', {"powerButton": device.powerButton, "startTimeButton": device.startTimeButton, "startTime": device.startTime, "shutdownTimer": device.shutdownTimer, "tweet": device.tweet, "coffie": device.coffie, "panPresence": device.panPresence, "coffeeReady": device.coffeeReady}, context_instance=RequestContext(request))

    # HTTP-Posts are used from Ajax-buttons to control the Arduino. The template is sending POST-requests to the view at least once every second, so this is also used as the loop function.
    elif request.method == 'POST':
        if request.POST.has_key('command'):
            x = request.POST['command']
            device = coffeeMaker.objects.filter(name='Insta').get()
            
            if x == "power_on":
                device.powerButton = "on"
                print "power on"
                
                # Shutdown timer
        
                shutdown_time = device.shutdownTimer
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
        
                smaller = False
        
                if turnOff_minute < 10:
                    turnOff_minute_str = "0" + turnOff_minute_str
                
                if turnOff_hour < 10:
                    turnOff_hour_str = "0" + turnOff_hour_str
                
                device.turnOffTime = turnOff_hour_str + ":" + turnOff_minute_str
                
                
            elif x == "power_off":
                device.powerButton = "off"
                print "power off"
            
            elif x == "start_time_on":
                device.startTimeButton = "on"
                print x
            elif x == "start_time_off":
                device.startTimeButton = "off"
                print x
                

            elif x == "tweet_switch_on":
                device.tweet = "on"
                print x
            
            elif x == "tweet_switch_off":
                device.tweet = "off"
                print x
                
            elif x == "coffie_switch_on":
                device.coffie = "on"
                print x
            
            elif x == "tweet_switch_off":
                device.coffie = "off"
                print x    
            else:
                print x
            
            device.save()
            
            return HttpResponse (status=200)
            
@csrf_exempt
def backendLoop(request):
    device = coffeeMaker.objects.filter(name='Insta').get()

    # Prevent more than one loop
    if device.loopOn == "true":
        return HttpResponse (status=200)
    
    time.sleep(2)
    while(True):
        time.sleep(1)
        device = coffeeMaker.objects.filter(name='Insta').get() 
        
        # Prevent more than one loop
        device.loopOn = "true"
        # Check pan presence
        gauss_sensitivity = 0.1
        # Find out the magnetometer value and determine the presence of the coffee pan accordingly
        while (True):
            ser.flush()
            ser.write('3')
            gauss_str = ser.readline()
            gauss = float(gauss_str)
            if -0.5 < gauss < 2.0 and gauss != 0.0:
                break
        
        if (gauss > gauss_sensitivity):
            device.panPresence = "true"
            
            # The pan needs to be returned back to its position to take new picture
            device.pictureTaken = "false"
            
        else:
            
            device.panPresence = "false"
            # If pan is taken from its place and coffee is ready, take a picture and post it to twitter
            if device.coffie == "on" and device.coffeeReady == "true" and device.pictureTaken == "false":
                cmd = 'raspistill -t 500 -w 1024 -h 768 -o pic.jpg'
                call ([cmd], shell=True)         #shoot the photo
                photo_path = "pic.jpg"
                status = "Join them for coffee! :)" + current_hour + ":" + current_minute + " " + current_day + "." + current_month + "." + current_year
                auth = tweepy.OAuthHandler(device.consumer_key, device.consumer_secret)
                auth.set_access_token(device.access_token, device.access_token_secret)
                api = tweepy.API(auth)
                api.update_with_media(photo_path, status=status)           
                device.pictureTaken = "true"
            
        # Parse the start time from 
        start_time = device.startTime
        (start_hour, start_minute) = start_time[:5].split(":")
        
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
        current_year = now.strftime("%Y")
        current_day = now.strftime("%d")
        current_month = now.strftime("%m")
        
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
        if device.turnOffTime == current_hour + ":" + current_minute:
            ser.flush()
            ser.write('0')
            device.powerButton = "off"
        
        # Shutdown timer
        shutdown_time = device.shutdownTimer
        (shutdown_hour_str, shutdown_minute_str) = shutdown_time[:8].split(":")

        shutdown_hour = int(shutdown_hour_str)
        shutdown_minute = int(shutdown_minute_str)
        
        current_hour_int = int(current_hour) 
        current_minute_int = int(current_minute) 
        
        # Start time
        if start_hour == current_hour and start_minute == current_minute and device.startTimeButton == "on" and device.panPresence == "true":
            ser.flush()
            ser.write('1')
            device.powerButton = "on"
            
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
        
            device.turnOffTime = turnOff_hour_str + ":" + turnOff_minute_str
         
        # Power button off
        if device.powerButton == "off":
            device.coffeeReady = "false"
            device.readyTime = ""
            ser.flush()
            ser.write('0')
        
        # Power button on
        elif device.powerButton == "on":
            if device.panPresence == "true": # Check that the pan is present before turning on
                ser.flush()
                ser.write('1')
                
                # Determine the time when coffee will be ready
                distance_sensitivity = 9
                minutesToReady = 0
        
                values = []
                
                while len(values) < 10:
                    ser.flush()
                    ser.write('4')
                    distance_str = ser.readline()
                    distance = float(distance_str)
                    if (5 < distance):
                        values.append(distance)
                        
                # Calculate the average of 10 distance values
                average = sum(values)/float(len(values))
                print values
                print "average: " + str(average)
                
                if average > distance_sensitivity and device.readyTime == "":
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
                        
                    device.readyTime = ready_hour_str + ":" + ready_minute_str
        
        # Check if the coffee is ready now
        if device.readyTime == current_hour + ":" + current_minute and device.coffeeReady == "false":
            device.coffeeReady = "true"
            print "yes ready"
            
            if  device.tweet == "on":
                print "TWITTERED 1"
                auth = tweepy.OAuthHandler(device.consumer_key, device.consumer_secret)
                auth.set_access_token(device.access_token, device.access_token_secret)
                api = tweepy.API(auth)
                api.update_status(status = "Coffee is ready on! Join me for a hot cup! :) " + current_hour + ":" + current_minute + " " + current_day + "." + current_month + "." + current_year)
                print "TWITTERED! 2"
        
        device.save()
        
@csrf_exempt
def presence(request):
    device = coffeeMaker.objects.filter(name='Insta').get()
    return HttpResponse(device.panPresence, status=200)

@csrf_exempt    
def startTime(request):  
    device = coffeeMaker.objects.filter(name='Insta').get()

    if request.GET.has_key('startT'):
        # Parse the start time from 
        x = request.GET['startT']
        start_time = x.replace("start_time: ", "")

        # Check that the string is in correct format
        if start_time.find(':') == -1:
            return HttpResponse("false", status=200)
        
        start_time = x.replace("start_time: ", "")
        
        device.startTime = start_time
        
        (start_hour, start_minute) = start_time[:5].split(":")
        
        # Find out the current time
        now = datetime.datetime.now()
        current_hour = now.strftime("%H")
        current_minute = now.strftime("%M")
             
        # Correct the time zone to Finland, Summer Time
        hour_int = int(current_hour)+3
            
        # Convert hour back to string for comparison
        current_hour = str(hour_int)
        
        if start_hour == current_hour and start_minute == current_minute and device.startTimeButton == "on" and device.panPresence == "true":
            device.save()
            return HttpResponse("true", status=200)
           
    device.save()   
        
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
        
        device = coffeeMaker.objects.filter(name='Insta').get()
        
        device.shutdownTimer = shutdown_time
        
        device.save()
            
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
        if device.turnOffTime == current_hour + ":" + current_minute:
            return HttpResponse("true")
        
        return HttpResponse(status=200)

@csrf_exempt        
def ready(request):
    device = coffeeMaker.objects.filter(name='Insta').get()
    return HttpResponse(device.coffeeReady, status=200)