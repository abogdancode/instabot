# coding=utf-8
"""
    instabot example

    Workflow:
        Like medias by location.
"""

import argparse
import os
import sys
import codecs
import json

from tqdm import tqdm

stdout = sys.stdout
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot
import instabot

try:
    input = raw_input
except NameError:
    pass


def like_location_feed(new_bot, new_location, amount=0):
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
                        print('I have jast followed %s' % new_bot.get_username_from_userid(media_owner))
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
            max_likes_per_day=800,
            max_unlikes_per_day=0,
            max_follows_per_day=400,
            filter_users=True,
            max_followers_to_follow=1000,
            min_followers_to_follow=40,
            max_following_to_follow=1000,
            min_following_to_follow=20,
            max_followers_to_following_ratio=10,
            max_following_to_followers_ratio=1.5,
            max_following_to_block=1000,
            min_media_count_to_follow=3,
            follow_delay=60,
            whitelist=False,
            blacklist=False,
            comments_file=False,
            stop_words=['shop', 'store', 'free'])
bot.login(username=args.u, password=args.p,
          proxy=args.proxy)

if args.locations:
    for location in args.locations:
        print(u"Location: {}".format(location))
        bot.searchLocation(location)
        finded_location = bot.LastJson['items'][0]
        if finded_location:
            print(u"Found {}".format(finded_location['title']))

            if not args.amount:
                nlikes = input(u"How much likes per location?\n")
            else:
                nlikes = args.amount
            like_location_feed(bot, finded_location, amount=int(nlikes))
else:
    location_name = input(u"Write location name:\n").strip()
    bot.searchLocation(location_name)
    if not bot.LastJson['items']:
        print(u'Location was not found')
        exit(1)
    if not args.amount:
        nlikes = input(u"How much likes per location?\n")
    else:
        nlikes = args.amount
    ans = True
    while ans:
        for n, location in enumerate(bot.LastJson["items"], start=1):
            print(u'{0}. {1}'.format(n, location['title']))
        print(u'\n0. Exit\n')
        ans = input(u"What place would you want to choose?\n").strip()
        if ans == '0':
            exit(0)
        try:
            ans = int(ans) - 1
            if ans in range(len(bot.LastJson["items"])):
                like_location_feed(bot, bot.LastJson["items"][ans], amount=int(nlikes))
        except ValueError:
            print(u"\n Not valid choice. Try again")
