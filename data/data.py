import json 
import os 
from pydantic import BaseModel
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread
from apscheduler.triggers.interval import IntervalTrigger


class CoffeeData(BaseModel): 
  favorite_coffee: str 
  hashmap: dict 

class DataWorkers(): 
  def __init__(self, hashmap: dict):
    self.hashmap  = hashmap
    self.scheduler = BlockingScheduler()

  def save(self): 
    file_path = "data/store/user_input.json"
    json_string = json.dumps(self.hashmap, indent=4)
   
    with open(file_path, 'w') as file:
        file.write(json_string)
      
  def size_of_file(self): 
    file_path = "data/store/user_input.json"
    file_size = os.path.getsize(file_path)
    return file_size
    
  def updating(self): 
    
    file_path = "data/store/user_input.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:

        data = {}
      
    data.update(self.hashmap)
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
      
  def set_jobs(self): 
    trigger = IntervalTrigger(seconds=1800) # Record user input every 30 minutes
    self.scheduler.add_job(self.save, trigger)
    
  def start_scheduler(self):
    scheduler_thread = Thread(target=self.scheduler.start)
    scheduler_thread.start()
    print("Scheduler thread started")
