import config
import tweepy
import time
import csv
import neologdn
import re

FIFTEEN_MINUTES = 16 * 60
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.errors.TooManyRequests:
            print('Twitter rate limit')
            time.sleep(FIFTEEN_MINUTES)
        except StopIteration:
            print("fetch end")
            return None

def fix_text(text):
    normalized_text = neologdn.normalize(text)
    text_without_url = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", normalized_text)
    text_replace_newline = re.sub(r"\n", "。", text_without_url)
    n = re.compile(r"[0-9a-zA-Z\u0023\u3040-\u30FF\u4E00-\u9FFF\u3001\u3002]")
    result = "".join(t for t in text_replace_newline if n.search(t))
    return result

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)

api = tweepy.API(auth)

first = True
i=0
out = [["name", "text", "id"]]
#for status in limit_handled(tweepy.Cursor(api.get_favorites).items()):
for status in limit_handled(tweepy.Cursor(api.search_tweets, q="#sarinatalk").items()):
    if first:
        latest_id = status.id_str
        first = False
    t = fix_text(status.text)
    out.append([status.user.screen_name, t,status.id_str])
    print(i, status.created_at)
    i += 1
    if i % 500 == 0:
        time.sleep(FIFTEEN_MINUTES)

with open("./result/sarinatalk.csv", mode="w", encoding="utf_8", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(out)

