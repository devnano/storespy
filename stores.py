import subprocess
import demjson
import urllib
#import requests

class GetStoreDataError(Exception):
    pass

class GetStoreDataBadHostError(GetStoreDataError):
    pass

class GetStoreDataMissingIdParameterError(GetStoreDataError):
    pass

class GetStoreDataItemNotFound(GetStoreDataError):
    pass

def get_play_store_app_data(url):
    app_id = parse_store_app_url(url, "play.google.com", "id")
    args = ["node", "node/scraper.js", app_id]
    result = subprocess.check_output(args).decode()

    return demjson.decode(result)

def parse_store_app_url(url, expected_hostname, expected_id_param_key):
    split = urllib.parse.urlsplit(url)
    if split.hostname != expected_hostname:
        raise GetStoreDataBadHostError()

    params = urllib.parse.parse_qs(split.query)
    app_id = params["id"][0]

    return app_id
