import time
import RPi.GPIO as io
import requests;
import ConfigParser

#!/usr/bin/python
print("Alarm monitor started")

# load config
config = ConfigParser.ConfigParser()
config.readfp(open(r'config.txt'))
pushoverUser = config.get('pushover', 'user')
pushoverApplication = config.get('pushover','application')

# GPIO configuration
io.setmode(io.BCM) 
door_pin = 23
window_pin = 24
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp
io.setup(window_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

# pushover configuration
def notifyPushover(eventName,pushoverApplication,pushoverUser):
    message = 'Office ' + eventName
    response = requests.post('https://api.pushover.net/1/messages.json',data={'token':pushoverApplication,'user':pushoverUser,'message':message,'title':'Office Alarm'})
    print(response)

# assume the door is open so we don't get a false alarm on startup
doorIsOpen = True;
windowIsOpen = True;

# poll the pins to see if they have changed
while True:
    # check the door
    if io.input(door_pin):
        if not doorIsOpen:
            print("Door Opened")
            notifyPushover("DoorOpened",pushoverApplication,pushoverUser)
        doorIsOpen = True
    else:
        doorIsOpen = False

    # check the window
    if io.input(window_pin):
        if not windowIsOpen:
            print("Window Opened")
            notifyPushover("WindowOpened",pushoverApplication,pushoverUser)
        windowIsOpen = True
    else:
        windowIsOpen = False

    # wait for next poll interval    
    time.sleep(0.5)
