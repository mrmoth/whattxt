import whatapi
from googlevoice import Voice

config = open ('settings.conf', 'r')
settings = config.read().split('\n')
voice = Voice()
import time
voice.login()

#access what.CD API
apihandle = whatapi.WhatAPI(username=settings[0], password=settings[1])


def checkInbox():

    messages = apihandle.request("inbox", sort="unread")[u'response'][u'messages']
    if not messages[0][u'unread']:
        return None
    unread_id = messages[0][u'convId']
    message = apihandle.request("inbox", type="viewconv", id=unread_id)
    username = messages[0][u'username']
    subject = messages[0][u'subject']
    body = message[u'response'][u'messages'][-1][u'body']
    return (username, subject, body, unread_id)
print checkInbox()

print "Ok, checking your inbox!"
prevId = 0
while True:
    newMessage = checkInbox()
    if newMessage != None and prevId != newMessage[3]:
        prevId = newMessage[3]
        voice.send_sms(int(settings[2]), "%s - %s\n%s" % newMessage)
    time.sleep(10)
