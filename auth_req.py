import user_config 
import oauth2 as oauth


"""
Generic method to send oauth requests 
Taken from sample at : https://dev.twitter.com/oauth/overview/single-user 
NOTE : Sample taken from twitter dev was out of date, this is slightly modified
"""
def oauth_req(url, key=user_config.my_access_token['access_token'], 
		secret=user_config.my_access_token['access_token_secret'], 
		http_method="GET", post_body=None, http_headers=None):
	token = oauth.Token(key=key, secret=secret)
	consumer = oauth.Consumer(key=user_config.consumer['key'], secret=user_config.consumer['secret'])
	
	client = oauth.Client(consumer, token) 
	resp, content = client.request(url, "GET")
	return resp, content



