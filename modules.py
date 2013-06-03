import BeautifulSoup

#I'm just throwing this shit here to make it easier to like check things.
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


    return (username, subject, body, messageId)

#This shit was taken from the documentation.
def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []                                       # accum message items here
    #   Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)         # parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #   For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :                               # for all rows
            #   For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}       # tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :                         # for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()   # put text in dict
            msgitems.append(msgitem)                    # add msg dictionary to list
    return msgitems

def extractInput(htmlsms, number):
    messages = []
    for msg in extractsms(htmlsms):
        if number in msg[u'from']:
            messages.append(msg)
    #only interested in latest message.
    return messages[-1][u'text']

def parseResponse(response, apihandle):
    response = response.split(' ')
    if 'top' in response[0]:
        return topTen(apihandle, response[1])
    return "Not sure what that meant. Try again bud."

def topTen(apihandle, period):
    top = apihandle.request('top10')
    index = 0
    if 'week' in period:
        index = 1
    elif 'all' in period:
        index = 2
    elif 'year' in period:
        index = 3

    text = top[u'response'][index][u'caption']+"\n"
    torrents = top[u'response'][index][u'results']
    for bands in torrents:
        text += "%s - %s\n" % (bands[u'groupName'], bands[u'artist'])
    return text
