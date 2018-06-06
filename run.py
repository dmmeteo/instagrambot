# -*- coding: utf-8 -*-

from glob import glob
import os
import threading
import time
import schedule
from instabot import Bot, utils
import config


bot = Bot(comments_file=config.COMMENTS_FILE,
          friends_file=config.FRIENDS_FILE)
bot.login()
bot.logger.info("Instagram bot. Safe to run 24/7!")

random_user_file = utils.file(config.USERS_FILE)
random_hashtag_file = utils.file(config.HASHTAGS_FILE)


def stats():
    bot.save_user_stats(bot.user_id)


def like_hashtags():
    bot.like_hashtag(random_hashtag_file.random(), amount=700 // 24)


def like_timeline():
    bot.like_timeline(amount=300 // 24)


def like_followers_from_random_user_file():
    bot.like_followers(random_user_file.random(), nlikes=3)


def follow_followers():
    bot.follow_followers(random_user_file.random(), nfollows=config.NUMBER_OF_FOLLOWERS_TO_FOLLOW)


def comment_medias():
    bot.comment_medias(bot.get_timeline_medias())


def unfollow_non_followers():
    bot.unfollow_non_followers(n_to_unfollows=config.NUMBER_OF_NON_FOLLOWERS_TO_UNFOLLOW)


def follow_users_from_hastag_file():
    bot.follow_users(bot.get_hashtag_users(random_hashtag_file.random()))




def run_threaded(job_fn):
    job_thread = threading.Thread(target=job_fn)
    job_thread.start()


schedule.every(1).minutes.do(run_threaded, stats)
schedule.every(1).minutes.do(run_threaded, like_hashtags)
schedule.every(1).minutes.do(run_threaded, unfollow_non_followers)
schedule.every(1).minutes.do(run_threaded, follow_users_from_hastag_file)

while True:
    schedule.run_pending()
    time.sleep(1)
