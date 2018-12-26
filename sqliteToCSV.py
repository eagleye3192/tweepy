import sqlite3, csv

conn = sqlite3.connect('.vscode/streamSentimentAnalysis.db')
cur = conn.cursor()

data = cur.execute('SELECT * from tweets')
# columns = cur.execute('PRAGMA table_info(tweets)')

with open('.vscode/output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([
        'user_description',
        'user_location',
        'coordinates',
        'text',
        'user_name',
        'user_created',
        'user_followers',
        'id_str',
        'created',
        'retweet_count',
        'user_bg_color',
        'polarity',
        'subjectivity',
        ])
    writer.writerows(data)
conn.close()