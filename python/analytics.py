from tweet import Tweet
from filewriter import FileWriter
from tracker import Tracker
import time
from datetime import datetime
import pandas as pd
import json
import filecmp
import winsound

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

filewriter = FileWriter()


''' formats date from str(YYYY-MM-DD-HH-MM-SS:MS) -> list ['YYYY', 'MM', 'DD', 'HH', 'MM', 'SS'] '''

def return_all_trackers(trackers):
    temp = []
    for tracker in trackers:
        temp.append(tracker.get_name())
    return temp

def calculate_delta_tweets(tweets_new, tweets_old):
        #take one of the new tweets
        for tweet_new in tweets_new:
            try:
                #search the corresponding old tweet
                for tweet_old in tweets_old:
                    if tweet_old.get_date() == tweet_new.get_date():
                        if tweet_old.get_user() == tweet_new.get_user():
                            if tweet_old.get_content() == tweet_new.get_content():
                                tweet_new.set_delta_tweet(int(tweet_new.get_likes()) - int(tweet_old.get_likes()))
                                raise StopIteration
                tweet_new.set_delta_tweet(int(tweet_new.get_likes()))
            except StopIteration:
                None

'''ef calculate_delta(trackers, trackers_old):
    for tracker in trackers:
        for tracker_old in trackers_old:
            if tracker.get_name() == tracker_old.get_name():
                tracker.delta = int(tracker.get_accumulated_likes()) - int(tracker_old.get_accumulated_likes()) + tracker.lost_likes
'''

def calculate_delta(trackers): #calculates accumulated delta existing for a tracker
    for tracker in trackers:
        delta = tracker.get_accumulated_likes() - tracker.likes + tracker.lost_likes
        tracker.delta = delta
    return


def new_data_available():
    try:
        if filecmp.cmp('python/Data/Tweets.json', 'python/Data/history_tweets/Tweets_backup.json'):
            return False
        else: return True
    except:
        return True
        

def initialize_trackers(tracker_dict_location):
    trackers_dict = filewriter.read_file(tracker_dict_location)
    trackers = []

    for name, all_names in zip(trackers_dict['name'], trackers_dict['all_names']):
        trackers.append(Tracker(name, all_names))
    return trackers


def update_tweets():
    found = False
    while found == False:
        try:
            tweets_json = filewriter.read_file('python/Data/Tweets.json')
            found = True
        except:
            found = False
            time.sleep(1)
            
    tweets = []
    for tweet in tweets_json:
        user = tweet['user']
        user_id = tweet['user_id']
        content = tweet['content'].replace('#',' ').replace('.', ' ').replace('@', ' ').replace(',', ' ')
        comments = tweet['comments']
        reposts = tweet['reposts']
        likes = tweet['likes']
        date = tweet['date']
        tweets.append(Tweet(user, user_id, content, date, comments, reposts, likes))
    return tweets

'''function which updates associated trackers and makes sure no duplicates are inserted'''
def update_trackers(trackers):
    for tracker in trackers:
        tracker.lost_likes = 0
        tracker.likes = tracker.get_accumulated_likes()
        for tweet in tweets:
            try:
                for tracker_name in tracker.get_all_names():
                    if tweet.get_content().lower().find(tracker_name.lower()) >= 0:
                        try:
                            for id, associated_tweet in enumerate(tracker.get_associated_tweets()):
                                if associated_tweet.get_date() == tweet.get_date():
                                    if associated_tweet.get_user() == tweet.get_user():
                                        if associated_tweet.get_content() == tweet.get_content():
                                            tracker.set_associated_tweet(id, tweet)
                                            raise StopIteration 
                            #check if empty
                            tracker.add_associated_tweet(tweet)  
                            likes_delta = tweet.get_likes()/(datetime.utcnow() - datetime(int(tweet.get_year()), int(tweet.get_month()), int(tweet.get_day()), int(tweet.get_hour()), int(tweet.get_minute()), int(tweet.get_second()))).total_seconds()*180
                            tracker.lost_likes += likes_delta - tweet.get_likes()
                            raise StopIteration
                        except StopIteration:
                            None
                            ''' tweet already exists '''
                            raise StopIteration
            except StopIteration:
                None
        print(len(tracker.get_associated_tweets()))
        print(tracker.get_accumulated_mentions())
    return


def remove_outdated_tweets_in_trackers(trackers):
    time_now = datetime.utcnow()
    for tracker in trackers:
        associated_tweets = []
        for tweet in tracker.get_associated_tweets():
            if (time_now - datetime(int(tweet.get_year()), int(tweet.get_month()), int(tweet.get_day()), int(tweet.get_hour()), int(tweet.get_minute()), int(tweet.get_second()))).total_seconds() < 86400:
                associated_tweets.append(tweet)
            else:
                tracker.lost_likes += tweet.get_likes()
        tracker.associated_tweets = associated_tweets

             

# initializing arrays
trackers = []
tweets = []
tweets_history = []
trackers_history = []

#create a filewriter for IO 
filewriter = FileWriter()

#initialize trackers
os.chdir(r'C:\Users\Bloempot\Documents\Programming\trend_forecast_beta')
path_datadir_gui = r'python/Data/'
trackers = initialize_trackers('python/Trackers/crypto_top100.json')
# build tweet objects
i = 0
while True:
    if True:
        if new_data_available():
            '''update tweets and trackers'''
            tweets = update_tweets()
            tweets_history.append(tweets) #append all the tweets to the history list
            update_trackers(trackers)
            remove_outdated_tweets_in_trackers(trackers) #check for outdated tweets, and account for lost likes in metrics
            trackers_history.append(trackers) #append all the trackers to the history list

            ''' convert the trackers to a pandasframe to do further analytics '''

            ''' ----------- analytics ----------- '''
            try:
                calculate_delta_tweets(tweets, tweets_history[-2])
            except IndexError:
                None
            calculate_delta(trackers)

            ''' ----------- end of analytics ------------'''
            

            ''' ----------- data pipelines --------------'''

            # write tweets to backup and a tracked backup file (BACKUP PIPELINES)
            with open('python/Data/history_tweets/Tweets_backup.json', 'w+') as json_file:
                json.dump([tweet.__dict__ for tweet in tweets], json_file)
            with open('python/Data/history_tweets/Tweets_'+datetime.utcnow().strftime('%Y-%m-%d-T%H-%M-%S')+'.json', 'w+') as json_file:
                json.dump([tweet.__dict__ for tweet in tweets], json_file)
            with open('python/Data/Tweets.json', 'w+') as json_file:
                json.dump([tweet.__dict__ for tweet in tweets], json_file)
            with open('python/Data/history_trackers/trackers_'+datetime.utcnow().strftime('%Y-%m-%d-T%H-%M-%S')+'.json', 'w+') as json_file:
                json.dump([tracker.dict_format() for tracker in trackers], json_file)
    
            # live pipelines (pandas csv)
            time_now = datetime.utcnow().strftime('%Y-%m-%d-T%H-%M-%S')

            # check if pipelines are initialized
            if not os.path.isdir('python/Data/analytics/'+str(trackers[0].get_name())):
                os.mkdir('python/Data/analytics/'+str(trackers[0].get_name()))

            try:
                pd.read_csv('python/Data/analytics/Bitcoin/bitcoin_'+datetime.utcnow().strftime('%Y-%m-%d')+'.csv')
            except:
                pd.DataFrame(columns = ['Timestamp', 'likes', 'mentions', 'delta']).to_csv('python/Data/analytics/Bitcoin/bitcoin_'+datetime.utcnow().strftime('%Y-%m-%d')+'.csv')

                
            # append new data
            likes = trackers[0].get_accumulated_likes()
            mentions = trackers[0].get_accumulated_mentions()
            delta = trackers[0].get_delta()

            df = pd.read_csv('python/Data/analytics/Bitcoin/bitcoin_'+datetime.utcnow().strftime('%Y-%m-%d')+'.csv', index_col=0)
            print(df)
            df =df.append(pd.DataFrame([[time_now, likes, mentions, delta]], columns=['Timestamp', 'likes', 'mentions', 'delta']))
            print(df)
            df.to_csv('python/Data/analytics/Bitcoin/bitcoin_'+datetime.utcnow().strftime('%Y-%m-%d')+'.csv')

            
            winsound.Beep(1000, 150)
            print('LOG: DATA UPDATED')
            print('STATISTICS:')
            print('bitcoin--- Delta='+str(trackers[0].get_delta())+' Likes='+str(trackers[0].get_accumulated_likes()) +' Mentions='+str(trackers[0].get_accumulated_mentions()))
            if int(trackers[0].get_delta()) > 1500:
                for i in range(1, 10):
                    winsound.Beep(i*150, 250)
                    
            time.sleep(5)   
        else:
            time.sleep(5)



    ''' DECAPRICATED
            for id, tracker_name in enumerate(list(export_list_sorted[0])):
                if id == 8: break
                for tracker in trackers:
                    if tracker.get_name() == tracker_name:
                        temp_tweets = tracker.get_associated_tweets()
                        temp_tweets.sort(key=lambda x: x.get_likes(), reverse=True)
                        export_list_tweets_top10_trackers.append(temp_tweets[0:4])
            print(export_list_tweets_top10_trackers)
            with open(r'python\Data\export_tracker_tweets.json', 'w') as json_file:
                json.dump([tweet.__dict__ for list in export_list_tweets_top10_trackers for tweet in list], json_file)
'''    



