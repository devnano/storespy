import stores
import pytest

def test_parse_store_bad_url_error():
    with pytest.raises(stores.GetStoreDataBadHostError):
        stores.parse_store_app_url("any string that's not an url", "play.google.com", "id")

def test_parse_store_bad_host_error():
    with pytest.raises(stores.GetStoreDataBadHostError):
        stores.parse_store_app_url("http://google.com", "play.google.com", "id")

def test_parse_store_missing_id_param_error():
    with pytest.raises(stores.GetStoreDataMissingIdParameterError):
        stores.parse_store_app_url("http://play.google.com", "play.google.com", "id")

def test_get_play_store_app_data_success():
    result = stores.get_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome")
    assert result["title"] == 'Google Chrome: Fast & Secure'

def test_get_play_store_app_data_not_found():
    with pytest.raises(stores.GetStoreDataItemNotFound):
        stores.get_play_store_app_data("https://play.google.com/store/apps/?id=non_existent_id")

def test_get_app_store_app_data_success():
    result = stores.get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/id535886823")
    assert result["trackName"] == 'Google Chrome'

def test_get_app_store_app_data_not_found():
    with pytest.raises(stores.GetStoreDataItemNotFound):
        stores.get_app_store_app_data("https://itunes.apple.com/us/app/google-chrome/idno_existent")

def test_parse_app_id_from_path_last_component():
    id = stores.parse_app_id_from_path("us/app/google-chrome/id535886823", "id")
    assert id == "535886823"

def test_parse_app_id_from_path_not_last_component():
    id = stores.parse_app_id_from_path("us/app/google-chrome/id535886823/extra/paths", "id")
    assert id == "535886823"

def test_parse_app_id_from_path_missing():
    with pytest.raises(stores.GetStoreDataMissingIdParameterError):
        stores.parse_app_id_from_path("us/app/google-chrome", "id")

