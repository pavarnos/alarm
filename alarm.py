import time
import RPi.GPIO as io
import requests;

# GPIO configuration
io.setmode(io.BCM) 
door_pin = 23
window_pin = 22
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp
io.setup(window_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

# ifttt configuration
iftttBaseUrl = 'https://maker.ifttt.com/trigger/'
iftttToken = '/with/key/dja7APuAMVvDhA1UZTway-'
doorOpenUrl = iftttBaseUrl + 'DoorOpened' + iftttToken
windowOpenUrl = iftttBaseUrl + 'WindowOpened' + iftttToken

# assume the door is open so we don't get a false alarm on startup
doorIsOpen = True;
windowIsOpen = True;

# poll the pins to see if they have changed
while True:
    # check the door
    if io.input(door_pin):
        if not doorIsOpen:
            print("Door Opened")
            response = requests.get(doorOpenUrl)
            print(response.text)
        doorIsOpen = True
    else:
        doorIsOpen = False

    # check the window
    if io.input(window_pin):
        if not windowIsOpen:
            print("Window Opened")
            response = requests.get(windowOpenUrl)
            print(response.text)
        windowIsOpen = True
    else:
        windowIsOpen = False

    # wait for next poll interval    
    time.sleep(0.5)
