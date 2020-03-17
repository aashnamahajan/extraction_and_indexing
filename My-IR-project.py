# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 22:54:51 2019

@author: Aashna Mahajan
"""
import tweepy
import json
import time
from datetime import datetime
from datetime import timedelta
from collections import Counter
import regex
import re
import emoji
import preprocessor as p
import string

api_key = "dtXDBEocb2hjne5oF5UCeFgCu" 
api_secret = "Cs6TBYaVrjFC9NAmGTbSzjT8VvvAjQtClXZet9xyPREf6O9uz7"
access_key = "330988061-fvceDeUg3A6F3J3e4H1qC6lfIHoVBtVlnowTa8sG"
access_secret = "dx6VKbCNs5jeLafLBDq1z5XFp8LSqNjad0jgKjRXAQr5w"

# Authorization to consumer key and consumer secret
auth = tweepy.OAuthHandler(api_key, api_secret) 
# Access to user's access key and access secret 
auth.set_access_token(access_key, access_secret) 
# Calling api 
api = tweepy.API(auth) 

emoticons = {':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}', ':^)', ':-D', ':D', '8-D',
             '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D', '=-3', '=3', ':-))', ":'-)", ":')", ':*' , ':^*', '>:P',
             ':-P', ':P', 'X-P', 'x-p', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)', '<3', ':L',
             ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<', ':-[', ':-<', '=\\', '=/', '>:(', ':(',
             '>.<', ":'-(", ":'(", ':\\', ':-c', ':c', ':{', '>:\\', ';('}

the_poi_id=0

#emoticons
def strip_smileys_emojis(text):
    smileys_emojis = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            smileys_emojis.append(word)
    for item in emoticons:
        if str(text).replace(" ", "").__contains__(item):
            smileys_emojis.append(item)
    return smileys_emojis

def hour_rounder(t):
    return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
               +timedelta(hours=t.minute//30))
    
def modifying_the_fields(tweet , username):
    emoticon_list= strip_smileys_emojis(tweet.full_text)
    tweet._json['country']='India'
    tweet._json['poi_name']=username
    tweet._json['tweet_lang'] = tweet._json['lang']
    tweet._json["replied_to_tweet_id"] = tweet._json["in_reply_to_status_id"] if tweet._json["in_reply_to_status_id"] is not None else None
    tweet._json["replied_to_user_id"] = tweet._json["in_reply_to_user_id"] if tweet._json["in_reply_to_user_id"] is not None else None
    tweet._json["mentions"] = None if tweet._json['entities']['user_mentions'] is None else [d['screen_name'] for d in tweet._json['entities']['user_mentions']]
    #tweet._json["tweet_urls"] = None if tweet._json['entities']['urls'] is None else [d['url'] for d in tweet._json['entities']['urls']]
    tweet._json["tweet_urls"] =  re.findall(r'(https?://\S+)', tweet.full_text)
    
    tweet._json["hashtags"] = None if tweet._json['entities']['hashtags'] is None else [d['text'] for d in tweet._json['entities']['hashtags']]
    tweet._json['tweet_emoticons'] = None if len(emoticon_list) == 0 else str(emoticon_list)
    tweet._json['full_text'] = tweet.full_text.replace("&lt;", "<").replace("&amp;", "&").replace("&gt;", ">")
    tweet._json['tweet_text'] = tweet._json['full_text'] 
    tweet._json['tweet_date'] = str(hour_rounder(datetime.strptime(tweet._json['created_at'], '%a %b %d %H:%M:%S %z %Y')).strftime("%Y-%m-%dT%H:%M:%SZ"))
    tweet._json["reply_text"] = None if tweet._json["replied_to_tweet_id"] is None else tweet._json["tweet_text"]
    if (tweet.lang == 'hi'):
        tweet._json['tweet_hi'] = p.clean(tweet._json['tweet_text'])
        x=tweet._json['tweet_hi']
        tweet._json['tweet_hi'] = x.translate(str.maketrans('', '', string.punctuation)) 
        repeated_emoticon_list= strip_smileys_emojis(tweet._json['tweet_hi'])
        for i in repeated_emoticon_list:
            if i in tweet._json['tweet_hi']:
                tweet._json['tweet_hi'] = tweet._json['tweet_hi'].replace(i,"")
        
        tweet._json['tweet_en'] = None
        tweet._json['tweet_pt'] = None
    elif (tweet.lang == 'en'):
        tweet._json['tweet_en'] = p.clean(tweet._json['tweet_text'])
        x=tweet._json['tweet_en']
        tweet._json['tweet_en'] = x.translate(str.maketrans('', '', string.punctuation)) 
        repeated_emoticon_list= strip_smileys_emojis(tweet._json['tweet_en'])
        for i in repeated_emoticon_list:
            if i in tweet._json['tweet_en']:
                tweet._json['tweet_en'] = tweet._json['tweet_en'].replace(i,"")
        s=tweet._json['tweet_en']
        tweet._json['tweet_en']=re.sub(' +', ' ', re.sub(r'[^\w]', ' ', s)).strip()
        tweet._json['tweet_hi'] = None
        tweet._json['tweet_pt'] = None
    elif (tweet.lang == 'pt'):
        tweet._json['tweet_pt'] = p.clean(tweet._json['tweet_text'])
        x=tweet._json['tweet_pt']
        tweet._json['tweet_pt'] = x.translate(str.maketrans('', '', string.punctuation)) 
        repeated_emoticon_list= strip_smileys_emojis(tweet._json['tweet_pt'])
        for i in repeated_emoticon_list:
            if i in tweet._json['tweet_pt']:
                tweet._json['tweet_pt'] = tweet._json['tweet_pt'].replace(i,"")
        
        
        tweet._json['tweet_en'] = None
        tweet._json['tweet_hi'] = None
    else:
        tweet._json['tweet_pt'] = None
        tweet._json['tweet_en'] = None
        tweet._json['tweet_hi'] = None 
     

  
    
def get_tweets(username, number_of_tweets):
        # tweets to be extracted 
        
        #get 200 tweets from the particular id
        #tweets = api.user_timeline(screen_name=username, count=number_of_tweets, max_id=00000)  
        tmp = []
        tweet_count = 0
        last_id=0
        for index in range(0,50):
            if index==0:
                tweets = api.user_timeline(screen_name=username, count=number_of_tweets,include_rts=False, tweet_mode='extended') 
            else:
                tweets = api.user_timeline(screen_name=username, count=number_of_tweets, max_id=last_id, include_rts=False, tweet_mode='extended') 
                         
            #tweets_for_csv = [tweet.text for tweet in tweets] # CSV file created  
            emoticon_list=[]                     
            for j in tweets:            
                if hasattr(j, "retweeted_status") or j.in_reply_to_status_id != None:
                    continue;
                else:
                    if(j.lang=="en" or j.lang=="hi"):
                        tweet_count+=1
                        emoticon_list= strip_smileys_emojis(j.full_text)
                        j._json['country']='India'
                        j._json['poi_name']=j.user.screen_name
                        j._json["poi_id"] = j._json["user"]["id"]
                        the_poi_id= j._json["poi_id"]
                        j._json['full_text'] = j.full_text.replace("&lt;", "<").replace("&amp;", "&").replace("&gt;", ">") 
                        j._json['tweet_text'] = j._json['full_text']
                        j._json["replied_to_tweet_id"] = j._json["in_reply_to_status_id"] if j._json["in_reply_to_status_id"] is not None else None
                        j._json["replied_to_user_id"] = j._json["in_reply_to_user_id"] if j._json["in_reply_to_user_id"] is not None else None
                        j._json["reply_text"] = None if j._json["replied_to_tweet_id"] is None else j._json["tweet_text"]
                        j._json["mentions"] = None if j._json['entities']['user_mentions'] is None else [d['screen_name'] for d in j._json['entities']['user_mentions']]
                        j._json["tweet_urls"] =  re.findall(r'(https?://\S+)', j.full_text)
                        j._json["hashtags"] = None if j._json['entities']['hashtags'] is None else [d['text'] for d in j._json['entities']['hashtags']]
                        
                        j._json['tweet_emoticons'] = None if len(emoticon_list) == 0 else str(emoticon_list)
                        
                        j._json['tweet_date'] = str(hour_rounder(datetime.strptime(j._json['created_at'], '%a %b %d %H:%M:%S %z %Y')).strftime("%Y-%m-%dT%H:%M:%SZ"))
                        j._json['tweet_lang'] = j._json['lang']
                        if (j.lang == 'hi'):
                            j._json['tweet_hi'] = p.clean(j._json['tweet_text'])
                            x=j._json['tweet_hi']
                            j._json['tweet_hi'] = x.translate(str.maketrans('', '', string.punctuation)) 
                            repeated_emoticon_list= strip_smileys_emojis(j._json['tweet_hi'])
                            for i in repeated_emoticon_list:
                                if i in j._json['tweet_hi']:
                                    j._json['tweet_hi'] = j._json['tweet_hi'].replace(i,"")
                            
                            j._json['tweet_en'] = None
                            j._json['tweet_pt'] = None
                        elif (j.lang == 'en'):
                            j._json['tweet_en'] = p.clean(j._json['full_text'])
                            j._json['tweet_en'] = p.clean(j._json['full_text'])
                            x=j._json['tweet_en']
                            j._json['tweet_en'] = x.translate(str.maketrans('', '', string.punctuation)).strip() 
                            repeated_emoticon_list= strip_smileys_emojis(j._json['tweet_en'])
                            for i in repeated_emoticon_list:
                                if i in j._json['tweet_en']:
                                    j._json['tweet_en'] = j._json['tweet_en'].replace(i,"")
                            s=j._json['tweet_en']
                            j._json['tweet_en']=re.sub(' +', ' ', re.sub(r'[^\w]', ' ', s))
                            j._json['tweet_hi'] = None
                            j._json['tweet_pt'] = None
                        elif (j.lang == 'pt'):
                            j._json['tweet_pt'] = p.clean(j._json['full_text'])
                            j._json['tweet_pt'] = p.clean(j._json['full_text'])
                            x=j._json['tweet_pt']
                            j._json['tweet_pt'] = x.translate(str.maketrans('', '', string.punctuation)) 
                            repeated_emoticon_list= strip_smileys_emojis(j._json['tweet_pt'])
                            for i in repeated_emoticon_list:
                                if i in j._json['tweet_pt']:
                                    j._json['tweet_pt'] = j._json['tweet_pt'].replace(i,"")
                            
                            j._json['tweet_en'] = None
                            j._json['tweet_hi'] = None
                        else:
                            j._json['tweet_pt'] = None
                            j._json['tweet_en'] = None
                            j._json['tweet_hi'] = None                                            
            
                        tmp.append(j._json)
                last_id=j.id
                
        # Saving the tweets in json file
        with open(username + '_tweets2.json', 'w', encoding='utf-8') as f:
            json.dump(tmp, f, ensure_ascii=False, indent=4)
        print("total tweets : " + str(tweet_count) , str(last_id) )        
                
def get_replies(username):
        
    data = json.load(open(username+'_tweets2.json',encoding = 'utf-8'))
    id_list = []
    for i in data:
        if (datetime.strptime(i['created_at'], '%a %b %d %H:%M:%S %z %Y').date() >= datetime.strptime('2019-09-10','%Y-%m-%d').date()):
            id_list.append(i['id_str'])
    print(id_list)
    lowest_id = min(id_list)
    highest_id = max(id_list)
    replies = []
    tweet_reply_ids = []
    reply_count = 0
    last_id = 0
    tweet_reply_ids_dict = {}
    originaltweetidvalidreply=set()
    for m in range(0,50):
        try:
            if(m!=0 and m%10==0):
                print("Sleep Started")
                time.sleep(900)
                print("Sleep Ended")
            if (m==0):   
                for tweet in tweepy.Cursor(api.search,q='to:'+ username, since_id=lowest_id, result_type='recent',timeout=999999, tweet_mode = 'extended').items(200):    
                    if hasattr(tweet, 'in_reply_to_status_id_str'): 
                        for j in id_list:            
                            if (tweet.in_reply_to_status_id_str == j):
                                originaltweetidvalidreply.add(j)
                                tweet._json["poi_id"] = tweet._json["in_reply_to_user_id"]
                                modifying_the_fields(tweet , username)
                                replies.append(tweet._json)
                                tweet_reply_ids.append(j)
                                
                                tweet_reply_ids_dict = dict(Counter(tweet_reply_ids))
                                reply_count += 1
                    last_id = tweet.id
                tweet_reply_ids_dict=dict(tweet_reply_ids_dict)
                for key in sorted(tweet_reply_ids_dict.keys(), reverse=True):
                    if(tweet_reply_ids_dict[key]>20):
                        del tweet_reply_ids_dict[key]
                        print(key)
                        last_id=key
                    else:
                        break
                print(last_id)
                print(len(replies))
                print(tweet_reply_ids_dict)
                with open(username+'_replies2.json', 'w', encoding='utf-8') as f:
                    json.dump(replies, f, ensure_ascii=False, indent=4)
                if (len(tweet_reply_ids_dict) != 0 and tweet_reply_ids_dict[min(tweet_reply_ids_dict.keys(), key=(lambda k: tweet_reply_ids_dict[k]))] >= 20 and set(id_list) == set(tweet_reply_ids)):    
                    break;
                else:
                    continue          

            else:                    
                for tweet in tweepy.Cursor(api.search,q='to:'+username, since_id=lowest_id,max_id = last_id, result_type='recent',timeout=999999, tweet_mode = 'extended').items(200):    
                    if hasattr(tweet, 'in_reply_to_status_id_str'): 
                        for j in id_list:            
                            if (tweet.in_reply_to_status_id_str == j):
                                originaltweetidvalidreply.add(j)
                                tweet._json["poi_id"] = tweet._json["in_reply_to_user_id"]
                                modifying_the_fields(tweet , username)
                                replies.append(tweet._json)
                                tweet_reply_ids.append(j)
                                tweet_reply_ids_dict = dict(Counter(tweet_reply_ids))
                                reply_count += 1
                    last_id = tweet.id   
                tweet_reply_ids_dict=dict(tweet_reply_ids_dict)
                for key in sorted(tweet_reply_ids_dict.keys(), reverse=True):
                    if(tweet_reply_ids_dict[key]>20):
                        del tweet_reply_ids_dict[key]
                        last_id=key
                    else:
                        break
                print(last_id)
                print(len(replies))
                print(tweet_reply_ids_dict)
                with open(username+'_replies2.json', 'w', encoding='utf-8') as f:
                    json.dump(replies, f, ensure_ascii=False, indent=4)
                if (len(tweet_reply_ids_dict) != 0 and tweet_reply_ids_dict[min(tweet_reply_ids_dict.keys(), key=(lambda k: tweet_reply_ids_dict[k]))] >= 20 and set(id_list) == set(tweet_reply_ids)):    
                    break;
                else:
                    continue
        except tweepy.TweepError:
            print("error")
            time.sleep(60 * 15)
            continue

    print(Counter(tweet_reply_ids))                                    
    print('final',reply_count)                        
    print(reply_count)
    #DELETE THE COUNTS FOR NO Reply
    deleteids=[]
    for id in id_list:
        if(id in originaltweetidvalidreply):
            if(tweet_reply_ids_dict[id]<20):
                print(id).append(id)
                deleteids.append(id)
            else:
                print(id)
                deleteids.append(id)
    print(deleteids)
 
def get_hashtags(username):
       
    hashtag_tweets = []
    last_mention_id = 0
    for counter in range(0, 50):
            if(counter == 0):
                for tweet in tweepy.Cursor(api.search, q=f"#{username} OR @{username}", count=200,  include_rts=False, tweet_mode='extended').items(200):
                    #mentions_data.append(add_edit_tweet_fields(tweet._json, language))
                    if(tweet.in_reply_to_screen_name != username) and not hasattr(tweet, "retweeted_status") and tweet.user.verified=='False':
                        tweet._json["poi_id"] = 74756085
                        modifying_the_fields(tweet , username)       
                        hashtag_tweets.append(tweet._json)    
                    last_mention_id = tweet.id
                        
            else:
                for tweet in tweepy.Cursor(api.search, q=f"#{username} OR @{username}", count=200, tweet_mode='extended',  include_rts=False, max_id=last_mention_id).items(200):
                    #mentions_data.append(add_edit_tweet_fields(tweet._json, language))
                    
                    if(tweet.in_reply_to_screen_name != username) and not hasattr(tweet, "retweeted_status") and tweet.user.verified=='False':
                        tweet._json["poi_id"] = 74756085
                        modifying_the_fields(tweet , username)  
                        hashtag_tweets.append(tweet._json)                         
                    last_mention_id = tweet.id
                    
            print(username,'','hashtag_tweets', len(hashtag_tweets))
            if(len(hashtag_tweets) > 1500):
                break
            
    with open(username+'_hashtags2.json', 'w', encoding='utf-8') as f:
        json.dump(hashtag_tweets, f, ensure_ascii=False, indent=4)
                   
if __name__ == '__main__':
    get_hashtags("BolsonaroSP")