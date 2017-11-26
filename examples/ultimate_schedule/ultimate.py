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

sys.path.append(os.path.join(sys.path[0],'../../'))
from instabot import Bot

bot = Bot(comments_file="comments.txt", blacklist="blacklist.txt",
          proxy=None,
            max_likes_per_day=300,
            max_unlikes_per_day=1000,
            max_follows_per_day=75,
            max_unfollows_per_day=80,
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
            like_delay=30,
            unlike_delay=30,
            follow_delay=60,
            unfollow_delay=150,
            comment_delay=120,
            whitelist=False,
            stop_words=['shop', 'store', 'free'])
bot.login()
bot.logger.info("ULTIMATE script. 24hours save")

comments_file_name = "comments.txt"
random_user_file = bot.read_list_from_file("username_database.txt")
random_hashtag_file = bot.read_list_from_file("hashtag_database.txt")

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

def stats(): bot.save_user_stats(bot.user_id)
def job1(): bot.like_hashtag(get_random(random_hashtag_file), amount=int(700/24))
def job2(): bot.like_timeline(amount=int(300/18))
def job3(): bot.like_followers(get_random(random_user_file), nlikes=3)
def job4(): bot.follow_followers(get_random(random_user_file))
def job5(): bot.comment_medias(bot.get_timeline_medias())
def job6(): bot.unfollow_non_followers()
def job7(): bot.follow_users(bot.get_hashtag_users(get_random(random_hashtag_file)))
def job8(): #-->fn to upload photos /auto_uploader
    try:
        for pic in pics:
            if pic in posted_pic_list:
                continue
            hashtags = "/>\n​​#instabot #vaskokorobko #kyiv"       #add custom hashtags
            caption = pic[:-4].split(" ")                        #caption is made from the name of file
            caption = " ".join(caption[1:])
            caption = "\n<" + caption + hashtags                 #create full caption with hashtags
            print("upload: " + caption)
            bot.uploadPhoto(pic, caption=caption)
            if bot.LastResponse.status_code != 200:
                print("Smth went wrong. Read the following ->\n")
                print(bot.LastResponse)
                # snd msg
                break

            if not pic in posted_pic_list:
                posted_pic_list.append(pic)
                with open('pics.txt', 'a') as f:
                    f.write(pic + "\n")
                print("Succsesfully uploaded: " + pic)
                break
    except Exception as e:
        print(str(e))
# end of job8


def job9():  # put non followers on blacklist
    try:
        print("Creating Non Followers List")
        followings = bot.get_user_following(bot.user_id)  # getting following
        followers = bot.get_user_followers(bot.user_id)  # getting followers
        friends_file = bot.read_list_from_file("friends.txt")  # same whitelist (just user ids)
        nonfollowerslist = list((set(followings) - set(followers)) - set(friends_file))
        with open('blacklist.txt', 'a') as file:  # writing to the blacklist
            for user_id in nonfollowerslist:
                file.write(str(user_id) + "\n")
        print("removing duplicates")
        lines = open('blacklist.txt', 'r').readlines()
        lines_set = set(lines)
        out = open('blacklist.txt', 'w')
        for line in lines_set:
            out.write(line)
        print("Task Done")
    except Exception as e:
        print(str(e))


# function to make threads -> details here http://bit.ly/faq_schedule
def run_threaded(job_fn):
    job_thread=threading.Thread(target=job_fn)
    job_thread.start()

follows_for_each_hash = 300/10
def like_and_follow_hash():
    one_hash = get_random(random_hashtag_file)
    counter = 0
    medias_list = bot.get_hashtag_medias(one_hash)
    for one_media in medias_list:
        if counter < follows_for_each_hash:
            media_owner = bot.get_media_owner(one_media)
            if bot.check_user(media_owner):
                bot.like_user(media_owner,3)
                bot.follow(media_owner)
                counter += 1

def delete_comment(self, media_id, comment_id):
    if super(self.__class__, self).deleteComment(media_id, comment_id):
        delay.small_delay(self)
        return True
    self.logger.info("Comment with %s in media %s is not deleted." % (comment_id, media_id))
    return False

needed_text = '#лофт #хобби #мастерская #стильлофт #своимируками'

my_medias = bot.get_your_medias()

def reload_comments():
    for media_id in my_medias:
        comment_list = bot.get_media_comments(media_id)
        for comment_item in comment_list:
            if comment_item["text"].encode('utf-8') == needed_text:
                print(comment_item["text"].encode('utf-8'))
                print(comment_item["pk"])
                comment_id = comment_item["pk"]
                delete_comment( bot, media_id, comment_id)
    for media_id in my_medias:
        bot.comment(media_id, needed_text)


#---------------------like timeline--------------------------#
schedule.every(1).days.at("07:30").do(run_threaded, job2)
schedule.every(1).days.at("08:30").do(run_threaded, job2)
schedule.every(1).days.at("09:30").do(run_threaded, job2)
schedule.every(1).days.at("10:30").do(run_threaded, job2)
schedule.every(1).days.at("11:30").do(run_threaded, job2)
schedule.every(1).days.at("12:30").do(run_threaded, job2)
schedule.every(1).days.at("13:30").do(run_threaded, job2)
schedule.every(1).days.at("14:30").do(run_threaded, job2)
schedule.every(1).days.at("15:30").do(run_threaded, job2)
schedule.every(1).days.at("16:30").do(run_threaded, job2)
schedule.every(1).days.at("17:30").do(run_threaded, job2)
schedule.every(1).days.at("18:30").do(run_threaded, job2)
schedule.every(1).days.at("19:30").do(run_threaded, job2)
schedule.every(1).days.at("20:30").do(run_threaded, job2)
schedule.every(1).days.at("21:30").do(run_threaded, job2)
schedule.every(1).days.at("22:30").do(run_threaded, job2)
schedule.every(1).days.at("23:30").do(run_threaded, job2)
schedule.every(1).days.at("00:30").do(run_threaded, job2)
schedule.every(1).days.at("01:30").do(run_threaded, job2)
#---------------------END like timeline---------------------#

#---------------------like and follow hash------------------#
schedule.every(1).days.at("07:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("09:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("11:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("13:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("15:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("17:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("19:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("21:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("23:00").do(run_threaded, like_and_follow_hash)
schedule.every(1).days.at("01:00").do(run_threaded, like_and_follow_hash)
#---------------------END like and follow hash--------------#


#---------------------unfollow non-followers------------------#
schedule.every(1).days.at("03:30").do(run_threaded, job6)
#---------------------END unfollow non-followers--------------#

#---------------------reload hashtag comments to my medias--------------#
schedule.every(1).days.at("15:00").do(run_threaded, reload_comments)
#---------------------END reload hashtag comments to my medias----------#

#---------------------get stats--------------------------------#
schedule.every(1).hour.do(run_threaded, stats)
#---------------------END get stats----------------------------#

#maybe will be needed later...
#schedule.every(1).days.at("16:00").do(run_threaded, job3)   #like followers of users from file
#schedule.every(2).days.at("11:00").do(run_threaded, job4)   #follow followers
#schedule.every(16).hours.do(run_threaded, job5)             #comment medias
#schedule.every(12).hours.do(run_threaded, job7)             #follow users from hashtag from file
#schedule.every(1).days.at("21:28").do(run_threaded, job8)   #upload pics
#schedule.every(4).days.at("07:50").do(run_threaded, job9)   #non-followers blacklist
                  
while True:
    schedule.run_pending()
    time.sleep(1)
