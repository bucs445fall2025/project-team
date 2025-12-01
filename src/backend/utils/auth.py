import jwt
from dotenv import load_dotenv
import os

load_dotenv()

def create_jwt_token(payload: any):
	"""
    Creates a JSON Web Token (JWT) using the provided payload.
    Parameters:
        payload (any): The data to be encoded in the JWT (usually a dictionary)
    Returns:
        str: The encoded JWT as a string
    """
	return jwt.encode(payload, key=os.getenv("SECRET_KEY"), algorithm="HS256")

def get_user_info(token: str):
	"""
    Decodes a JSON Web Token (JWT) to retrieve the user information (payload).
    Parameters:
        token (str): The JWT string to be decoded
    Returns:
        dict: The decoded payload containing user information
    """
	return jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms="HS256")