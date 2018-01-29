import subprocess
import demjson
import urllib
import requests
import os

class GetStoreDataError(Exception):
    pass

class GetStoreDataBadHostError(GetStoreDataError):
    pass

class GetStoreDataMissingIdParameterError(GetStoreDataError):
    pass

class GetStoreDataItemNotFound(GetStoreDataError):
    pass

def get_play_store_app_data(url):
    # Installing npm here… check if this is running just the first time or on every execution.
    args = ["npm", "install", "google-play-scraper"]
    subprocess.check_output(args)

    app_id = __parse_store_app_url(url, "play.google.com", "id")
    args = ["node", "-e", "var gplay = require('google-play-scraper'); gplay.app({{appId: '{0}'}}).then(console.log, console.log);".format(app_id)]
    result = subprocess.check_output(args).decode()

    try:
        return demjson.decode(result)
    except Exception as err:
        # Just assume any communication error as item not found. Could be improved to parse the error thrown:
        raise GetStoreDataItemNotFound() from err

def get_app_store_app_data(url):
    app_id = __parse_store_app_url(url, "itunes.apple.com", "id")
    err = None
    try:
        r = requests.get("https://itunes.apple.com/lookup?id={0}".format(app_id))
        if r.status_code == 200:
            return r.json()["results"][0]
    except Exception as e:
        # Just assume any error as item not found. Could be improved to parse the error thrown:
        err = e

    if err != None:
        raise GetStoreDataItemNotFound() from err

    raise GetStoreDataItemNotFound()

def __parse_store_app_url(url, expected_hostname, expected_id_param_key):
    split = urllib.parse.urlsplit(url)

    if split.hostname != expected_hostname:
        raise GetStoreDataBadHostError()

    params = urllib.parse.parse_qs(split.query)

    if expected_id_param_key in params:
        return params[expected_id_param_key][0]

    return __parse_app_id_from_path(split.path, expected_id_param_key)

def __parse_app_id_from_path(path, expected_id_param_key):
    components = path.split(expected_id_param_key)
    if len(components) < 2:
        raise GetStoreDataMissingIdParameterError()

    # Get the string to the right of id token and then discard any additional path after it
    return components[1].split("/")[0]
