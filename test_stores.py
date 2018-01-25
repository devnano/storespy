import stores
import pytest


def test_retrive_play_store_app_data_success():
    result = stores.retrieve_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome")
    assert result["title"] == 'Google Chrome: Fast & Secure'


def test_retrive_play_store_app_data_except():
    with pytest.raises(Exception):
        stores.retrieve_play_store_app_data("https://play.google.com/store/apps/")

