from collections import deque


class RequestQueue:
    def __init__(self, capacity:int):
        self.queue = deque()
        self.capacity = capacity
    
    def enqueue(self, request):
        if len(self.queue) < self.capacity:
            self.queue.append(request)
        else:
            self.queue.popleft()
            self.queue.append(request)

    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.popleft()
        else:
            return None

    def is_empty(self):
        return len(self.queue) == 0

    def get_size(self):
        return len(self.queue)

    def remove_completed_task(self, task):
        if task in self.queue:
            self.queue.remove(task)
  
    def should_it_be_served(self) -> bool: 
        if self.is_empty(): 
            return True 
        
        elif self.get_size != self.capacity: 
            return True 
        
        elif self.get_size == self.capacity: 
            return False 

    
