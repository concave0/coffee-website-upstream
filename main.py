from threading import Thread
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from routes.routes import coffee_blog_router , run_scheduler 

# Configuration Blog
app = FastAPI()
app.include_router(coffee_blog_router)

limiter = Limiter(key_func=get_remote_address, default_limits=["3/seconds"])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(GZipMiddleware, minimum_size=1000)

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
  
  server_thread = Thread(target=run_server)
  scheduler_thread = Thread(target=run_scheduler)
  
  server_thread.start()
  scheduler_thread.start()
  
  server_thread.join()
  scheduler_thread.join()
