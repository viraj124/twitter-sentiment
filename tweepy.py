import sentiment as s
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json






#consumer key, consumer secret, access token, access secret.
ckey="lj46PvfG83yRIVTdAVkLCZKIs"
csecret="AbyiwQkq4pEDzN3wQR5634rDlMQxnxk5JNlNFA54PL4f1HxgPc"
atoken="990818729117306881-x4tjdfivmtXFb8Fzxyqg3SrBjlERqxN"
asecret="j3BiXlwNzLTzBH4FV0EmsfCGICXsk8xVJOioWBJTxGCKZ"

class listener(StreamListener):
   def on_data(self, data):
       try:
         all_data = json.loads(data)
        
         tweet = all_data["text"]
         review,confi=s.sentiment(tweet)
         print(tweet,review,confi)
         if confi>=80:
            file=open("tweets.txt","a")
            file.write(review)
            file.write('\n')
            file.close()
        
         return True
       except:
          return True

     
def on_error(self, status):
            return True

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["india"])
