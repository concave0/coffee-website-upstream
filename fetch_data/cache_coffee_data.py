import requests
import json 
from api_token.token_data  import CONSTAINT_TOKEN
import time 

class CacheData: # <---    THIS CALL GOES TO THE DATABASE
    def fetch_data(self) -> dict: 
        cache = {}
        path = open("fetch_data/last_path/last_path.txt").read()
        with open(path, "r") as file: 
            id = json.loads(json.dumps(json.load(file)))
            for coffee , id in id.items(): 
                time.sleep(1)
                url= f"http://0.0.0.0:8080/ngork_endpoint/data" # TODO and NOTE replace ngrok endpoint
                headers = {
                    "Authorization": f"Bearer {CONSTAINT_TOKEN.generate_jwt()}",
                    "User-Agent": "MyCustomClient",
                    "Accept": "application/json",
                    "X-Request-ID": f"{id}"
                }
                response = requests.get(url, headers=headers)
                json_response = response.json()
                facts = json_response.get('Data')
                cache[coffee] = facts
        return cache 
