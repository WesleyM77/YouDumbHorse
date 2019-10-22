import tweepy
import requests
import os
from keys import consumer_key, consumer_secret, access_token, access_token_secret

# replace keys and tokens later on
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Function stolen from the intenet modified to reply directly to a tweet
def tweet_image(url, user, id):
    api = tweepy.API(auth)
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status="@"+user, in_reply_to_status_id=id)
        os.remove(filename)
    else:
        print("Unable to download image")

class rdtStreamListener(tweepy.StreamListener):

    # The list of statuses we checked/responded to
    statuses = []

    def on_status(self, status):
        try:
            self.statuses.index(status.id)
        except:
            if(status.author.screen_name == 'realDonaldTrump'):
                print(status.author.screen_name, " (", status.created_at, ") ", status.text)
                url = "https://raw.githubusercontent.com/WesleyM77/YouDumbHorse/master/youDumbHorse.png"
                tweet_image(url, status.author.screen_name, status.id)
                self.statuses.append(status.id)


rdtListener = rdtStreamListener()
stream = tweepy.Stream(auth = api.auth, listener = rdtListener)
# id(s) of user(s) we want to reply to. Need to check screen name in on_status of rdtStreamListener
stream.filter(follow=["25073877"])
