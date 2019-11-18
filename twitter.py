import sys
import tweepy
import http_request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
import dao
from datetime import datetime
import pytz
import telegram

Q = sys.argv[1:]

CONSUMER_KEY = 'Xa1hk2E9b2JDkJK3a71Y8RWq0'
CONSUMER_SECRET = 'xzVOwRIdO4qDN1CQZ1hP3dDbhuWuFJoUoVNeFuipTzRiadqXRR'

ACCESS_TOKEN = '968302017830707201-O2OmNGw8aF5ydIDF97gMBGTHwlBqqB9'
ACCESS_TOKEN_SECRET = 'P8fqdUgdtRKfLb5S4abM2aYL6JMaCW8PyisGFMtDAzlYs'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

links = []


def checkLinkExists(href):
    if len(links) == 0:
        return False
    for tw in links:
        if tw == href:
            return True
    return False


URL_GETID = "https://tweeterid.com/ajax.php"


def get_twitter_info(ref):
    try:
        url = "https://coinmarketcap.com%s" % ref
        print(url)
        open = urlopen(url)
        page = BeautifulSoup(open, 'html.parser')
        # print(page)
        twitter = page.find_all('a', class_='twitter-timeline', text=True)
        twitter = str(re.sub("<.*?>", "", str(twitter)))
        twitter = twitter.replace("[Tweets by ", "")
        twitter = twitter.replace("]", "")
        print("start get tw id for %s " % str(twitter))
        twitter_id = http_request.sendPost(URL_GETID, twitter)
        print("twitter_id %s " % str(twitter_id))
        dao.insertTwitter(twitter, twitter_id)
    except Exception as e:
        print(e)
        links.append(ref)
        time.sleep(30)


def get_twitter():
    try:
        url = "https://coinmarketcap.com/exchanges/binance/"
        open = urlopen(url)
        page = BeautifulSoup(open, 'html.parser')
        # print(page)
        twitters = page.find_all('a', class_='margin-left--lv1 link-secondary')
        for tw in twitters:
            href = tw.attrs.get("href")
            if (checkLinkExists(href=href)) == False:
                links.append(href)

        for tw in links:
            get_twitter_info(tw)
            time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(30)


# get_twitter()

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            authorId = status.author.id
            in_reply_to_status_id = status.in_reply_to_status_id
            text = status.text
            if dao.checkExists(authorId) and in_reply_to_status_id is None \
                    and text.startswith("RT @") == False:
                twId = status.id
                screen_name = status.author.screen_name
                sourceLink = "https://twitter.com/%s/status/%s" % (screen_name, twId)
                text = status.text
                # timest = int(status.timestamp_ms) / 1000
                # create_at_tm = datetime.fromtimestamp(timest, tz=pytz.timezone("Asia/Ho_Chi_Minh")).strftime(
                #     '%Y-%m-%d %H:%M:%S')
                symbol = dao.getSymbol(authorId)
                if symbol is None:
                    symbol = screen_name

                try:
                    symbol = symbol.decode()
                except Exception as e:
                    print(e)

                message = "<b>#%s</b>\n%s\n\n<a href='%s'>Source</a>" % (symbol, text, sourceLink)
                # 468847123
                # @aztoolChannelFollowTwitter

                textLower = text.lower()
                keywords = dao.getKeyword()
                for keyword in keywords:
                    try:
                        keyword = keyword[0].decode().lower()
                    except Exception as e:
                        keyword = keyword[0].lower()

                    isValidKeyword = keyword in textLower
                    if isValidKeyword:
                        telegram.sendMessage(message, '@aztool_ignore_spam')
                        break

                telegram.sendMessage(message, '@aztool_twitter')
            else:
                print("I dont care tw of %s " % status.author.screen_name)
        except Exception as e:
            print("Encountered Exception: %s " % e)
            pass

    def on_error(self, status_code):
        print("Encountered error with status code:%s " % status_code)
        return True  # Don't kill the stream

    def on_timeout(self):
        print("time out ")
        return True  # Don't kill the stream


def run_main():
    usernames = dao.getAllUsername()
    usernameArr = []
    if usernames is not None:
        for us in usernames:
            usernameArr.append(str(us[0]))

        print(usernameArr)

        streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)
        streaming_api.filter(follow=usernameArr)

run_main()
