from modules import stripHtmlTags
#this will be more fleshed out later
def checkInbox(apihandle):
    messages = apihandle.request("inbox", sort="unread")[u'response'][u'messages']
    #already read, don't need to send a new txt
    #variables to make it look pretty c:
    unreadConvId = messages[0][u'convId']
    message = apihandle.request("inbox", type="viewconv", id=unreadConvId)[u'response'][u'messages']
    username = message[-1][u'senderName']
    subject = messages[0][u'subject']
    messageId = message[-1][u'messageId']
    body = message[-1][u'body']
    return (username, subject, stripHtmlTags(body), messageId)

