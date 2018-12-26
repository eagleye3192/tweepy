print('my twitter bot')

import tweepy, json

# Get API keys from twitter.json
with open(".vscode/twitter.json") as f:
    twitter_api = json.load(f)

CONSUMER_KEY = twitter_api['API']['CONSUMER_KEY']
CONSUMER_SECRET = twitter_api['API']['CONSUMER_SECRET']
ACCESS_KEY = twitter_api['API']['ACCESS_KEY']
ACCESS_SECRET = twitter_api['API']['ACCESS_SECRET']

# Setup api object to connect to Twitter
auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
auth.set_access_token(key=ACCESS_KEY, secret=ACCESS_SECRET)
api = tweepy.API(auth)

mentions = api.mentions_timeline(count=3)