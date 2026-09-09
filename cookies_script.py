from fastapi import FastAPI,Request,Response,Depends
from pydantic import BaseModel
import secrets

class Input(BaseModel):
    name:str
    password:str

app=FastAPI()
user_details={}
session_details={}

@app.post("/register")
def register_user(input:Input):
    if input.name in user_details:
        return {"response":"User already exists"}

    user_details[input.name]=input.password

    return {"response":"Details addedd successfully"}

@app.post("/login")
def login_func(input:Input,response:Response):
    if input.name not in user_details:
        return {"response":"user details not found"}

    user_password=user_details[input.name]
    if user_password!=input.password:
        return {"response":"password mismatch"}

    session_id=secrets.token_urlsafe(32)

    session_details[session_id]=input.name

    response.set_cookie("cookie",session_id,httponly=True)

    return {"response":"login successful"}

def get_current_user(request:Request):
    cookie_id=request.cookies.get("cookie")
    return session_details[cookie_id]

@app.get("/dashboard")
def route_dashboard(request:Request,user:str=Depends(get_current_user)):
    return {"res":f"Hello {user} welcome to python tutorial"}

