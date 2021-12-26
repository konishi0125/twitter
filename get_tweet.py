import config
import tweepy
import time
import csv
import neologdn
import re

FIFTEEN_MINUTES = 16 * 60
#twitter取得制限が来たら処理を待つ関数
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

#twitterから取得したテキストを成型する 全角半角統一、絵文字除去、改行を読点に変換
def fix_text(text):
    normalized_text = neologdn.normalize(text)
    text_without_url = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", normalized_text)
    text_replace_newline = re.sub(r"\n", "。", text_without_url)
    text_delete_double_piriod = text_replace_newline.replace("。。","。")
    n = re.compile(r"[0-9a-zA-Z\u0023\u3040-\u30FF\u4E00-\u9FFF\u3001\u3002]")
    result = "".join(t for t in text_delete_double_piriod if n.search(t))
    return result

#tweepy用のトークン読み込み
def auth_set():
    CK = config.CONSUMER_KEY
    CS = config.CONSUMER_SECRET
    AT = config.ACCESS_TOKEN
    ATS = config.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, ATS)
    return auth

#search_keyで検索結果を取得
def get_tweet_by_search(search_key, get_num=1000):
    api = tweepy.API(auth_set())
    i=0
    out=[]
    for status in limit_handled(tweepy.Cursor(api.search_tweets, q=search_key).items(get_num)):
        t = fix_text(status.text)
        out.append([status.user.screen_name, t, status.id_str, ])
        print(i, status.created_at)
        i += 1
    return out

#自分のファボを取得する
def get_tweet_by_favorite(get_num=1000):
    api = tweepy.API(auth_set())
    i=0
    out=[]
    for status in limit_handled(tweepy.Cursor(api.get_favorites).items(get_num)):
        t = fix_text(status.text)
        out.append([status.user.screen_name, t, status.id_str, ])
        print(i, status.created_at)
        i += 1
    return out


if __name__ == "__main__":
    api = tweepy.API(auth_set())
    i=0
    out = [["name", "text", "id"]]
    #for status in limit_handled(tweepy.Cursor(api.get_favorites).items()):
    for status in limit_handled(tweepy.Cursor(api.search_tweets, q="#sarinatalk").items()):
        t = fix_text(status.text)
        out.append([status.user.screen_name, t,status.id_str])
        print(i, status.created_at)
        i += 1

    with open("./result/sarinatalk.csv", mode="w", encoding="utf_8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(out)

