import requests
import json
import os
import tempfile
from api_token.token_data import CONSTAINT_TOKEN


class FetchIds:
    def update_json_file_safely(self, file_path, updates):
        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        read_file.close()
        
        data.update(updates)
        
        with open(file_path, "w") as write_file:   
            json.dump(data, write_file, indent=4)
        write_file.close()
    
        
    def fetch_ids(self, url: str) -> str: 
        headers = {"Authorization": f"Bearer {CONSTAINT_TOKEN.curr_token}"}
        response = requests.get(url=url, headers=headers)
        id_reponse = json.loads(json.dumps(response.json()))
        path = "fetch_data/ids_data/ids.json"
        self.update_json_file_safely(file_path=path , updates=id_reponse)