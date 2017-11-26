"""
    ULTIMATE SCRIPT

    It uses data written in files:
        * follow_followers.txt
        * follow_following.txt
        * like_hashtags.txt
        * like_users.txt
    and do the job. This bot can be run 24/7.
"""

import os
import sys
import time
from random import shuffle

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot

bot = Bot(proxy=None,
            max_likes_per_day=360,
            max_unlikes_per_day=1000,
            max_follows_per_day=120,
            max_unfollows_per_day=350,
            max_comments_per_day=100,
            max_likes_to_like=100,
            filter_users=True,
            max_followers_to_follow=2000,
            min_followers_to_follow=40,
            max_following_to_follow=7500,
            min_following_to_follow=150,
            max_followers_to_following_ratio=0.9,
            max_following_to_followers_ratio=99999999,
            max_following_to_block=99999999,
            min_media_count_to_follow=3,
            like_delay=25,
            unlike_delay=10,
            follow_delay=60,
            unfollow_delay=30,
            comment_delay=60,
            whitelist=False,
            blacklist=False,
            comments_file=False,
            stop_words=['shop', 'store', 'free'])
bot.login()

print("Current script's schedule:")
follow_followers_list = bot.read_list_from_file("follow_followers.txt")
print("Going to follow followers of:", follow_followers_list)
follow_following_list = bot.read_list_from_file("follow_following.txt")
print("Going to follow following of:", follow_following_list)
like_hashtags_list = bot.read_list_from_file("like_hashtags.txt")
print("Going to like hashtags:", like_hashtags_list)
like_users_list = bot.read_list_from_file("like_users.txt")
print("Going to like users:", like_users_list)

tasks_list = []
counter = 0
#for item in follow_followers_list:
#    tasks_list.append((bot.follow_followers, {'user_id': item, 'nfollows': None}))
#for item in follow_following_list:
#    tasks_list.append((bot.follow_following, {'user_id': item}))
#for item in like_hashtags_list:
#    tasks_list.append((bot.like_hashtag, {'hashtag': item, 'amount': None}))
#for item in like_users_list:
#    tasks_list.append((bot.like_user, {'user_id': item, 'amount': None}))

# shuffle(tasks_list)
#for func, arg in tasks_list:
#    func(**arg)

likes_for_each_hash = input(u"How many follows per one hashtag?\n")

for one_hash in like_hashtags_list:
    counter = 0
    medias_list = bot.get_hashtag_medias(one_hash)
    for one_media in medias_list:
        if counter < likes_for_each_hash:
            media_owner = bot.get_media_owner(one_media)
            if bot.check_user(media_owner):
                bot.like_user(media_owner,3)
                bot.follow(media_owner)
                counter += 1
            
        



