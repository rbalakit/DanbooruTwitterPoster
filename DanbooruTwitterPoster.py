import requests
import pprint
import json
import ssl
import re
import urllib
import os
import string
import random
import sys
from twython import Twython
import urllib3
from random import randint
from random import shuffle
import ConfigParser


universal_g = "pregnant diaper inflation panties guro scat peeing comic bikini chastity_belt trefoil undressing spread_legs pussy nipples censored cum nude sex facial vaginal cum_on_body convenient_censoring bottomless covering_breasts groin nude cameltoe panty_lift french_kiss underboob between_breasts lingerie ebola navel_cutout partially_visible_vulva ball_gag bdsm bondage gag gagged "

artist_blacklist = "khee cactuskhee"

#Some default options selected. Please configure in BotConfig.py instead
app_key = ""
app_secret = ""
oauth_token = ""
oauth_token_secret = ""
img_dir = ""
enable_tweets = True
search_tags = ""
hashtags = ""
blacklist_tags = ""
score_minimum = 0
enable_ratingsafe = True
enable_ratingquestionable = False
enable_ratingexplicit = False
repeat_threshold = 24
blacklist_rating = ""
#End of default options

#from DanBotConfig import *

configdefined = False
config = ConfigParser.ConfigParser()
if len(sys.argv) >= 2:
    w = 0
    for arg in sys.argv:
        if w > 0:
            if ".ini" in str(sys.argv[w]):
                config.read(str(sys.argv[w]))
                configdefined = True
            else:
                print("You wrote a garbage argument!")
        w += 1
if configdefined == False:
    config.read("config.ini")

app_key = config.get("configuration", "app_key")
app_secret = config.get("configuration", "app_secret")
oauth_token = config.get("configuration", "oauth_token")
oauth_token_secret = config.get("configuration", "oauth_token_secret")
img_dir = config.get("configuration", "img_dir")
enable_tweets = config.getboolean("configuration", "enable_tweets")
repeat_threshold = config.getint("configuration", "repeat_threshold")
search_tags = config.get("configuration", "search_tags")
blacklist_tags = config.get("configuration", "blacklist_tags")
hashtags = config.get("configuration", "hashtags")
score_minimum = config.getint("configuration", "score_minimum")
enable_ratingsafe = config.getboolean("configuration", "enable_ratingsafe")
enable_ratingquestionable = config.getboolean("configuration", "enable_ratingquestionable")
enable_ratingexplicit = config.getboolean("configuration", "enable_ratingexplicit")

if (enable_ratingquestionable == False and enable_ratingexplicit == False):
    #blacklist_tags.append(universal_g)
    uniquer = blacklist_tags + universal_g
    print "Automatically adding safe tags"
    uniquer = ' '.join(set(uniquer.split(' ')))
    print uniquer
    blacklist_tags = uniquer

#Hashtag to include at the beginning of the twitter post"
def postImage(htags, dblink, twurl, dbpf):
    print "Twitter Pic Post:\n\t" + (htags + " " + dblink)
    if enable_tweets == True:
        photo = open(img_dir + dbpf, 'rb')
        twitter.update_status_with_media(
            status=(htags +" "+ dblink), media=photo)
        print "Tweet was posted"
    else:
        print "Tweet was pretend-posted"
    os.remove(img_dir + dbpf)
    return 1


def scramble(sentence):
    split = sentence.split()  # Split the string into a list of words
    shuffle(split)  # This shuffles the list in-place.
    return ' '.join(split)  # Turn the list back into a string


def addTags(htags, mtags):
    # print mtags
    length = 70
    # str = mtags
    regex = re.compile('\(.+?\)')
    str = regex.sub('', mtags)
    str = "%# " + string.replace(str, " ", "%# ")
    str = string.replace(str, "_", " ")
    str = string.replace(str, "-", "")
    str = str.title()
    str = string.replace(str, " ", "")
    str = string.replace(str, "%#", " #")
    str = re.sub('\(*\)', '', str)
    if not len(str) <= length - len(htags) - 1:
        str = scramble(str)
        str = ' ' + ' '.join(str[:length + 1].split(' ')[0:-1])
    str = htags + str
    # print str
    return str


file = open(img_dir + "submissions_log.txt", "a+")
prevlogs = file.read()
file.close()
# print prevlogs
hashtags = hashtags.decode('UTF-8')
print hashtags

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)
blacklist_tags_list = blacklist_tags.split()
#twitter.update_profile(url="picbots.moe")
#if (enable_ratingquestionable == False and enable_ratingexplicit == False):
#twitter.update_profile(description = "[SFW] run by @pearlgreymusic, DM pearl for complains & feedback. stats, info, & artist removal requests at http://picbots.moe")
#else:
#twitter.update_profile(description = "[NSFW] run by @pearlgreymusic, DM pearl for complains & feedback. stats, info, & artist removal requests at http://picbots.moe")
tagrequest = requests.get(
    url='http://danbooru.donmai.us/tags.json?search[name]=' + search_tags)
tagdata = json.loads(tagrequest.text)
print "The tag(s) " + search_tags + " has a total of " + str(tagdata[0]["post_count"]) + " posts"
pagerange = tagdata[0]["post_count"] / 20
if pagerange > 1000:
    pagerange = 1000
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

                print "Artist is " + resultspage[randomsubindex]["tag_string_artist"]
                if any(word in resultspage[randomsubindex]["tag_string_artist"] for word in artist_blacklist):
                    print "Result " + str(randomsubindex) + "was by a blacklisted artist"
                    if randomsubindex < len(resultspage) - 1:
                        randomsubindex += 1
                    else:
                        randomsubindex = 0
                    iterated += 1
                    if iterated >= len(resultspage):
                        validsub = 2
                        validpagerange = 0


                resultspage[randomsubindex]["tag_string_artist"]
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
                    print "Result " + str(randomsubindex) + " doesn't contain a blacklisted tag and is within rating restrictions " + resultspage[randomsubindex]["source"]

                    danboorupiclink = "http://danbooru.donmai.us" + \
                        resultspage[randomsubindex]["file_url"]
                    danboorulink = "http://danbooru.donmai.us/posts/" + \
                        str(resultspage[randomsubindex]["id"])
                    page = requests.get(danboorulink)
                    chopfront = (page.text).split('<li>Source: <a href="', 1)[-1]
                    chopback = chopfront.split('">', 1)[0]
                    # print chopback
                    danboorupic = resultspage[randomsubindex][
                        "file_url"].split('/')[-1]
                    moretags = ''

                    if not os.path.exists(img_dir + resultspage[randomsubindex]["file_url"].split('/')[-1]):
                        urllib.urlretrieve("http://danbooru.donmai.us" + resultspage[randomsubindex][
                                           "file_url"], img_dir + resultspage[randomsubindex]["file_url"].split('/')[-1])
                    tweettags = addTags(
                        hashtags, resultspage[randomsubindex]["tag_string_character"])

                    if "pixiv" in chopback or "deviantart" in chopback or "twitter" in chopback or "tumblr" in chopback:
                        posted = postImage(
                            tweettags, chopback, danboorupiclink, danboorupic)
                    else:
                        print "source URL is not on the whitelist"
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
