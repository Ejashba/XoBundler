__author__ = 'e.shoichet-bartus'
__version__ = 1.0

"""
Created by Emerson Shoichet-Bartus
Upper Canada College
IB1-IB2 Martlands

Made on PyCharm CE IDE 3.0.2
Edited with PyCharm CE IDE 5.0.1 (latest version)

Alpha testing version
Authenticated for use in ICS3U in UCC

THIS IS TO BE RUN ON AN OLPC/XO (little green computer)
This has currently only been tested on Mac

Comments have been provided for those who wish to learn more about the xo bundling process

Suggestions for improvement are welcome, contact me at e.shoichet-bartus@ucc.on.ca
"""

from os import system #system does terminal (command-line) commands
#I used 'from' because there's no need to import the entire 'os' (Operating System) library

global NewActivityName, ActivityName

system('echo BUNDLING START')  #signal that the program has begun, often good coding practice to give periodic updates to the user

manifestExists = False  #temporary: existence of a MANIFEST in FEDORA 19 is undetermined

while True: #this ensures that the questions are perpetually asked until the user has entered in all the correct information, i.e if the user makes a mistake he/she needn't worry, the questions will repeat themselves so long as he/she doesn't respond with 'y' to the final question
    ActivityName = input("What is the name of the activity you're modifying (with spaces)? ")
    NewActivityName = input("What do you want the new name of your activity to be (with spaces, enter nothing if you don't want to rename your activity)? ")
    if NewActivityName == '\n' or NewActivityName == ' ':
        NewActivityName = ActivityName
    UsbName = input("What is the name of the USB that you're using (including any spaces if applicable)? ")
    if input('Do all three previously entered fields have the correct information (y/n)? ') == 'y':
        break  #if all info entered is correct break out of the loop and move on
    else:
        continue #otherwise if some info is wrong ask all the questions again
        #TODO possible redundancy and/or prolixity

ANNoSpaces = ActivityName.strip().replace(' ', '') #ANNoSpaces means 'Activity Name No Spaces'
activityDirectory = '~/Activities/' + ANNoSpaces + '.activity/' #TODO check filepath validity, & untested
activityInfoFileExt = 'activity/activity.info'  #done so that paths aren't hardcoded; i.e easy to change if filepaths are presently incorrect

system('cd ' + activityDirectory) #get into your activity's directory

if manifestExists:  #I'm not sure yet whether or not the current version of FEDORA in ICS3U uses a MANIFEST (the newest version of FEDORA doesn't but the class may use an older build)
    system("rm MANIFEST && find . -type f | sed 's,^./,,g' > MANIFEST")  #TODO untested

pointerPos, nxtLines = 0, []  #File pointer, start it at the beginning of the file. the file pointer moves relative to character counts
                # e.g. the pointer position of 50 would be 50 characters into the file, not 50 lines or 50 words in
                #Array used to save the lines after the activity number, explained in more detail a little later
                #I used 'unpacking', where you can declare and assign multiple variables in one line using commas

#closes automatically after with statement ends  #must open in 'r+' mode, signifies that reading AND writing permission is granted
#This verbose 'with' statement increments the activity version number by one
with open(activityDirectory + activityInfoFileExt, 'r+') as activityInfoFile:
    lines = activityInfoFile.readlines() #read in all lines from activity.info, normally this is not ideal as it will take a long time to read in large files, but this file is relatively small
    for i in range(len(lines)): #loop that find out which line the activity version number is on
        if lines[i].split()[0] == 'activity_version':
            verLineNum = i  #record the line number of the activity version line in the activity info file, this is
                            #done for compatibility for multiple versions of FEDORA, where this line may be in different places
                            #in the file depending on the version
        else:
            pass #must do this as python only counts a time through the loop if something happens; it counts idling (pass) as something happening

    for i in range(len(lines)): #Loop that increments the activity version by 1, goes through all the lines one by one
        if i < verLineNum:  #If we haven't reached the activity version line yet:
            pointerPos += len(lines[i]) #increment the position of the pointer by the length (in chars) of the line,
                                        # this ensures that when we come to the activity version line we will know where
                                        # to put the pointer, as it is moved from the beginning of the file (not where you'd think it currently is)
        elif i == verLineNum: #If the current line is the activity version one:
            activityInfoFile.seek(pointerPos) #go to the beginning of the activity version line
            linePieces = activityInfoFile.readline().strip().split() #read in the parts of the line as an array
            numDepth = len(linePieces[0]) + 1 + len(linePieces[1]) + 1 #find the depth into the line where the actual version number resides (the '1's indicate spaces)
            activityInfoFile.seek(pointerPos + numDepth)  #put file pointer at activity version number
            ver = int(activityInfoFile.readline().strip())  #read in version number to temporarily save in code
            nxtLines = activityInfoFile.readlines()  #read in all lines after the version line so that they are not lost when they're preliminarily removed from the file
            activityInfoFile.seek(pointerPos + numDepth)  #reset file pointer to right before act ver num
            activityInfoFile.truncate(pointerPos + numDepth)  #delete everything after and including the ver num (truncate = remove)
            activityInfoFile.write(str(ver + 1) + '\n')  #write the new activity ver num, needs to be written as a string (hence the typecasting)
        elif i > verLineNum:  #If we're beyond the activity version line:
            activityInfoFile.write(nxtLines[i-(verLineNum+1)]) #write first, second, third, etc. line after activity ver line
            #this puts the removed lines back into the file, thus reconstructing it

system('chmod a+x setup.py && chmod a+x activity.py')  #TODO untested
while True:
    if input("Type in 'ready' once you've run part 2 on a mac and have your zipped activity on a usb in your OLPC... ") == 'ready' and input("Are you sure you're ready to proceed? (yes/no) ") == 'yes':
        system('cd /media/ && mv ' + NewActivityName.strip().replace(' ', '') + '.xo ' + activityDirectory)
        break
    else:
        continue #continue makes program go back to beginning of loop, and ignores code after conditional but still in loop
                 #Okay here because there is no code in loop after conditional
        #TODO untested

system('echo BUNDLING COMPLETE') #inform the user of the program's completion and termination