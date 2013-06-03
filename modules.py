#I'm just throwing this shit here to make it easier to like check things.
def checkInbox(apihandle):
    messages = apihandle.request("inbox", sort="unread")[u'response'][u'messages']
    print messages
    #already read, don't need to send a new txt
    #variables to make it look pretty c:
    unreadConvId = messages[0][u'convId']
    message = apihandle.request("inbox", type="viewconv", id=unreadConvId)
    username = messages[0][u'username']
    subject = messages[0][u'subject']
    messageId = message[u'response'][u'message'][-1][u'messageId']
    body = message[u'response'][u'messages'][-1][u'body']


    return (username, subject, body, messageId)
