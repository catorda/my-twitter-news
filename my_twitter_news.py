from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config
import json
import schedule
import time
import emailer

class KeywordCounter():

	def __init__(self, name):
		self.name = name; 
		self.keywordCount = dict() 
		self.tweetTotal = 0

	def addToCount(self, keywords):
		self.tweetTotal += 1 
		for word in keywords:
			if word in config.unwanted_words:
				continue
			if word in self.keywordCount:
				self.keywordCount[word] = self.keywordCount[word] + 1 
			else:
				self.keywordCount[word] = 1

	def getKeywordCount(self, minimum=0):
		minimum = self.tweetTotal * 0.10
		results = dict()
		for word in self.keywordCount:
			if self.keywordCount > minimum:
				results[word] = self.keywordCount[word]

		return results


jsKeywords = KeywordCounter('javascript')
nodejsKeywords = KeywordCounter('nodejs')
iojsKeywords = KeywordCounter('iojs')
javaKeywords = KeywordCounter('java')
keywordCounters = dict(
	javascript = jsKeywords, 
	nodejs = nodejsKeywords,
	iojs = iojsKeywords, 
	java = javaKeywords
)

def addKeywordsToCounters(text):
	if text.find("javascript") != -1 or text.find("js") != -1:
		keywordCounters['javascript'].addToCount(text.split())
	if text.find("nodejs") != -1:
		keywordCounters['nodejs'].addToCount(text.split())
	if text.find("iojs") != -1:
		keywordCounters['iojs'].addToCount(text.split())
	if text.find("java") != -1:
		keywordCounters['java'].addToCount(text.split())

class StdOutListener(StreamListener):

	def __init__(self):
		self.count = 0 

	def on_data(self, data):
		self.count += 1
		data = json.loads(data)

		if data['lang'] == 'en':
			#print "***** Tweet received ********"
			#print data['text']
			#print "Followers: ", data['user']['followers_count'], " Filter level: ", data['filter_level']

			addKeywordsToCounters(data['text'])
			

		return True

	def on_error(self, status):
		print status 


def emailJob():
	print "**** SENDING EMAIL *****"
	keywordDicts = dict()
	for kwdict in keywordCounters:
		keywordDicts[kwdict] = keywordCounters[kwdict].getKeywordCount()
	message = emailer.getMessageFromKeywords(keywordDicts)
	emailer.sendEmail(config.email['to'], message)

listener = StdOutListener()
auth = OAuthHandler(config.consumer['key'], config.consumer['secret'])
auth.set_access_token(config.my_access_token['access_token'], config.my_access_token['access_token_secret'])
stream = Stream(auth, listener)

schedule.every(30).minutes.do(emailJob)

while True:
	if stream.running is True:
		stream.disconnect()
		print "Stream disconnected", stream.running
	schedule.run_pending()
	stream.filter(track=['nodejs', 'javascript', 'android dev', 'iojs', 'java'], async=True)
	time.sleep(60)