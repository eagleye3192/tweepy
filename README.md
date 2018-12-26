# Stream Automatic Sentiment Analysis

This project automatically retrieves streaming tweets from Twitter based on a number of keywords, (which may or may not also focus on an optionally defined twitter handle), and automatically assigns a sentiment to the tweet. The data is saved as an sqlite database as specified in the code - StreamSentimentAnalysis.py

It also allows you to export the database as a csv file using the sqliteToCSV.py

There is also a Twitter bot (still under development) that should automatically respond to tweets based on criteria you may define in the variable section - TwitterBot.py

## Required modules

- Tweepy
- dataset
- sqlalchemy
- TextBlob

### Other requirements and comments

- A Twitter Dev account with API keys
- I've saved the database itslef outside this git, so  you may need to configure some of the variables as you so desire