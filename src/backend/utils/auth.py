import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def create_jwt_token(payload: any):
	return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm="HS256")

def get_user_info(token: str):
	return jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms="HS256")