import json
from os import getenv
import random
import requests
from dotenv import load_dotenv

load_dotenv()
apikey = getenv("TENOR_API_KEY")
lmt = 10


def get_random_gif(search_term):
    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        gifs = json.loads(r.content)
        results = gifs['results']
        # get a random gif
        res = random.choice(results)
        return res['media'][0]['gif']['url']
    else:
        return None

def get_chatting_gif():
    return "https://media.tenor.com/9nZ5fdxEyQQAAAAi/chatting-twich-emote-xqc-asmongold-chat-tyler1.gif"
