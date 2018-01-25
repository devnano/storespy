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
        pass

def test_retrive_play_store_app_data_success():
    result = stores.get_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome")
    assert result["title"] == 'Google Chrome: Fast & Secure'

def test_retrive_play_store_app_data_except():
    with pytest.raises(Exception):
        stores.get_play_store_app_data("https://play.google.com/store/apps/")

