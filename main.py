import whatapi
from googlevoice import Voice
from modules import checkInbox, extractInput, parseResponse
import time

config = open ('settings.conf', 'r')

settings = config.read().split('\n')
voice = Voice()
voice.login()

#access what.CD API
apihandle = whatapi.WhatAPI(username=settings[0], password=settings[1])



print "Ok, checking your inbox!"
prevId = 0
prevResponse = ''
while True:
    newMessage = checkInbox(apihandle)

    #statements to let user know of new forum threads / etc.
    if prevId != newMessage[3] and settings[0] != newMessage[0]:
        prevId = newMessage[3]
        messageText = "%s - %s\n%s" % newMessage[0:3]

        print "Sending message: ", messageText

        voice.send_sms(settings[2], messageText)

    #Checks for new text messages
    voice.sms()
    response = extractInput(voice.sms.html, settings[2])
    if prevResponse != response:
        print "New text: %s" % response
        prevResponse = response
        resp = parseResponse(response, settings[0], apihandle)
        voice.send_sms(settings[2], resp)

    time.sleep(10)

