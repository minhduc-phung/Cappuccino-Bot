import json
from os import getenv

import requests
from dotenv import load_dotenv

load_dotenv()
apikey = getenv("TENOR_API_KEY")
lmt = 10

search_term = "wysi"

r = requests.get(
    "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
if r.status_code == 200:
    # load the GIFs using the urls for the smaller GIF sizes
    gifs = json.loads(r.content)
    results = gifs['results']
    for res in results:
        med = res['media']
        gif = med[0]
        gifurl = gif['gif']['url']
        print(gifurl)
else:
    gifs = None
