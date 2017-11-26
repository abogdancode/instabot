# -*- coding: utf-8 -*-
import schedule
import time
import sys
import os
import random
import yaml             #->added to make pics upload -> see job8
import glob             #->added to make pics upload -> see job8
from tqdm import tqdm
import threading        #->added to make multithreadening possible -> see fn run_threaded

import argparse
import codecs
import json

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot
import instabot

try:
    input = raw_input
except NameError:
    pass

def like_and_follow_location_feed(new_bot, new_location, amount=0):
    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if new_bot.getLocationFeed(new_location['location']['pk'], maxid=max_id):
                location_feed = new_bot.LastJson
                for media in new_bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    media_owner = new_bot.get_media_owner(media)
                    if bot.check_user(media_owner):
                        bot.like_user(media_owner,4)
                        bot.follow(media_owner)
                        print('I have just followed %s  -- counter is %d' % (new_bot.get_username_from_userid(media_owner), counter))
                        counter += 1
      
                if location_feed.get('next_max_id'):
                    max_id = location_feed['next_max_id']
                else:
                    return False
    return True

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-u', type=str, help="username")
parser.add_argument('-p', type=str, help="password")
parser.add_argument('-amount', type=str, help="amount")
parser.add_argument('-proxy', type=str, help="proxy")
parser.add_argument('locations', type=str, nargs='*', help='locations')
args = parser.parse_args()


try:
    print(u'Like medias by location')
except TypeError:
    sys.stdout = stdout

    
bot = Bot(
            max_likes_per_day=150,
            max_unlikes_per_day=0,
            max_follows_per_day=50,
            filter_users=True,
            max_followers_to_follow=5000,
            min_followers_to_follow=200,
            max_following_to_follow=99999999,
            min_following_to_follow=600,
            max_followers_to_following_ratio=0.4,
            max_following_to_followers_ratio=100000,
            max_following_to_block=99999999,
            min_media_count_to_follow=1,
            follow_delay=75,
            like_delay=45,
            whitelist=False,
            blacklist=False,
            stop_words=['shop', 'store', 'free','bot','follow'])

bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

bot.logger.info("ULTIMATE script. 24hours save")

comments_file_name = "comments.txt"
random_user_file = bot.read_list_from_file("username_database.txt")
random_hashtag_file = bot.read_list_from_file("hashtag_database.txt")

def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

#to get pics and autopost it
posted_pic_list = []
try:
    with open('pics.txt', 'r') as f:
        posted_pic_list = f.read().splitlines()
except:
    posted_pic_list = []
#!!-> to work this feature properly write full/absolute path to .jgp files as follows ->v
pics = glob.glob("/home/user/instagram/instabot/examples/ultimate_schedule/pics/*.jpg")  #!!change this
pics = sorted(pics)
#end of pics processing

#fn to return random value for separate jobs
def get_random(from_list):
    _random=random.choice(from_list)
    print("Random from ultimate.py script is chosen: \n" + _random + "\n")
    return _random           

def like_and_follow_users_by_location():
    if args.locations:
        for location in args.locations:
            print(u"Location: {}".format(location))
            bot.searchLocation(location)
            finded_location = bot.LastJson['items'][0]
            if finded_location:
                print(u"Found {}".format(finded_location['title']))

                if not args.amount:
                    nlikes = 250
                else:
                    nlikes = args.amount
                like_and_follow_location_feed(bot, finded_location, amount=int(nlikes))
    else:
        print(u"\n Not valid Location. Try again")


#---------------------like_and_follow_humans_by_location------------------#
schedule.every(1).days.at("07:30").do(run_threaded, like_and_follow_users_by_location)
#---------------------like_and_follow_humans_by_location------------------#

                  
while True:
    schedule.run_pending()
    time.sleep(1)
