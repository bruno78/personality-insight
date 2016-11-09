import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights
from config import *


# Interact with Twitter API
twitter_api = twitter.Api(consumer_key = twitter_consumer_key, consumer_secret = twitter_consumer_secret,
access_token_key = twitter_access_token,
access_token_secret = twitter_access_secret)

# This handles will be replaced for a user input raw_input
handle = '@Codecademy' #'@realDonaldTrump'

# this will retrieve user status
statuses = twitter_api.GetUserTimeline(screen_name=handle, count=1, include_rts=False)

# this will be used to store the concatenated twitter posts
text = ""

for status in statuses:
    if (status.lang == 'en'):
        text += status.text.encode('utf-8')
