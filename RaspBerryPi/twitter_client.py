import tweepy
import json
from env import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)
 
client = tweepy.Client(
    consumer_key = consumer_key,
    consumer_secret = consumer_secret,
    access_token = access_token,
    access_token_secret = access_token_secret
)

def tweet_tempture():
    tempture_json = open("tempture.json", "r")
    tempture_dic = json.load(tempture_json)
    tempture_text = f"室温：{tempture_dic['temp']}　湿度：{tempture_dic['huid']}"
    print(tempture_text)
    client.create_tweet(text = tempture_text)