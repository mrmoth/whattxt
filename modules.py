#I'm just throwing this shit here to make it easier to like check things.
def checkInbox(apihandle):
    messages = apihandle.request("inbox", sort="unread")[u'response'][u'messages']
    print messages
    #already read, don't need to send a new txt
    if not messages[0][u'unread']:
        return None

    #variables to make it look pretty c:
    unread_id = messages[0][u'convId']
    message = apihandle.request("inbox", type="viewconv", id=unread_id)
    username = messages[0][u'username']
    subject = messages[0][u'subject']
    body = message[u'response'][u'messages'][-1][u'body']

    return (username, subject, body, unread_id)
