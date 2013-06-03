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


    return (username, subject, stripHtmlTags(body), messageId)
def checkSubscriptions(apihandle):
    subscriptions = apihandle.request("subscriptions")[u'response'][u'threads']
    threads = []
    for thread in subscriptions:
        threads.append([thread[u'threadTitle'],thread[u'threadId']])
    if len(threads) == 0:
        return "No new Subscriptions"
    message = ""
    for title in threads:
        message += title[0]+"\n"
        posts = apihandle.request("forum", type="viewthread", threadid=title[1])[u'response'][u'posts']
        message+=posts[-1][u'body'] #I'm only doing it this in case I figure out how to get the bottom code working so meh whatever.
        '''
        until I figure out how to get this to only add the last read posts it's pretty useless.
        for post in posts:
            message += post[u'body']+"\n"
            '''
    return (stripHtmlTags(message), threads)




    pass
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

def parseResponse(response, user, apihandle):
    response = response.lower().split(' ')
    if 'top' in response[0]:
        return topTen(apihandle, response[1])
    if 'ratio' in response[0]:
        if len(response)==1: #i.e., they didn't specify a name.
            return ratio(apihandle, getUserId(apihandle, user))
        return ratio(apihandle, getUserId(apihandle, response[1]))
    if 'sub' in response[0]:
        return checkSubscriptions(apihandle)
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

def ratio(apihandle, userid):
    if userid == None:
        return "That user wasn't found bud."
    user = apihandle.request('user',id=userid)[u'response'][u'stats']
    text = "ratio: %s\nUpload:%s, Download:%s" % (user[u'ratio'], user[u'uploaded'], user[u'downloaded'])
    return text

def getUserId(apihandle, user):
    id = apihandle.request('usersearch', search=user)[u'response'][u'results']
    if len(id)==0:
        return None

    return id[0][u'userId']

#found this shit on stackoverflow
def stripHtmlTags(htmlTxt):
    if htmlTxt is None:
        return None
    else:
        return ''.join(BeautifulSoup.BeautifulSoup(htmlTxt).findAll(text=True))
