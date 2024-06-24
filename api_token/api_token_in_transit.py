import requests
from fastapi.security import OAuth2PasswordBearer
import string
import secrets

class TokenInTransit: 
  def give(self, token:str, endpoint:str):
      headers = {
                  "Authorization": f"Bearer {token}"
              } 
      response = requests.post(url=endpoint,headers=headers)
      return response

class GenerateAuthToken:
  def __init__(self) -> None:
      self.token = self.generate_token(32) 
      self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=self.token)
      self.SECRET_KEY = self.token 
      self.ALGORITHM = "HS256"  

  def generate_token(self, length:int):
      alphabet = string.ascii_letters + string.digits
      token = ''.join(secrets.choice(alphabet) for _ in range(length))
      return token
