from fastapi import Request, APIRouter, Form, HTTPException, Depends , Response 
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from data.data import CoffeeData, DataWorkers
from jinja2 import Template
from website.website import WebsiteSchema
from datetime import datetime
import bleach
from requests_queue.queue import RequestQueue
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from autocorrect import Speller
from api_token.token_data import CONSTAINT_TOKEN
from fetch_data.cache_workers import CacheWorkers
import jwt
from api_token.api_token_in_transit import GenerateAuthToken , TokenInTransit 
import os 
import time 

# Server data
hashmap = {}
coffee_blog_router_data = CoffeeData(favorite_coffee='', hashmap=hashmap)

# Server HMTL Files
website_hmtl_files = WebsiteSchema()

# Generating auth token for this server
auth_token = GenerateAuthToken()

# Coffee routes
coffee_blog_router = APIRouter()

# Data Workers
data_workers = DataWorkers(hashmap=coffee_blog_router_data.hashmap)

# Cache Workers
cache_workers = CacheWorkers()

# Messaging Queues
homepage_queue = RequestQueue(capacity=100)
data_sources_queue = RequestQueue(capacity=100)
get_data_queue = RequestQueue(capacity=10000)
what_is_favoirte_coffee_queue = RequestQueue(capacity=100)


def queue_request(request: Request, queue: RequestQueue):
    if queue.should_it_be_served() == True:
        queue.queue.append(hash(request))  # Storing hash as look up.

    elif queue.should_it_be_served() != True:
        raise HTTPException(
            status_code=503,
            detail=
            "Unable to serve request. Please try again in a couple of seconds."
        )


async def get_app(token: str = Depends(auth_token.oauth2_scheme)):
    # credentials_exception = HTTPException(
    #     status_code=status.HTTP_401_UNAUTHORIZED,
    #     detail="Could not validate credentials",
    #     headers={"WWW-Authenticate": "Bearer"},
    # )
    # try:
    #     payload = jwt.decode(token,
    #                          auth_token.SECRET_KEY,
    #                          algorithms=[auth_token.ALGORITHM])
    #     pass
    # except jwt.PyJWTError as e:
    #     print(e)
    #     raise credentials_exception
    pass 

# Home page
@coffee_blog_router.get("/")
async def homepage(request: Request):
    queue_request(request, homepage_queue)
    source = f"{website_hmtl_files.hashmap.get('homepage')}"
    template = Template(source)
    rendered_template = template.render()
    return HTMLResponse(content=rendered_template, status_code=200)


# Give back user information about there favorite coffee
@coffee_blog_router.get("/data_sources/{favorite_coffee}")
async def data_source_webpage(favorite_coffee: str, request: Request):
    queue_request(request, data_sources_queue)

    source = f"{website_hmtl_files.hashmap.get('data_sources')}"

    template = Template(source)

    details = cache_workers.cache_node.get(favorite_coffee)

    if details == None:
        spell = Speller()
        corrected_word = spell(favorite_coffee)

        closest_match = process.extractOne(corrected_word,
                                           cache_workers.cache_node.keys(),
                                           scorer=fuzz.ratio)

        if closest_match:
            key, score = closest_match
            if score >= 80:
                rendered_template = template.render(
                    data=cache_workers.cache_node.get(key).get("Facts"))
                return HTMLResponse(content=rendered_template, status_code=200)
            else:
                try:
                    choice = key
                    return RedirectResponse(url=f"/is_correct_maybe/{choice}")

                except Exception as e:
                    pass
    else:
        data = details.get("Facts")
        rendered_template = template.render(data=data)
        return HTMLResponse(content=rendered_template, status_code=200)


# Gueses the user favorite coffee
@coffee_blog_router.get("/is_correct_maybe/{choice}")
async def is_correct_maybe(choice: str, request: Request):
    source = f"{website_hmtl_files.hashmap.get('was_it_a_match')}"
    new_template = Template(source)
    rendered_template = new_template.render(data=choice)
    return HTMLResponse(rendered_template, status_code=200)


# Redirects to favorite users coffee
@coffee_blog_router.get("/redirect_data_sources/{choice}")
async def redirect_data_sources(choice: str, request: Request):
    return RedirectResponse(f"/data_sources/{choice}", status_code=303)


# Servers 404 page
@coffee_blog_router.get("/four_o_four")
async def four_o_four(request: Request):
    four_o_four = f"{website_hmtl_files.hashmap.get('four_o_four')}"
    new_template = Template(four_o_four)
    four_o_four_page = new_template.render()
    return HTMLResponse(content=four_o_four_page, status_code=404)


@coffee_blog_router.get("/redirect_four_o_four")
def redirect_four_o_four(request: Request):
    return RedirectResponse(f"/four_o_four", status_code=303)


# Pull in data from user
@coffee_blog_router.post("/what_is_favoirte_coffee")
async def what_is_favoirte_coffee(request: Request,
                                  favorite_coffee: str = Form(...)):

    queue_request(request, what_is_favoirte_coffee_queue)  # Queue request

    coffee_blog_router_data.favorite_coffee = bleach.clean(
        favorite_coffee)  # ! Cleaning data !
    client_ip = request.client.host if request.client else "Unknown Probably TOR! "

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    stored_data = coffee_blog_router_data.hashmap[
        f"{client_ip}+{formatted_datetime}"] = coffee_blog_router_data.favorite_coffee
    what_is_favoirte_coffee_queue.queue.popleft()  # remove request from the Q

    return RedirectResponse(
        f"/data_sources/{coffee_blog_router_data.favorite_coffee}",
        status_code=303)


# AUTHENTICATION ENDPOINT
@coffee_blog_router.post("/updating_api_key")
async def api_key_updating(request: Request):
    new_token = str(request.headers.get("Authorization")).split(" ")  # Receive token Ngork endpoint
    CONSTAINT_TOKEN.curr_token = new_token[1]
    
    print(f"Ngork token {CONSTAINT_TOKEN.curr_token} and the Coffee website token {auth_token.token}")
    giving_token = TokenInTransit()
    endpoint = os.environ['ngork_endpoint']
    giving_token.give(token=auth_token.token, endpoint=f"{endpoint}/updating_api_key")
    respond_confirming = Response(content=f"Done sending the token", status_code=200)
    
    return respond_confirming

# PROTECTED ROUTES
@coffee_blog_router.get("/turn_data_collection")  # Start collecing data based from a successful 200 request
async def turn_data_collection(request: Request, app_auth: str = Depends(get_app)):
    print("hello")
    new_token = str(request.headers.get("Authorization"))# Receive token Ngork endpoint
    print(f"current token being used {new_token}")
    cache_workers.cache_ids()
    time.sleep(3)
    cache_workers.cache()
    return Response(content="Done", status_code=200)
