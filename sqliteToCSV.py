import dataset, pandas as pd

db = dataset.connect("sqlite:///.vscode/streamSentimentAnalysis.db")

outputDict = {}
for tweet in db['tweets']:
    outputDict[tweet['id']] = [tweet['id_str'], tweet['user_name'], tweet['created'], tweet['text'], tweet['polarity'], tweet['subjectivity']]

pd.DataFrame.from_dict(outputDict, orient='index', columns=['id_str', 'user_name', 'created', 'text', 'polarity', 'subjectivity']).to_csv('.vscode/output.csv')

"""  # If you intend to use csv and sqlite3 instead
import csv, sqlite3
conn = sqlite3.connect('.vscode/streamSentimentAnalysis.db')
cur = conn.cursor()

data = cur.execute('SELECT id, user_name, text, polarity, subjectivity from tweets')
# columns = cur.execute('PRAGMA table_info(tweets)')

with open('.vscode/output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow([
        'id',
        'user_name',
        'text',
        'polarity',
        'subjectivity',
        ])
    writer.writerows(data)
conn.close() """