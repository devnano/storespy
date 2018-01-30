import storespy
import pytest

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
    result = storespy._get_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome")
    assert result["title"] == 'Google Chrome: Fast & Secure'

def test_get_play_store_app_data_not_found():
    with pytest.raises(storespy.GetStoreDataItemNotFound):
        storespy.get_play_store_app_data("https://play.google.com/store/apps/?id=non_existent_id")

def test_get_app_store_app_data_success():
    result = storespy._get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/id535886823")
    assert result["trackName"] == 'Google Chrome'

def test_get_app_store_app_data_not_found():
    with pytest.raises(storespy.GetStoreDataItemNotFound):
        storespy.get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/idno_existent")

def test_parse_app_id_from_path_last_component():
    id = storespy.__parse_app_id_from_path("us/app/google-chrome/id535886823", "id")
    assert id == "535886823"

def test_parse_app_id_from_path_not_last_component():
    id = storespy.__parse_app_id_from_path("us/app/google-chrome/id535886823/extra/paths", "id")
    assert id == "535886823"

expected_fields = ['contentRating', 'description', 'developer', 'developerId', 'developerWebsite', 'fileSizeBytes', 'genre', 'icon', 'minimumOsVersion', 'price', 'releaseNotes', 'reviews', 'score', 'screenshotUrls', 'summary', 'title', 'updated', 'url', 'version']

def test_parse_app_id_from_path_missing():
    with pytest.raises(storespy.GetStoreDataMissingIdParameterError):
        storespy.__parse_app_id_from_path("us/app/google-chrome", "id")


def test_google_play_expected_fields():
    result = storespy.get_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome")
    fields = list(set(result.keys()).intersection(expected_fields))
    fields.sort()

    assert expected_fields == fields

def test_app_store_expected_fields():
    result = storespy.get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/id535886823")
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
