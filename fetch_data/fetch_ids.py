import requests 
import json 
import datetime 
from api_token.token_data import CONSTAINT_TOKEN 

class FetchIds:
    
    def fetch_ids(self, url:str) -> str: # TODO and NOTE make sure that it is tne ngork URL when you get to it.
        headers = {"Authorization": f"Bearer {CONSTAINT_TOKEN.generate_jwt()}"}
        response = requests.get(url=url , headers=headers)
        id_reponse = json.loads(json.dumps(response.json()))
        now = datetime.datetime.now()
        path = f"fetch_data/ids_data/{now}_ids.json"
        with open(path,"w") as file: 
            json.dump(id_reponse, file, indent=4)
        file.close()
        new_path_record = open("fetch_data/last_path/last_path.txt", "w").write(path)

        