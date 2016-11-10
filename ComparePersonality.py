import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights
from config import *

def analyze(handle):

    # Interact with Twitter API
    twitter_api = twitter.Api(consumer_key = twitter_consumer_key, consumer_secret = twitter_consumer_secret,
    access_token_key = twitter_access_token,
    access_token_secret = twitter_access_secret)

    # this will retrieve user status
    statuses = twitter_api.GetUserTimeline(screen_name=handle, count=1200, include_rts=False)

    # this will be used to store the concatenated twitter posts
    text = ""

    for status in statuses:
        if (status.lang == 'en'):
            text += status.text.encode('utf-8')

    # The IBM Bluemix credentials for Personality Insights
    pi_username = username
    pi_password = password

    personality_insights = PersonalityInsights(username = pi_username, password = pi_password)

    pi_result = personality_insights.profile(text)

    return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                            data[c3['id']] = c3['percentage']
    return data

def compare(dict1, dict2):
    compared_data = {}
    for keys in dict1:
        if dict1[keys] != dict2[keys]:
            compared_data[keys] = abs(dict1[keys] - dict2[keys])
    return compared_data

user_handle =  "@HillaryClinton"
celebrity_handle = "@realDonaldTrump"

user_result = analyze(user_handle)
celebrity_result = analyze(celebrity_handle)
print user_result
# First, flatten the results from the Watson PI API
hillary = flatten(user_result)
donald = flatten(celebrity_result)

# Compare the results for the Watson PI API by calculating the distance between traits
compared_results = compare(hillary, donald)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

hillary
for keys, value in sorted_result[:5]:
    print keys,":"
    print('Hillary'),
    print(hillary[keys]),
    print('Donald'),
    print(donald[keys])
    print('Compared results:')
    print ('->'),
    print(compared_results[keys])

print ""
print "Now saving into a json file..."



# Writes JSON data into a .json file
with open('hillary.json', 'w') as f:
    json.dump(hillary, f)

with open('trump.json', 'w') as f:
    json.dump(donald, f)

with open('hillary_raw.json', 'w') as f:
    json.dump(user_result, f)

with open('trump_raw_data.json', 'w') as f:
    json.dump(celebrity_result, f)

print "...done!"
