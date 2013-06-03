from modules import stripHtmlTags, sizeof_fmt

class textResponses(object):
    def __init__(self, apihandle, user):
        self.apihandle = apihandle
        self.userId = apihandle.request('usersearch', search=user)[u'response'][u'results'][0][u'userId']

    def parseResponse(self, response):
        response = response.lower().split(' ')
        if 'top' in response[0]:
            if len(response) == 1:
                return self.topTen()
            return self.topTen(response[1])
        if 'ratio' in response[0]:
            if len(response)==1: #i.e., they didn't specify a name.
                return self.ratio()
            return self.ratio()
        if 'sub' in response[0]:
            return self.checkSubscriptions(self.apihandle)[0]

    def topTen(self, period='day'):
        top = self.apihandle.request('top10')
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

        return "Not sure what that meant. Try again bud."

    def checkSubscriptions(self):
        subscriptions = self.apihandle.request("subscriptions")[u'response'][u'threads']
        threads = []

        for thread in subscriptions:
            threads.append([thread[u'threadTitle'],thread[u'threadId'], thread[u'lastPostId']])

        if len(threads) == 0:
            return "No new Subscriptions"

        message = ""

        for title in threads:
            message += title[0]+"\n"
            posts = self.apihandle.request("forum", type="viewthread", threadid=title[1], postid=title[2])[u'response'][u'posts']
            message+=posts[-1][u'body']+"\n" #I'm only doing it this in case I figure out how to get the bottom code working so meh whatever.
            '''
            until I figure out how to get this to only add the last read posts it's pretty useless.
            for post in posts:
                message += post[u'body']+"\n"
            '''
        return (stripHtmlTags(message), threads)


    def ratio(self):
        user = self.apihandle.request('user',id=self.userId)[u'response'][u'stats']
        text = "ratio: %s\nUpload:%s, Download:%s" % (user[u'ratio'], sizeof_fmt(int(user[u'uploaded'])), sizeof_fmt(int(user[u'downloaded'])))
        return text
