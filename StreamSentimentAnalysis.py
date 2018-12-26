import re, tweepy, json, dataset
from textblob import TextBlob
from sqlalchemy.exc import ProgrammingError

# Connect to database / create database
db = dataset.connect("sqlite:///.vscode/streamSentimentAnalysis.db")

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
api = tweepy.API(auth, retry_count=3, retry_delay=5, retry_errors=([401, 404, 500, 503]))

# Setup variables
# Handle defines a particular handle that you must be mentioned, e.g. a tweet reply (RTs are excluded)
# keywords describe words that may be included in the tweet
handle = ''
keywords = ['Buhari']

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # filter out retweets and tweets where handle is not mentioned and tweets not starting with RT
        focus = '@'+handle.lower() if len(handle) != 0 else '' # add '@' to handle if it's not blank
        if status.retweeted or not re.findall(focus, status.text.lower()) or re.findall('^rt+', status.text.lower()):
            return
        description = status.user.description
        loc = status.user.location
        text = status.text
        coords = status.coordinates
        geo = status.geo
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        print(status.text)

        # Perform sentiment analysis using TextBlob
        blob = TextBlob(text)
        sentiment = blob.sentiment

        # Add files to database
        if coords is not None:
            coords = json.dumps(coords)

        if geo is not None:
            geo = json.dumps(geo)
        table = db["tweets"]
        try:
            table.insert(dict(
                user_description=description,
                user_location=loc,
                coordinates=coords,
                text=text,
                user_name=name,
                user_created=user_created,
                user_followers=followers,
                id_str=id_str,
                created=created,
                retweet_count=retweets,
                user_bg_color=bg_color,
                polarity=sentiment.polarity,
                subjectivity=sentiment.subjectivity,
            ))
        except ProgrammingError as err:
            print(err)
    
    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects strea
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=keywords)
