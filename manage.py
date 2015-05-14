#!/usr/bin/env python
import os
import sys

default_workfile = '{"loopOn": "false", "powerButton": "off", "startTimeButton": "off", "startTime": "12:00", "shutdownTimer": "01:00", "turnOffTime": "", "tweet": "off", "coffie": "off", "panPresence": "false", "coffeeReady": "false", "ready": "false", "readyTime" : ""}'
f = open('workfile', 'w')
f.write(default_workfile)
f.close()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "instacoffee.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

