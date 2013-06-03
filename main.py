import whatapi
from googlevoice import Voice
from modules import checkInbox, extractInput
import time

config = open ('settings.conf', 'r')

if len(settings[2]) != 12:
       print "You need to add the country number thing\n(+1 in front of your number or something similar)"
settings = config.read().split('\n')
voice = Voice()
voice.login()

#access what.CD API
apihandle = whatapi.WhatAPI(username=settings[0], password=settings[1])



print "Ok, checking your inbox!"
prevId = 0
while True:
    newMessage = checkInbox(apihandle)
    if prevId != newMessage[3] and settings[0] != newMessage[0]:
        prevId = newMessage[3]
        messageText = "%s - %s\n%s" % newMessage[0:3]

        print "Sending message: ", messageText

        voice.send_sms(settings[2], messageText)

    time.sleep(10)


