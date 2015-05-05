import smtplib
import config
from email.mime.text import MIMEText

def sendEmail(to, message):
	message = message.encode("utf-8")
	me = config.email['from_addr'] 
	msg = MIMEText(message)
	msg['To'] = config.email['to']
	msg['From'] = config.email['from_addr']
	msg['Subject'] = config.email['subject'] 

	#s = smtplib.SMTP('localhost', port=1025)
	s = smtplib.SMTP()
	s.connect(config.email_server['host'], config.email_server['port'])
	s.starttls()
	s.login(config.email_server['login'], config.email_server['password'])
	s.sendmail(me, [to], msg.as_string())
	s.quit()

"""
The keywordDicts should be in the form of: 
{
	mainKeyword :  {
		keyword1 : count,
		keyword2 : count
	},
	secondKeyword : {
		keyword1 : count
	}
}
"""
def getMessageFromKeywords(keywordDicts):
	msg = ""
	lb = "\r\n"
	for mainKeyword in keywordDicts:
		msg += "Trending keywords for : " + mainKeyword + lb
		keywordDict = keywordDicts[mainKeyword]
		if not keywordDict:
			continue
		for word in keywordDict:
			msg += word + ":" + str(keywordDict[word]) + lb 

		msg += lb
	return msg
