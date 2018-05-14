import urllib
import requests
import xmltodict
import dateutil.parser
import play_scraper

class GetStoreDataError(Exception):
    pass

class GetStoreDataBadHostError(GetStoreDataError):
    pass

class GetStoreDataMissingIdParameterError(GetStoreDataError):
    pass

class GetStoreDataItemNotFound(GetStoreDataError):
    pass

fields_mapping_dict = {
     'title': 'trackName',
     'price': {'type': float, 'mapped_key': 'price'},
     'icon':'artworkUrl512',
     'score':'averageUserRating',
     'reviews':'userRatingCount',
     'developer':'artistName',
     'developer_id':'artistId',
     'developer_url':'sellerUrl',
     'updated':'currentVersionReleaseDate',
     'category':'genres',
     'minimumOsVersion':'required_android_version',
     'content_rating':'trackContentRating',
     'screenshotUrls':'screenshots',
     'fileSizeBytes':'size',
     'releaseNotes':'recent_changes',
     'url':'trackViewUrl'
     }

def get_play_store_app_data(url):
    return __dict_keys_value_fixup(_get_play_store_app_data(url), fields_mapping_dict)

def _get_play_store_app_data(url):
    app_id = __parse_store_app_url(url, "play.google.com", "id")

    try:
        result = play_scraper.details(app_id)
        # XXX:
        result['summary'] = "TODO: missing in play_scraper. Check it's feasible to modify its code and get summary value."
        return result
    except Exception as err:
        # Just assume any communication error as item not found. Could be improved to parse the error thrown:
        raise GetStoreDataItemNotFound() from err

def get_app_store_app_data(url):
    dict = _get_app_store_app_data(url)
    # XXX:
    dict['summary'] = "a summary is available on App Store (from iOS 11) but such a field is not in itunes response. "

    return __dict_keys_value_fixup(dict, fields_mapping_dict)

def _get_app_store_app_data(url):
    app_id = __parse_store_app_url(url, "itunes.apple.com", "id")
    err = None
    try:
        r = requests.get("https://itunes.apple.com/lookup?id={0}".format(app_id))
        if r.status_code == 200:
            dict = r.json()["results"][0]
            dict['review_entries'] = _get_app_store_app_reviews(app_id)

            return dict
    except Exception as e:
        # Just assume any error as item not found. Could be improved to parse the error thrown:
        err = e

    if err != None:
        raise GetStoreDataItemNotFound() from err

    raise GetStoreDataItemNotFound()

def _get_app_store_app_reviews(app_id):
    r = requests.get("https://itunes.apple.com/us/rss/customerreviews/id={0}/sortby=mostRecent/page=1/xml".format(app_id))
    r.encoding = 'utf-8'
    feed = xmltodict.parse(r.text)

    return _get_reviews_from_feed(feed)

def _get_reviews_from_feed(feed):
    entries = feed.get('feed', {}).get('entry', [])[1:]
    reviews = []
    for entry in entries:
        review = _get_review_from_entry(entry)
        reviews.append(review)

    return reviews

def _get_review_from_entry(entry):
    review = {}
    review["title"] = entry['title']
    review["date"] = dateutil.parser.parse(entry['updated'])
    review["version"] = entry['im:version']
    review["score"] = entry['im:rating']
    review["userName"] = entry['author']['name']
    review["userUrl"] = entry['author']['uri']
    review["url"] = entry['link']['@href']
    review["text"] = entry['content'][0]['#text']

    return review

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
    componentsLen = len(components)
    if componentsLen < 2:
        raise GetStoreDataMissingIdParameterError()

    # Get the string to the right of id token and then discard any additional path after it
    return components[componentsLen-1].split("/")[0]

# Mutating original_dict in place
def __dict_keys_value_fixup(original_dict, expected_keys_value_mapping):
    for key, value in expected_keys_value_mapping.items():
        __dict_key_value_fixup(original_dict, key, value)

    return original_dict

def __dict_key_value_fixup(original_dict, expected_key, mapped_key_value):
    mapped_key = mapped_key_value
    expected_type = None
    if isinstance(mapped_key_value, dict):
        mapped_key = mapped_key_value['mapped_key']
        expected_type = mapped_key_value['type']

    if mapped_key in original_dict:
        original_dict[expected_key] = original_dict.pop(mapped_key)

    if (expected_type != None) and not isinstance(original_dict[expected_key], expected_type):
        try:
            original_dict[expected_key] = expected_type(original_dict[expected_key])
        except Exception as e:
            print(e)
            print('Assigning None to field \'{}\''.format(expected_key) )
            original_dict[expected_key] = None

    return original_dict
