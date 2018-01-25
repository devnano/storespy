import subprocess
import demjson
import urllib
#import requests


def retrieve_play_store_app_data(url):
    splited = urllib.parse.urlsplit(url)
    params = urllib.parse.parse_qs(splited.query)
    app_id = params["id"][0]
    args = ["node", "node/scraper.js", app_id]
    result = subprocess.check_output(args).decode()

    return demjson.decode(result)


# return requests.get('https://api.github.com/events') #


