#importing libraries needed
import tweepy
import json
import nltk
from nltk.corpus import *
nltk.download('stopwords')
from collections import Counter

# authentication keys
consumer_key = "HnMymptP2MtqO2JwyUAOO9B8X"
consumer_secret = "FpjMdirp8CXoUafDuMCGlZrjW7XBWEwDXYoSWYtHd1GFGbIgvJ"
access_token = "1001496307926781952-bXxh6EFuqaKYb1N5Z8laTXstSQwrOG"
access_secret = "hgrwOHIUPG5wEYk8jYZsOYeKkm4zWr8sGvjeTnwzLOnd9"
oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_secret)
api = tweepy.API(oauth)

# displaying menu
flag = True
def display_menu():
    global flag
    message = str
    while flag==True:
        print("MENU")
        print("1. Retrieve tweets")
        print("2. Count the followers")
        print("3. Determine the sentiment")
        print("4. Location, Language and Time Zone")
        print("5. Comparision of tweets by Narendera Modi and Donald Trump.")
        print("6. Analyse the top usage")
        print("7. Tweet a message")
        print("8. Exit")
        option = int(raw_input("What do you wanna do?"))
        if option==1:
            GetSearch()
            display_menu()
        elif option==2:
            count()
            display_menu()
        elif option == 3:
            sentiment_analysis()
            display_menu()
        elif option == 4:
            location()
            display_menu()
        elif option == 5:
            compare()
            display_menu()
        elif option == 6:
            top_usage()
            display_menu()
        elif option==7:
            tweet_status(new=message)
            display_menu()
        elif option==8:
            print("Exit.")
            flag = False
        else:
            print("Enter a valid value!")
            display_menu()

# putting on the hashtag
def query():
    global tweets
    tweet_input = raw_input("For which hashtag do you want to see the tweets? (Do not include #)")
    tweet_input = "#" + tweet_input
    tweets = api.search(q=tweet_input)

#forming the status object
def GetSearch():
    query()
    status = tweets[0]
    json_str = json.dumps(status._json,indent=4,sort_keys=True)
    print(json_str)

# counting followers
def count():
    query()
    print("UserName      Follower Count")
    for tweet in tweets:
        print(tweet.user.name+"     "+str(tweet.user.followers_count))

# determining the sentiment
def sentiment_analysis():
    flagp = 0
    flagn = 0
    flagneg = 0
    query()
    from paralleldots import set_api_key, get_api_key
    from paralleldots import similarity, ner, taxonomy, sentiment, keywords, intent, emotion, abuse, multilang_keywords
    set_api_key("vE1RAJOzx2YzxpteT70qyAKEQXKxI6ahwfvzCIs8IGw")
    get_api_key()
    for tweet in tweets:
        text = tweet.text
        sentiment_value = sentiment(text)
        values1 = sentiment_value['sentiment']
        if values1 == "positive":
            flagp = flagp + 1
        elif values1 == "negative":
            flagneg = flagneg + 1
        else:
            flagn = flagn + 1
    if flagn > flagneg and flagn > flagp:
        print("Sentiment: Neutral")
    elif flagneg > flagn and flagneg > flagp:
        print("Sentiment: Negative")
    else:
        print("Sentiment: Positive")

# determines the location, language and time zone
def location():
    global time_zone1,loca,lang
    query()
    location = {}
    language = {}
    time_zone = {}
    for tweet in tweets:
        loca = tweet.user.location
        lang = tweet.user.lang
        time_zone1 = tweet.user.time_zone
        if loca in location:
            location[loca] += 1
        else:
            location[loca] = 1
        if lang in language:
            language[lang] += 1
        else:
            language[lang] = 1
        if time_zone1 in time_zone:
            time_zone[time_zone1] += 1
        else:
            time_zone[time_zone1] = 1
    # limiting the display of the values
    if None in time_zone:
        del time_zone[None]
    if '' in time_zone:
        del time_zone['']
    if '' in language:
        del language['']
    if '' in location:
        del location['']
    if None in location:
        del location[None]
    if None in language:
        del language[None]
    language_count = dict(Counter(language).most_common(5))
    print("Language:")
    print(language_count)
    location_count = dict(Counter(location).most_common(5))
    print("Location:")
    print(location_count)
    time_zone_count = dict(Counter(time_zone).most_common(5))
    print("Time Zone:")
    print(time_zone_count)

# compare tweets
def compare():
    flagword = 0
    flagword1 = 0
    # for narendra modi
    tweets = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word=word.upper()
            if word == "AMERICA" or word == "US" or word=="USA" or word=="UNITED STATES OF AMERICA":
                flagword = flagword + 1
    print("USA BY NARENDRA MODI: "+ str(flagword))

    # for donald trump
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet = re.split(r"\s", cur_tweet)
        for word in cur_tweet:
            word = word.upper()
            if word == "INDIA" or word == "India" or word == "India":
                flagword1 = flagword1 + 1
    print("INDIA BY DONALD TRUMP: " + str(flagword1))

# analysing top usage
def top_usage():
    global count
    stop_words = set(stopwords.words('english'))
    x = [x.upper() for x in stop_words]
    tweets = api.user_timeline(screen_name="narendramodi", count=200, tweet_mode="extended")
    for tweet_compare in tweets:
        fulltext = tweet_compare.full_text
        tmp = []
        tmp.append(fulltext)
        temp = tmp
        import re
        cur_tweet = re.sub(r"http\S+", "", str(temp))
        cur_tweet1 = re.split(r"\s", cur_tweet)
        cur_tweet = [w for w in cur_tweet1 if not w in stop_words]
        cur_tweet=[]
        for w in cur_tweet1:
            if w not in stop_words:
                cur_tweet.append(w)
                count = Counter(cur_tweet).most_common(10)
        print(count)

#  updates status
def tweet_status(new):
    message = raw_input("What is the status that you want to set?")
    api.update_status(message)

print("Twitter Bot")
display_menu()