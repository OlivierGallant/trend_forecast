import json
import os 
import datetime
import time 
import pandas as pd

class FileWriter():
    def reset(self):
        dict_clean = {
            'username':[],
            'date':[],
            'content':[],
            'likes':[],
            'reposts':[],
            'comments':[]
        }

        with open('python/Data/Tweets.json', 'w') as json_file:
            json.dump(dict_clean, json_file)
            time.sleep(0.01)
        


    def update_dictionary(self, filename, tweets):
        with open(filename) as json_file:
            data = json.load(json_file)

        for tweet in tweets:
            data['username'].append(tweet.get_user())
            data['date'].append(tweet.get_date())
            data['content'].append(tweet.get_content())
            data['likes'].append(tweet.get_likes())
            data['reposts'].append(tweet.get_reposts())
            data['comments'].append(tweet.get_comments())

        return data
                


    def write_json(self, filename, tweets):
        with open(filename, 'w') as json_file:
            json.dump([tweet.__dict__ for tweet in tweets], json_file)

        
    def read_file(self, filename):
        with open(filename) as json_file:
            return json.load(json_file)

