"""
    instabot example

    Workflow:
        Follow user's followers by username.
"""

import sys
import os
import time
import random
from tqdm import tqdm
import argparse

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot
from instabot.bot import limits
from instabot.bot import delay


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('users', type=str, nargs='+', help='users')
args = parser.parse_args()

bot = Bot(  filter_users=True,
            max_followers_to_follow=99999999,
            min_followers_to_follow=40,
            max_following_to_follow=99999999,
            min_following_to_follow=300,
            max_followers_to_following_ratio=0.5,
            max_following_to_followers_ratio=100000,
            max_following_to_block=99999999,
            min_media_count_to_follow=1,
            follow_delay=0,
            whitelist=False,
            blacklist=False,
            comments_file=False)
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

def console_print(verbosity, text):
    if verbosity:
        print(text)
        


def add_user_to_file(file_path,user_id):
    with open(str(file_path), 'a') as file:
        file.write(str(user_id) + "\n")

def get_list_of_followers_with_many_followings(self, user_id, nfollows=None):
    print('hello')
    file_path = '../user_ids/with_many_following.txt'
    self.logger.info("Follow followers of: %s" % user_id)
    if not user_id:
        self.logger.info("User not found.")
        return
    follower_ids = self.get_user_followers(user_id, nfollows)
    if not follower_ids:
        self.logger.info("%s not found / closed / has no followers." % user_id)
    else:
        present_user_ids = open(str(file_path)).read()
        for user_id in follower_ids:
            if user_id not in present_user_ids:
                if self.check_user(user_id):
                    add_user_to_file(file_path,user_id)
            else:
                self.logger.info("%s is present" % user_id)
                
for username in args.users:
    get_list_of_followers_with_many_followings(bot, username)




