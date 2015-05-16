#!/usr/bin/env python
import os
import sys

default_workfile = '{"loopOn": "false", "powerButton": "off", "startTimeButton": "off", "startTime": "12:00", "shutdownTimer": "01:00", "turnOffTime": "", "tweet": "off", "coffie": "off", "pictureTaken": "false", "panPresence": "false", "coffeeReady": "false", "ready": "false", "readyTime" : "", "consumer_key": "eO96ZowsEhEdmvpioGNBrQxzE", "consumer_secret": "nKPGmuSAVdK9UQV2h1jFcQ0fec4OLOlaDkTWdu8tbVkkKzZYWj","access_token": "1428460136-TSXqHkUqEzaepLpU7orUIwA6lZfyfRmLuurvUDB", "access_token_secret": "r7nk7u1yaFfsSZl8QdABHv9N7KpAi99qZOofVFBvz0CB0"}'
f = open('workfile', 'w')
f.write(default_workfile)
f.close()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instacoffee.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

