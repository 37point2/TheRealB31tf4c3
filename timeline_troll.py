import tweepy
import json
from time import sleep

api_keys = json.load(open('api.json', 'r'))

CONSUMER_KEY = api_keys['api']['twitter']['CONSUMER_KEY']
CONSUMER_SECRET = api_keys['api']['twitter']['CONSUMER_SECRET']
ACCESS_TOKEN = api_keys['api']['twitter']['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = api_keys['api']['twitter']['ACCESS_TOKEN_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

mangle_dict = dict([x.split('\n')[0].split(',') for x in open('mangle_list.txt','r').readlines()])

class StreamListener(tweepy.StreamListener):

    def on_error(self, status_code):
        print 'Error: ' + repr(status_code)
        return False

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            if not json_data.has_key("friends"):
                print json_data["user"]["screen_name"] + " " + json_data["text"] + "\n"
                # Uncomment below to harass B31tf4c3 and friends whenever B31tf4c3 tweets about TheRealB31tf4c3
                # if "TheRealB31tf4c3" in [x['screen_name'] for x in json_data['entities']['user_mentions']] and json_data['user']['id'] == 423784527:
                #     reply(json_data)
                if json_data["text"][0:2] != "RT" and json_data['user']['id'] == 423784527:
                    tweet(mangle(json_data["text"]))
            print data
        except:
            pass

def reply(json_data):
    status = "@" + json_data['user']['screen_name'] + " "
    for name in json_data['entities']['user_mentions']:
        if name["screen_name"] != "TheRealB31tf4c3":
            status += "@" + name['screen_name'] + " "
    if len(status) > 102:
        return 0
    status += "user error; beltfaced; #ticketresolved"
    api.update_status(status=status, in_reply_to_status_id=json_data['id_str'])
    return 0

def mangle(text):
    status = ''
    for word in text.split(' '):
        if mangle_dict.has_key(word):
            status += mangle_dict[word] + " "
        else:
            status += word + " "
    if text == status[:-1]:
        if len(status) > 124:
            status = status[:124] + "#yolo #babyseal"
        else:
            status += "#yolo #babyseal"
    return status

def tweet(status):
    print status + "\n"
    if len(status) > 140:
        api.update_status(status = status[0:139])
    else:
        api.update_status(status = status)

def get_stream():
    listener = StreamListener()
    streamer = tweepy.Stream(auth=auth, listener=listener)
    streamer.userstream()

def main():
    while(True):
        try:
            get_stream()
        except:
            sleep(300)
            continue

if __name__ == '__main__':
    main()