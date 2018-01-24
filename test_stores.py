import stores


def test_retrive_play_store_app_data():
    result = stores.retrieve_play_store_app_data("https://play.google.com/store/apps/details?id=com.android.chrome")
    assert result["title"] == 'Google Chrome: Fast & Secure'
