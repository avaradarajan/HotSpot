##########################################################################
## GetTweets.py v0.1
##
## Get/Scrape all the tweets using GetOldTweets3 library as the Tweepy API gives data only for latest 7 days
## Here we extracted all the tweets for a specific time range and working with the subset
##
## Team Name: ANA
## Team Members : Anandh Varadarajan, Nithish Kolli, Abhiram Karri
##########################################################################

import GetOldTweets3 as got
#tweetCriteria = got.manager.TweetCriteria().setQuerySearch("vehicle OR crash OR road OR accident OR hit OR collision OR casualty OR mishap OR ambulance OR traffic").setSince("2014-12-31").setUntil("2015-01-01").setNear('England').setWithin('46814mi')#.setMaxTweets(10)
tweetCriteria = got.manager.TweetCriteria().setSince("2014-12-30").setUntil("2014-12-31").setNear('England').setWithin('46814mi')#.setMaxTweets(10)

tweet = got.manager.TweetManager.getTweets(tweetCriteria)

for tw in tweet:
    print(tw.text)
#Write all the tweets extracted to the csv file
with open('train.csv','a+',encoding="utf-8") as file:
    for tw in tweet:
        print(tw.text)
        file.write(tw.text.replace(',','')+'\n')
file.close()
