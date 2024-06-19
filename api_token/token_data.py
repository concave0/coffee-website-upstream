import jwt 

class Token:

    def __init__(self) -> None:
        self.curr_token = None 

    def generate_jwt(self):
        payload = {"application": "ids", "exp": 999999999999999999999999999} 
        api_token = self.curr_token
        token = jwt.encode(payload, api_token, algorithm="HS256")  
        return token
    
CONSTAINT_TOKEN = Token() # will be replaced with actual token once everything is running