# extraction_and_indexing
Twitter data extraction and Indexing of the data


Interested in political tweets from the following types of persons of interest(POI):

● Politicians
● Journalists
● Social Activists

Countries:

● USA
● India
● Brazil

Multilingual dataset containing following languages

● English
● Hindi
● Portuguese

<B> EXTRACTION : </B>

1. At least 33,000 tweets in total with not more than 15% being retweets.
2. At least 1000 tweets per person of interest. Note that Twitter allows max 3200 recent
tweets to be extracted from a person’s account.
3. At least 20 replies to each of the tweet posted by the POIs for 5 consecutive days.
4. At least 3000 replies in total across all POIs
5. At least 5,000 tweets per language i.e, English, Hindi and Portuguese
6. At least 5,000 tweets per country
7. At least 1000 tweets containing hashtags/keywords related to person of interest

<B> INDEXING : </B>

1. Person of Interest: Name and Ids of at least 15 persons of interest
2. Country: one amongst USA, India and Brazil
3. All the replies to a particular tweet of a particular person of interest
4. One copy of the tweet text that retains all content (see below) irrespective of the
language. This field should be set as the default field while searching.
5. Language of the tweet (as identified by Twitter) and a language specific copy of the tweet
text that removes all stopwords (language specific), punctuation, emoticons, emojis, kaomojis, 
hashtags, mentions, URLs and other Twitter discourse tokens. Thus, you would
have at least four separate fields that index the tweet text, the general field above plus
three for each language. For any given tweet, only two of the four fields would have a
value.
6. Separate fields that index: hashtags, mentions, URLs, tweet creation date, emoticons+
(emoticons + emojis+ kaomojis)
7. Additionally, geolocation (if present), and any other fields you may like.
