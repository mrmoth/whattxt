import BeautifulSoup

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




#found this shit on stackoverflow
def stripHtmlTags(htmlTxt):
    if htmlTxt is None:
        return None
    else:
        return ''.join(BeautifulSoup.BeautifulSoup(htmlTxt).findAll(text=True))

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
