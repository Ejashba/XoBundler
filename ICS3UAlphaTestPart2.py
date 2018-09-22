__author__ = 'e.shoichet-bartus'
__version__ = 1.0

"""
Created by Emerson Shoichet-Bartus
Upper Canada College
IB1-IB2 Martlands

Made on PyCharm CE IDE 3.0.2
Edited with PyCharm CE IDE 5.0.1 (latest version)

Alpha testing version
Authenticated for use in ICS3U

THIS IS TO BE RUN ON A MAC following the execution of the first portion of part 1 on an olpc
This has currently only been tested on Mac

Comments have been provided for those who wish to learn more about the xo bundling process

Suggestions for improvement are welcome; contact me at e.shoichet-bartus@ucc.on.ca
"""

from os import system #system does terminal (console) commands

while 1+1 == 2: #infinite loop until user indicates that all fields have the correct information
    usbName = input('What is the name of your usb (without spaces)? ')
    oldActName = input("What is the name of the activity you're modifying (also without spaces)? ")
    newActName = input('What would you like the new name of your activity to be (press enter if you wish it to be the '
                + 'same as the old activity name)? ')
    if input('Do all three fields have the correct information (y/n)? ') == 'y':
        break
    else:
        continue

if newActName == '\n': #If the user chose not to make a new activity name and stick with the old one (\n means a blank newline, it's what you get when you press enter):
    newActName = oldActName #make the new name the old name
system('cd /Volumes/' + usbName + ' && zip -r ' + newActName + '.xo ./' + oldActName + '.activity') #TODO untested
# Cd (change directory) to the USB and then zip the new activity as an xo