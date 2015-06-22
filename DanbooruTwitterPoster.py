import requests
import pprint
import json
import ssl
import re
import urllib
import os.path
import string
import random
import re
from twython import Twython
import urllib3
from random import randint
from random import shuffle

#Some default options selected. Please configure in BotConfig.py instead
app_key = ""
app_secret = ""
oauth_token = ""
oauth_token_secret = ""
img_dir = "/var/DanbooruTwitterPoster/Images/"
enable_tweets = False
search_tags = ""
hashtags = ""
blacklist_tags = ""
score_minimum = 0
enable_ratingsafe = True
enable_ratingquestionable = False
enable_ratingexplicit = False
repeat_threshold = 24
#End of default options

from BotConfig import *


def postImage(htags, dblink, twurl, dbpf):
    print "Twitter Pic Post:\n\t" + (htags + " " + dblink)
    if enable_tweets == True:
        photo = open(img_dir + dbpf, 'rb')
        twitter.update_status_with_media(
            status=(htags +" "+ dblink), media=photo)
        print "Tweet was posted"
    else:
        print "Tweet was pretend-posted"
    return 1


def scramble(sentence):
    split = sentence.split()  # Split the string into a list of words
    shuffle(split)  # This shuffles the list in-place.
    return ' '.join(split)  # Turn the list back into a string


def addTags(htags, mtags):
    # print mtags
    length = 84
    str = mtags
    str = "%# " + string.replace(str, " ", "%# ")
    str = string.replace(str, "_", " ")
    str = str.title()
    str = string.replace(str, " ", "")
    str = string.replace(str, "/", "")
    str = string.replace(str, "%#", " #")
    str = re.sub('\(\w*\)', '', str)
    if not len(str) <= length - len(htags) - 1:
        str = scramble(str)
        str = ' ' + ' '.join(str[:length + 1].split(' ')[0:-1])
    str = htags + str
    # print str
    return str


file = open(img_dir + "submissions_log.txt", "r")
prevlogs = file.read()
file.close()
# print prevlogs

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
blacklist_tags_list = blacklist_tags.split()
tagrequest = requests.get(
    url='http://danbooru.donmai.us/tags.json?search[name]=' + search_tags)
tagdata = json.loads(tagrequest.text)
print "The tag(s) " + search_tags + " has a total of " + str(tagdata[0]["post_count"]) + " posts"
pagerange = tagdata[0]["post_count"] / 20
validpagetagsafe = 0
while(validpagetagsafe == 0):
    validpagerange = 0
    while(validpagerange == 0):
        randompageindex = randint(1, pagerange)
        print "Looking at Page " + str(randompageindex)
        pagerequest = requests.get(
            url='http://danbooru.donmai.us/posts.json?page=' + str(randompageindex) + '&tags=' + search_tags)
        resultspage = json.loads(pagerequest.text)
        # print len(resultspage)
        if len(resultspage) == 0:
            validpagerange = 0
        else:
            validpagerange = 1

            randomsubindex = randint(0, len(resultspage) - 1)
            iterated = 0
            validsub = 0

            while (validsub == 0):
                # print "Tags are " + resultspage[randomsubindex]["tag_string_general"]
                # print "Rating is " + resultspage[randomsubindex]["rating"]
                if any(word in resultspage[randomsubindex]["tag_string_general"] for word in blacklist_tags_list):
                    print "Result " + str(randomsubindex) + " contained a blacklisted tag. Choosing the next result..."
                    if randomsubindex < len(resultspage) - 1:
                        randomsubindex += 1
                    else:
                        randomsubindex = 0
                    iterated += 1
                    if iterated >= len(resultspage):
                        validsub = 2
                        validpagerange = 0

                elif (resultspage[randomsubindex]["rating"] == "q" and not enable_ratingquestionable) or (resultspage[randomsubindex]["rating"] == "s" and not enable_ratingsafe) or (resultspage[randomsubindex]["rating"] == "e" and not enable_ratingexplicit):
                    print "Result " + str(randomsubindex) + " was not within safety rating restriction"
                    if randomsubindex < len(resultspage) - 1:
                        randomsubindex += 1
                    else:
                        randomsubindex = 0
                    iterated += 1
                    if iterated >= len(resultspage):
                        validsub = 2
                        validpagerange = 0
                elif resultspage[randomsubindex]["score"] < score_minimum:
                    print "Result " + str(randomsubindex) + " failed to meet the minimum score"
                    if randomsubindex < len(resultspage) - 1:
                        randomsubindex += 1
                    else:
                        randomsubindex = 0
                    iterated += 1
                    if iterated >= len(resultspage):
                        validsub = 2
                        validpagerange = 0
                elif str(resultspage[randomsubindex]["id"]) in prevlogs:
                    print "Result " + str(randomsubindex) + " has already been posted in the last " + str(repeat_threshold) + " tweets"
                    if randomsubindex < len(resultspage) - 1:
                        randomsubindex += 1
                    else:
                        randomsubindex = 0
                    iterated += 1
                    if iterated >= len(resultspage):
                        validsub = 2
                        validpagerange = 0
                else:
                    print "Result " + str(randomsubindex) + " doesn't contain a blacklisted tag and is within rating restrictions"

                    danboorupiclink = "http://danbooru.donmai.us" + \
                        resultspage[randomsubindex]["file_url"]
                    danboorulink = "http://danbooru.donmai.us/posts/" + \
                        str(resultspage[randomsubindex]["id"])
                    danboorupic = resultspage[randomsubindex][
                        "file_url"].split('/')[-1]
                    moretags = ''
                    if not os.path.exists(img_dir + resultspage[randomsubindex]["file_url"].split('/')[-1]):
                        urllib.urlretrieve("http://danbooru.donmai.us" + resultspage[randomsubindex][
                                           "file_url"], img_dir + resultspage[randomsubindex]["file_url"].split('/')[-1])
                    tweettags = addTags(
                        hashtags, resultspage[randomsubindex]["tag_string_character"])
                    posted = postImage(
                        tweettags, danboorulink, danboorupiclink, danboorupic)

                    file = open(img_dir + "submissions_log.txt", "w+")
                    newlogs = str(resultspage[randomsubindex]["id"]).ljust(
                        10) + "%\n" + prevlogs
                    newlogs = newlogs[:(12 * repeat_threshold)]
                    # print "Log of the Danbooru IDs posted:\n\n"+newlogs
                    file.write(newlogs)
                    file.close()

                    validsub = 1
                    validpagerange = 1
                    validpagetagsafe = 1
    if validpagetagsafe == 0:
        print "No results on page " + str(randompageindex) + "was suitable to post. Querying for another page"
        