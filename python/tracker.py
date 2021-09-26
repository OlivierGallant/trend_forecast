import numpy as np 


class Tracker:
    def __init__(self, name, all_names):
        self.name = name
        self.all_names = all_names
        self.associated_tweets = [] # list of tweet objects associated
        self.associated_tweets_dict = []
        self.likes = 0
        self.mentions = 0
        self.delta = 0 # delta is tracker in the object itself
        self.lost_likes = 0 # lost likes tracker


    def get_name(self): return self.name

    def get_all_names(self): return self.all_names

    def get_associated_tweets(self): return self.associated_tweets

    def set_associated_tweet(self, id, tweet):
        self.associated_tweets[id] = tweet
    
    def set_associated_tweets_dict(self, tweets):
        self.associated_tweets_dict = tweets

    def set_mentions(self, mentions):
        self.mentions = mentions
    
    def set_likes(self, likes):
        self.likes = likes

    def add_associated_tweet(self, tweet): 
        self.associated_tweets.append(tweet)

    def get_accumulated_likes(self):
        likes = 0
        for tweet in self.associated_tweets:
            likes += tweet.get_likes()
        return likes

    def get_accumulated_mentions(self):
        return len(self.associated_tweets)

    def get_lost_likes(self): return self.lost_likes

    def get_delta(self): return self.delta

    def dict_format(self):
        dict = {
            'name': self.name,
            'all_names': self.all_names,
            'associated_tweets_dict': [[tweet.get_user(), tweet.get_user_id(), tweet.get_content(), tweet.get_comments(), tweet.get_likes(), tweet.get_date()] for tweet in self.get_associated_tweets()],
            'likes': self.likes,
            'mentions': self.mentions,
            'delta': self.delta,
            'lost_likes': self.lost_likes
        }
        return dict

