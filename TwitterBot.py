print('my twitter bot')

import tweepy, json, time, datetime

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

mentions = api.mentions_timeline(count=50)
lastTweetTime = mentions[-1].created_at

focusString = 'Stephen Hawking'

# The tweet order is from latest [0] to earliest [-1]
# So on responding, we need to respond from earliest to latest - note this in the for statement
# pick the time of the last created tweet in the list
# use that time to retrieve the next 150 tweets and save as mentions
# wait 15 seconds
# repeat

"""
DATABASE MANAGEMENT
"""

# Connect to database
import sqlite3, time
from sqlite3 import Error

# Create database if it doesn't exist
def create_connection(db_file):
    """
    Create a database connection to an sqlite database (or in memory)
    """
    try:
        conn = sqlite3.connect(db_file)
        # to create the connection in memory, just write this instead
        # conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

create_connection('.vscode/sqlite.db')


# Connect to database
conn = sqlite3.connect('.vscode/sqlite.db')
c = conn.cursor()
# Create mentionsTable if it doesn't exist
c.execute("CREATE TABLE IF NOT EXISTS mentionsTable (id, author, tweet)")

# Insert tweets into database
for mention in mentions:
    c.execute("INSERT INTO mentionsTable(id, author, tweet) VALUES (?, ?, ?)", (mention.created_at, mention.author.screen_name, mention.text))
conn.commit()
conn.close()