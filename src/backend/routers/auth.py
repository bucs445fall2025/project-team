from typing import Annotated
from fastapi import APIRouter, Response, status, Depends
from pydantic import BaseModel
import hashlib
from db import get_db_connection
from utils.auth import create_jwt_token, get_user_info
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SignUpRequest(BaseModel):
	first: str
	last: str
	email: str
	password: str

class LoginRequest(BaseModel):
	email: str
	password: str

def encrypt_string(string: str):
    return hashlib.sha256(string.encode()).hexdigest()

@router.post("/auth/signup")
async def signup(signupBody: SignUpRequest, response: Response):

	db = get_db_connection()
	if not db:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return "Error connecting database"
	
	encrypted_password = encrypt_string(signupBody.password)
	cursor = db.cursor()

	command = "INSERT INTO users (first, last, email, password) VALUES (%s, %s, %s, %s)"

	values = (signupBody.first, signupBody.last, signupBody.email, encrypted_password)

	cursor.execute(command, values)
	db.commit()
	response.status_code = status.HTTP_201_CREATED
	return f"Created user"


@router.post("/auth/login")
async def login(loginRequest: LoginRequest, response: Response):
	db = get_db_connection()
	if not db:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return "Error connecting database"
	encrypted_password = encrypt_string(loginRequest.password)
	cursor = db.cursor()
	command = "SELECT id, email, first, password FROM users WHERE email=%s"
	cursor.execute(command, (loginRequest.email, ))
	result = cursor.fetchone()
	if not result or encrypted_password != result[3]:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return "Incorrect email or password"
	payload = {
		"id": result[0],
		"email": result[1],
		"first": result[2],
		"password": result[3]
	}
	return create_jwt_token(payload)

@router.get("/auth/getFirstName")
async def getFirstName(token: Annotated[str, Depends(oauth2_scheme)]):
	user_info = get_user_info(token)
	print("test")
	return {"firstName": user_info['first']}