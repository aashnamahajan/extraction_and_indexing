# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 11:04:17 2019

@author: Aashna Mahajan
"""

import unicodedata
import sys
import json

def remove_punctuation(text):
    tbl = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))
    return text.translate(tbl)

data= json.load(open('C://Users//Aashna Mahajan//Desktop//my json files//AmitShah_tweets.json',encoding="utf-8-sig"))

for i in data:
    if( i['tweet_hi'] ):
        x=remove_punctuation( i['tweet_hi'] )
        
with open('AmitShah_tweets.json', 'w', encoding='utf-8') as f:
        json.dump(x, f, ensure_ascii=False, indent=4)
              