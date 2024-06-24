# Coffee Data Management System

## Module Overview

This system handles fetching, caching, and managing coffee data and IDs. It also defines the routing for the coffee blog application.

## Setup Instructions
Follow these steps to set up the Coffee Data Management System using `pip`.
### Prerequisites
Ensure that you have the following installed:
- Python 3.6 or later
- `pip` (Python package installer)
### Installation Steps
1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/concave0/coffee-website.git 
   cd coffee-website
2. Create venv ```bash
   python -m venv venv
3. Activate it:
   ```bash 
   source venv/bin/activate 
   
4. Install the nesscary dependencies  
   ```bash
   pip install -r requirements.txt
  
5. Run the application
   ```bash
   python3 main.py
   


---
## Program Knowledge Base

### Modules and Classes

#### Coffee Data Fetching and Caching
- **Module Description**: Responsible for fetching coffee data and caching it.
- **Classes**:
  - `CacheData`: Fetches coffee data based on various IDs and caches it.
    - **Methods**:
      - `fetch_data`: Fetches coffee data from an endpoint and stores it in a cache dictionary.
        - **Returns**: A dictionary containing coffee data indexed by coffee IDs.

#### Cache Workers Management
- **Module Description**: Manages cache operations for coffee data.
- **Classes**:
  - `CacheWorkers`: Manages cache operations for coffee data.
    - **Attributes**:
      - `cache_node`: Stores cached coffee data.
    - **Methods**:
      - `__init__`: Initializes the `CacheWorkers` class.
      - `cache`: Fetches and updates cached coffee data.
      - `cache_ids`: Fetches and updates the list of coffee IDs.

#### Coffee IDs Fetching
- **Module Description**: Fetches and updates coffee IDs in a JSON file.
- **Classes**:
  - `FetchIds`: Fetches and updates coffee IDs.
    - **Methods**:
      - `update_json_file_safely`: Safely updates a JSON file with new data.
        - **Arguments**:
          - `file_path (str)`: The path to the JSON file.
          - `updates (dict)`: The new data to update the file with.
      - `fetch_ids`: Fetches coffee IDs from an endpoint and updates the JSON file.
        - **Arguments**:
          - `url (str)`: The endpoint URL to fetch coffee IDs from.

#### Routing for Coffee Blog Application
- **Module Description**: Defines the routing for the coffee blog application.
- **Classes**:
  - `CoffeeData`: Manages coffee data.
  - `DataWorkers`: Manages data operations.
  - `WebsiteSchema`: Contains HTML templates for the website.
  - `RequestQueue`: Manages a request queue.
  - `GenerateAuthToken`: Generates authentication tokens.
  - `TokenInTransit`: Manages token transit operations.
  - `CacheWorkers`: Manages cache operations for coffee data.
- **Functions**:
  - `queue_request`: Adds a request to the queue if it should be served.
    - **Arguments**:
      - `request (Request)`: The incoming request.
      - `queue (RequestQueue)`: The request queue to add to.
  - `get_app`: Endpoint for user authentication.
    - **Arguments**:
      - `token (str)`: The authentication token.

---

### Routing

- **@coffee_blog_router.get("/")**
  - **Description**: Serves the homepage.
  - **Arguments**:
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `HTMLResponse`: The homepage HTML content.

- **@coffee_blog_router.get("/data_sources/{favorite_coffee}")**
  - **Description**: Serves the data source webpage for favorite coffee.
  - **Arguments**:
    - `favorite_coffee (str)`: The favorite coffee type.
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `HTMLResponse/RedirectResponse`: The data source HTML content or redirect response.

- **@coffee_blog_router.get("/is_correct_maybe/{choice}")**
  - **Description**: Serves a page asking if the guessed coffee is correct.
  - **Arguments**:
    - `choice (str)`: The guessed coffee choice.
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `HTMLResponse`: The confirmation HTML content.

- **@coffee_blog_router.get("/redirect_data_sources/{choice}")**
  - **Description**: Redirects to the data sources page.
  - **Arguments**:
    - `choice (str)`: The coffee choice.
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `RedirectResponse`: A redirect response to the data sources page.

- **@coffee_blog_router.get("/four_o_four")**
  - **Description**: Serves the 404 error page.
  - **Arguments**:
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `HTMLResponse`: The 404 error HTML content.

- **@coffee_blog_router.get("/redirect_four_o_four")**
  - **Description**: Redirects to the 404 error page.
  - **Arguments**:
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `RedirectResponse`: A redirect response to the 404 error page.

- **@coffee_blog_router.post("/what_is_favoirte_coffee")**
  - **Description**: Collects user input for favorite coffee.
  - **Arguments**:
    - `request (Request)`: The incoming request.
    - `favorite_coffee (str)`: The user-provided favorite coffee.
  - **Returns**:
    - `RedirectResponse`: A redirect response to the data sources page.

- **@coffee_blog_router.post("/updating_api_key")**
  - **Description**: Updates the API key.
  - **Arguments**:
    - `request (Request)`: The incoming request.
  - **Returns**:
    - `Response`: A confirmation response.

- **@coffee_blog_router.get("/turn_data_collection")**
  - **Description**: Starts data collection based on a successful request.
  - **Arguments**:
    - `request (Request)`: The incoming request.
    - `app_auth (str)`: The application authentication token.
  - **Returns**:
    - `Response`: A confirmation response after data collection is complete.

---

### Class Details

#### `WebsiteSchema`
Contains HTML templates for the website.
- **Attributes**:
  - `hashmap`: A dictionary storing the content of various HTML templates.
- **Methods**:
  - `__init__`: Initializes the `hashmap` attribute with the content of HTML templates for homepage, data sources, match check, and 404 error page.

#### `RequestQueue`
Manages a request queue.
- **Attributes**:
  - `queue`: A deque to store requests.
  - `capacity`: An integer representing the maximum capacity of the queue.
- **Methods**:
  - `__init__`: Initializes the queue and sets its capacity.
    - **Arguments**:
      - `capacity (int)`: The maximum capacity of the queue.
  - `enqueue`: Adds a request to the queue. If the queue is full, it removes the oldest request before adding the new one.
    - **Arguments**:
      - `request`: The request to be added to the queue.
  - `dequeue`: Removes and returns the oldest request from the queue. Returns `None` if the queue is empty.
  - `is_empty`: Checks if the queue is empty.
    - **Returns**: `True` if the queue is empty, else `False`.
  - `get_size`: Returns the current size of the queue.
  - `remove_completed_task`: Removes a specific task from the queue if it exists.
    - **Arguments**:
      - `task`: The task to be removed.
  - `should_it_be_served`: Determines whether a request should be served based on the queue's state.
    - **Returns**: `True` if the queue is not at full capacity or empty, else `False`.

#### `CoffeeData`
A model to store favorite coffee data and a hashmap.
- **Attributes**:
  - `favorite_coffee`: A string indicating the user's favorite coffee.
  - `hashmap`: A dictionary storing additional data.

#### `DataWorkers`
Manages data operations for storing and updating user input.
- **Attributes**:
  - `hashmap`: A dictionary to store user input data.
  - `scheduler`: An APScheduler instance for scheduling regular data operations.
- **Methods**:
  - `__init__`: Initializes the class with a hashmap and a scheduler.
    - **Arguments**:
      - `hashmap (dict)`: A dictionary to store user input data.
  - `save`: Saves the current hashmap data to a JSON file.
  - `size_of_file`: Returns the size of the JSON file storing user input data.
    - **Returns**: File size in bytes.
  - `updating`: Loads existing data from the JSON file and updates it with new data from the hashmap.
  - `set_jobs`: Schedules the `save` method to run at regular intervals (every 3 seconds).
  - `start_scheduler`: Starts the scheduler in a new thread.
    - **Prints**: "Scheduler thread started".

#### `TokenInTransit`
Manages token transit operations.
- **Methods**:
  - `give`: Sends a token to a specified endpoint.
    - **Arguments**:
      - `token (str)`: The token to be sent.
      - `endpoint (str)`: The endpoint where the token will be sent.
    - **Returns**: The response from the endpoint.

#### `GenerateAuthToken`
Generates authentication tokens.
- **Attributes**:
  - `token`: The generated token.
  - `oauth2_scheme`: An instance of `OAuth2PasswordBearer` initialized with the token URL.
  - `SECRET_KEY`: The generated token used as the secret key.
  - `ALGORITHM`: The algorithm used for token encryption.
- **Methods**:
  - `__init__`: Initializes the class and generates a token.
  - `generate_token`: Generates a random token of specified length.
    - **Arguments**:
      - `length (int)`: The length of the generated token.
    - **Returns**: The generated token.

#### `Token`
Manages JWT token generation.
- **Attributes**:
  - `curr_token`: Stores the current token (initialized as `None`).
- **Methods**:
  - `__init__`: Initializes the `Token` class and sets `curr_token` to `None`.
  - `generate_jwt`: Generates a JWT token with a predefined payload.
    - **Returns**: The generated JWT token.

---

### Constants

#### `CONSTAINT_TOKEN`
- An instance of `Token`, replaced with the actual token once everything is running.