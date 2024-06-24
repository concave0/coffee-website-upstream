from fetch_data.cache_coffee_data import CacheData 
from fetch_data.fetch_ids import FetchIds 
import os 

class CacheWorkers: 
    
    def __init__(self) -> None:
        self.cache_node = None
        
    # Fetching the data 
    def cache(self): 
        cache_ids = CacheData()
        self.cache_node = cache_ids.fetch_data() # Update everytime ran 

    # Fetching an updated list of ids
    def cache_ids(self): 
        endpoint_route = "ngork_endpoint/id"
        endpoint = os.environ['ngork_endpoint']
        url = f"{endpoint}/{endpoint_route}"
        fetch = FetchIds()
        fetch.fetch_ids(url=url)


