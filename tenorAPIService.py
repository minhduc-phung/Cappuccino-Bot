import json
from os import getenv
import random
import requests
from dotenv import load_dotenv

load_dotenv()
apikey = "LIVDSRZULELA"
print(apikey)
lmt = 10


def get_random_gif(search_term):
    r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
    print(r.status_code)
    if r.status_code == 200:
        # load the GIFs using the urls for the smaller GIF sizes
        gifs = json.loads(r.content)
        results = gifs['results']
        # get a random gif
        res = random.choice(results)
        return res['media'][0]['gif']['url']
    else:
        return None
