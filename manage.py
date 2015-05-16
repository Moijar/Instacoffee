#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instacoffee.settings")

    from django.core.management import execute_from_command_line
    
    
    execute_from_command_line(sys.argv)
    
    from insta.models import coffeeMaker
    # Set the defaults
    device = coffeeMaker.objects.filter(name='Insta').get()
    device.loopOn = "false"
    device.powerButton = "off"
    device.startTimeButton = "off"
    device.startTime = "12:00"
    device.shutdownTimer = "01:00"
    device.turnOffTime = ""
    device.tweet = "off"
    device.coffie = "off"
    device.pictureTaken = "off"
    device.panPresence = "false"
    device.coffeeReady = "false"
    device.readyTime = ""
    device.consumer_key = "eO96ZowsEhEdmvpioGNBrQxzE" 
    device.consumer_secret = "nKPGmuSAVdK9UQV2h1jFcQ0fec4OLOlaDkTWdu8tbVkkKzZYWj"
    device.access_token = "1428460136-TSXqHkUqEzaepLpU7orUIwA6lZfyfRmLuurvUDB"
    device.access_token_secret = "r7nk7u1yaFfsSZl8QdABHv9N7KpAi99qZOofVFBvz0CB0"



