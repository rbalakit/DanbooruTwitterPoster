[configuration]
#CONFIGURATION
#This is for your Twitter App keys
app_key: 
app_secret: 
oauth_token: 
oauth_token_secret: 
#Images Directory, which should look similar to /var/DanbooruTwitterPoster/images/
img_dir: /var/NicoBot/DanImages/Kongou/
#Enables if the bot actually posts to twitter. Useful for testing with prints instead of spamming your followers (True/False)
enable_tweets: True
#Sets the number of tweets before a submission may be reposted. Recommended no higher than either a quarter of the total search results for your tag (Integer)
repeat_threshold: 48
#Tags to search for in Danbooru (Must follow the formatting) (Exclusive rating tags and blacklist tags) (Limited to up to 2 for now...) Separate by spaces.
search_tags: kongou_(kantai_collection)
#Tags to blacklist from posting. Separate by spaces.
blacklist_tags: pregnant diaper inflation guro scat peeing comic chastity_belt
#Hashtag to include at the beginning of the twitter post
hashtags: #KanColle
#Minimum score a danbooru post must have to be posted
score_minimum: 0
#Choose which ratings may be posted
enable_ratingsafe: True
enable_ratingquestionable: False
enable_ratingexplicit: False
