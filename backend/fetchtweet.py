import requests
import string
from nltk.stem import PorterStemmer
from collections import Counter
import emoji
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sentence_transformers import SentenceTransformer
import numpy as np
import re
model_name="all-MiNiLM-L6-v2"
model_encode=SentenceTransformer(model_name)
bearer_token=""
def getStatus(link):
    return link.split('/')[-1]
st=PorterStemmer()
def preprocess(text):
    x=" ".join([st.stem(x) for x in text.split()])
    x=x.translate(str.maketrans('','',string.punctuation))
    return x
def fetchtweet(bearer_token,tweet_id,no_of_tweets):
    url = f"https://api.twitter.com/2/tweets/search/recent?query=conversation_id:{tweet_id}"
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    params = {
        "max_results": no_of_tweets,
        "expansions": "author_id",
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        print("Request successful!")
        replies=response.json()
    else:
        print("Request failed with status code", response.status_code)
        replies=None
    return replies
def postfetch(replies):
    res = []
    for i in replies['data']:
        res.append(i['text'])
    res1 = [i.split() for i in res]
    res1 = [word for i in res1 for word in i]
    out=[]
    for i in [i[0] for i in Counter(res1).most_common()]:
        if '@' in list(i):
            out.append(i)
    author=out[0]
    out=[]
    for i in res:
        out.append(" ".join(emoji.replace_emoji(re.sub(r'http[s]?://\S+', '', i)).split()[1:]))
    cleaned_comments= [name for name in out if name.strip() != '']
    return cleaned_comments
# Rebuild the model (you already have this part)
model = Sequential([
    Bidirectional(LSTM(128, return_sequences=True), input_shape=(1, 384)),
    Dropout(0.3),
    BatchNormalization(),
    Bidirectional(LSTM(64, return_sequences=False)),
    Dropout(0.3),
    BatchNormalization(),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(4, activation='softmax')
])

# Load only the weights, not the full model
model.load_weights("model.keras")

def predict_class(text):
    vector = model_encode.encode(text)
    vector = vector.reshape((1, 1, 384))
    probs = model.predict(vector)
    class_index = np.argmax(probs)
    return class_index
def getSentiment(link):
    status=getStatus(link)
    tweets=fetchtweet(bearer_token,status,10)
    tweets=postfetch(tweets)
    print(tweets)
    res=[predict_class(i) for i in tweets]
    return res
def count_occ(arr):
    counts = Counter(arr)
    return [counts[i] for i in range(4)]
# getSentiment("https://x.com/SecRubio/status/1900655283380146267")