# -*- coding: utf-8 -*-

import storespy
import pytest
import datetime
from collections import OrderedDict

def test_parse_store_bad_url_error():
    with pytest.raises(storespy.GetStoreDataBadHostError):
        storespy.__parse_store_app_url("any string that's not an url", "play.google.com", "id")

def test_parse_store_bad_host_error():
    with pytest.raises(storespy.GetStoreDataBadHostError):
        storespy.__parse_store_app_url("http://google.com", "play.google.com", "id")

def test_parse_store_missing_id_param_error():
    with pytest.raises(storespy.GetStoreDataMissingIdParameterError):
        storespy.__parse_store_app_url("http://play.google.com", "play.google.com", "id")

def test_get_play_store_app_data_success():
    result = storespy._get_play_store_app_data("https://play.google.com/store/apps/details?id=com.americanwell.android.member.wellpoint&hl=en")
    assert result["title"] == 'LiveHealth Online Mobile'

def test_get_play_store_app_data_not_found():
    with pytest.raises(storespy.GetStoreDataItemNotFound):
        storespy.get_play_store_app_data("https://play.google.com/store/apps/?id=non_existent_id")

def test_get_app_store_app_data_success():
    result = storespy._get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/id535886823&hl=en")
    assert "trackName" in result
    assert "review_entries" in result

def test_get_app_store_app_data_id_in_url_success():
    result = storespy._get_app_store_app_data("https://itunes.apple.com/us/app/imprivata-id/id991327711?&hl=en")
    assert "trackName" in result
    assert "review_entries" in result

def test_get_app_store_app_data_not_found():
    with pytest.raises(storespy.GetStoreDataItemNotFound):
        storespy.get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/idno_existent&hl=en")

def test_get_reviews_from_feed_empty():
    feed = {}
    reviews = storespy._get_reviews_from_feed(feed)

    assert len(reviews) == 0

def test_get_review_from_entry():
    entry = OrderedDict([('updated', '2018-01-28T14:51:18-07:00'), ('id', '2137938140'), ('title', 'Has been an excellent application'), ('content', [OrderedDict([('@type', 'text'), ('#text', 'I have used this app for 6 and a half years. It has been excellent. Tracking has been excellent, generally agrees with my Cateye computer within 0.1 miles. I am coming up on 10,000 miles of tracked rides.\n\nIn 2012 I lost a couple month’s data when they had a “basic” and “pro” version and eliminated the basic version. That is the only time.')]), OrderedDict([('@type', 'html'), ('#text', '<table border="0" width="100%">\n    <tr>\n        <td>\n            <table border="0" width="100%" cellspacing="0" cellpadding="0">\n                <tr valign="top" align="left">\n                    \n                    \n                    \t<td width="100%">\n                    \n                        <b><a href="https://itunes.apple.com/us/app/endomondo/id333210180?mt=8&uo=2">Has been an excellent application</a></b><br/>\n                        \n                        \n                        \n                        \n\n                        \n\n                       <font size="2" face="Helvetica,Arial,Geneva,Swiss,SunSans-Regular">\n\t\t\t\t\t\t\n                        </font>\n                    </td>\n                </tr>\n            </table>\n        </td>\n    </tr>\n    <tr>\n        <td>\n            \n                <font size="2" face="Helvetica,Arial,Geneva,Swiss,SunSans-Regular"><br/>I have used this app for 6 and a half years. It has been excellent. Tracking has been excellent, generally agrees with my Cateye computer within 0.1 miles. I am coming up on 10,000 miles of tracked rides.<br/><br/>In 2012 I lost a couple month’s data when they had a “basic” and “pro” version and eliminated the basic version. That is the only time.</font><br/>\n            \n            \n            \n        </td>\n    </tr>\n</table>')])]), ('im:contentType', OrderedDict([('@term', 'Application'), ('@label', 'Application')])), ('im:voteSum', '0'), ('im:voteCount', '0'), ('im:rating', '5'), ('im:version', '17.12.0'), ('author', OrderedDict([('name', 'ulfoaf'), ('uri', 'https://itunes.apple.com/us/reviews/id28852301')])), ('link', OrderedDict([('@rel', 'related'), ('@href', 'https://itunes.apple.com/us/review?id=333210180&type=Purple%20Software')]))])
    review = storespy._get_review_from_entry(entry)

    assert isinstance(review, dict)
    assert "title" in review
    assert "date" in review
    assert "version" in review
    assert "score" in review
    assert "userName" in review
    assert "userUrl" in review
    assert "text" in review
    assert "url" in review
    assert isinstance(review['date'], datetime.datetime)

def test_get_app_store_app_reviews():
    reviews = storespy._get_app_store_app_reviews("535886823")

    assert isinstance(reviews, list)
    assert len(reviews) > 0
    for review in reviews:
        assert isinstance(review, dict)
        assert "title" in review
        assert "date" in review
        assert "version" in review
        assert "score" in review
        assert "userName" in review
        assert "userUrl" in review
        assert "text" in review
        assert "url" in review


def test_parse_app_id_from_path_last_component():
    id = storespy.__parse_app_id_from_path("us/app/google-chrome/id535886823", "id")
    assert id == "535886823"

def test_parse_app_id_from_path_not_last_component():
    id = storespy.__parse_app_id_from_path("us/app/google-chrome/id535886823/extra/paths", "id")
    assert id == "535886823"

expected_fields = ['category', 'content_rating', 'developer', 'developer_id', 'developer_url', 'fileSizeBytes', 'icon', 'minimumOsVersion', 'releaseNotes', 'reviews', 'score', 'screenshotUrls', 'title', 'updated', 'url']
def test_parse_app_id_from_path_missing():
    with pytest.raises(storespy.GetStoreDataMissingIdParameterError):
        storespy.__parse_app_id_from_path("us/app/google-chrome", "id")


def test_google_play_expected_fields():
    result = storespy.get_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome&hl=en")
    fields = list(set(result.keys()).intersection(expected_fields))
    fields.sort()

    assert expected_fields == fields

def test_app_store_expected_fields():
    result = storespy.get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/id535886823&hl=en")
    fields = list(set(result.keys()).intersection(expected_fields))
    fields.sort()

    assert expected_fields == fields

def test_dict_keys_fixup():
    expected_keys_mapping_dict = {'a':'z', 'w':'c', 'z':'d'}
    original_dict = {'a':'1','c':'2', 'd':'3'}
    resulting_dict = storespy.__dict_keys_fixup(original_dict, expected_keys_mapping_dict)

    assert resulting_dict == {'a':'1','w':'2','z':'3'}

def test_dict_keys_fixup_no_change():
    expected_keys_mapping_dict = {'a':'z', 'w':'c', 'z':'d'}
    original_dict = {'a':'1','w':'2', 'x':'3'}
    resulting_dict = storespy.__dict_keys_fixup(original_dict, expected_keys_mapping_dict)

    assert resulting_dict == {'a':'1','w':'2','x':'3'}

def test_dict_keys_fixup_expected_key_present():
    expected_keys_mapping_dict = {'a':'z', 'w':'c', 'z':'d'}
    original_dict = {'a':'1','w':'2', 'z':'3'}
    resulting_dict = storespy.__dict_keys_fixup(original_dict, expected_keys_mapping_dict)

    assert resulting_dict == {'a':'3','w':'2'}

def test_dict_keys_fixup_key_not_present():
    expected_keys_mapping_dict = {'a':'z', 'w':'c', 'z':'d'}
    original_dict = {'a':'1','e':'2', 'f':'3'}
    resulting_dict = storespy.__dict_keys_fixup(original_dict, expected_keys_mapping_dict)

    assert resulting_dict == {'a':'1','e':'2','f':'3'}

def test_dict_key_fixup():
    expected_key = 'w'
    mapped_key = 'c'
    original_dict = {'a':'1','c':'2'}
    resulting_dict = storespy.__dict_key_fixup(original_dict, expected_key, mapped_key)

    assert resulting_dict == {'a':'1','w':'2'}

def test_dict_key_fixup_no_change():
    expected_key = 'w'
    mapped_key = 'c'
    original_dict = {'a':'1','w':'2'}
    resulting_dict = storespy.__dict_key_fixup(original_dict, expected_key, mapped_key)

    assert resulting_dict == {'a':'1','w':'2'}

def test_dict_key_fixup_key_not_present():
    expected_key = 'w'
    mapped_key = 'c'
    original_dict = {'a':'1','b':'2'}
    resulting_dict = storespy.__dict_key_fixup(original_dict, expected_key, mapped_key)

    assert resulting_dict == {'a':'1','b':'2'}

def test_dict_key_fixup_key_expected_key_present():
    expected_key = 'w'
    mapped_key = 'c'
    original_dict = {'w':'1','c':'2'}
    resulting_dict = storespy.__dict_key_fixup(original_dict, expected_key, mapped_key)

    assert resulting_dict == {'w':'2'}
