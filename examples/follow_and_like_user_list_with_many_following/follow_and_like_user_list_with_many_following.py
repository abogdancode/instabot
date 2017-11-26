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

bot = Bot(
            proxy=None,
            max_likes_per_day=800,
            max_unlikes_per_day=0,
            max_follows_per_day=400,
            max_unfollows_per_day=0,
            filter_users=False,
            like_delay=20,
            follow_delay=45,
            whitelist=False,
            blacklist=False,
            comments_file=False
)
bot.login()

file_path = '../user_ids/with_many_following.txt'

def remove_user_from_file(file_path,user_id):
    f = open(str(file_path)).read()
    f = f.replace(str(user_id) + '\n','')
    with open(str(file_path),'w') as F:
        F.writelines(f)


follow_followers_list = bot.read_list_from_file(str(file_path))

tasks_list = []
count = 0
count_likes_prev = 0
count_likes_next = 0
for user_id in follow_followers_list:
        count = count+1
        if bot.like_user(user_id,4) == []:
            bot.follow(user_id)
        remove_user_from_file(file_path,user_id)
        print('user id %s has been removed from file' % user_id)
        if count >50:
            print('reload list!')
            follow_followers_list = bot.read_list_from_file(str(file_path))
            count =0





