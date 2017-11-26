# -*- coding: utf-8 -*-
"""
    instabot example

    Workflow:
    1) likes your timeline feed
    2) likes user's feed

    Notes:
    1) You should pass user_id, not username
"""

import time
import sys
import os

sys.path.append(os.path.join(sys.path[0], '../../'))
from instabot import Bot
from instabot.bot import delay
bot = Bot(comment_delay = 10)
bot.login()


def delete_comment(self, media_id, comment_id):
    if super(self.__class__, self).deleteComment(media_id, comment_id):
        delay.small_delay(self)
        return True
    self.logger.info("Comment with %s in media %s is not deleted." % (comment_id, media_id))
    return False


needed_text = '#лофт #хобби #мастерская #стильлофт #своимируками'

my_medias = bot.get_your_medias()

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
