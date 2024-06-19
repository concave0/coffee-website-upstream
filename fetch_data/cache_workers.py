from fetch_data.cache_coffee_data import CacheData 
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from apscheduler.triggers.interval import IntervalTrigger
from fetch_data.fetch_ids import FetchIds 

class CacheWorkers: 
    
    def __init__(self) -> None:
        self.cache_node = None
        self.scheduler = BlockingScheduler()

    def cache(self): 
        cache_ids = CacheData()
        self.cache_node = cache_ids.fetch_data() # Update everytime you run 
    
    def cache_ids(self): 
        url = "http://0.0.0.0:8080/ngork_endpoint/id" # TODO and NOTE make sure that it is tne ngork URL when you get to it.
        fetch = FetchIds()
        fetch.fetch_ids(url=url)

    def set_jobs(self): 
        trigger = IntervalTrigger(seconds=4) 
        self.scheduler.add_job(self.cache, trigger)
        self.scheduler.add_job(self.cache_ids, trigger)
    
    def start_scheduler(self):
        scheduler_thread = Thread(target=self.scheduler.start)
        scheduler_thread.start()
        print("Cache worker thread started")
