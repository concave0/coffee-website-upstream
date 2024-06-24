import requests
import json 
from api_token.token_data  import CONSTAINT_TOKEN
import time 
import os 

class CacheData: # <---    THIS CALL GOES TO THE DATABASE
    def fetch_data(self) -> dict: # !! NOTE THE CHANGE THE DATA BEING WRITTEN A JSON FILE IN FETCH IDS BREAK THE CACHE COFFEE DATA!!  
        cache = {}
        path = "fetch_data/ids_data/ids.json"
        with open(path, "r") as file: 
            id = json.loads(json.dumps(json.load(file)))
            for coffee ,id in id.items(): 
                time.sleep(3)
                print(f"making the first call to {id}")
                endpoint_route = "ngork_endpoint/data"
                endpoint = os.environ['ngork_endpoint']
                url= f"{endpoint}/{endpoint_route}"
                headers = {
                    "Authorization": f"Bearer {CONSTAINT_TOKEN.curr_token}",
                    "User-Agent": "MyCustomClient",
                    "Accept": "application/json",
                    "X-Request-ID": f"{id}"
                }
                response = requests.get(url, headers=headers)
                json_response = response.json()
                facts = json_response.get('Data')
                cache[coffee] = facts
        return cache 
