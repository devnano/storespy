import subprocess
import demjson
#import requests




def retrieve_play_store_app_data(url):
   result = subprocess.check_output(["node", "node/test.js"]).decode()
   return demjson.decode(result)

# return requests.get('https://api.github.com/events') #


