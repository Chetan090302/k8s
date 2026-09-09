from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from user_service import all_users_data,add_user_to_db,find_user_with_name,update_user,delete_user_with_name,validate_credentials
from user_db import get_db
from security import create_token
from fastapi import Response

oath2_session=OAuth2PasswordBearer(tokenUrl="/token_validate")
app = FastAPI()


class Input(BaseModel):
    name: str
    email: str
    password: str

class UpdateUser(BaseModel):
    email: str
    password: str

class InputLogin(BaseModel):
    email:str
    password:str

@app.get("/token_validate")
def validate_544(token:str=Depends(oath2_session)):
    return {"token":token}

@app.get("/profile")
def route_profile(
    token: str = Depends(oath2_session)
):
    return {
        "response": token
    }
@app.post("/login")
def load_user(
    input: InputLogin,
    session: Session = Depends(get_db)
):

    email = input.email
    password = input.password

    is_validated = validate_credentials(
        email,
        password,
        session
    )

    if not is_validated:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    subject = {
        "sub": email
    }

    token = create_token(
        subject,
        10
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/validate")
def validate_token(token:str=Depends(oath2_session)):
    return token

@app.post("/register")
def register_data_to_db(input: Input,session: Session = Depends(get_db)):
    return add_user_to_db(session, input)

@app.get("/users")
def get_all_users(session: Session = Depends(get_db)):
    return all_users_data(session)

@app.get("/users/{name}")
def get_user(name: str,session: Session = Depends(get_db)):
    user = find_user_with_name(session, name)

    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@app.put("/users/{name}")
def update_user_data(
    name: str,
    input_data: UpdateUser,
    session: Session = Depends(get_db)
):
    user = update_user(
        session,
        name,
        input_data
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.delete("/users/{name}")
def delete_user_data(name: str,session: Session = Depends(get_db)):
    user = delete_user_with_name(session,name)

    if not user:
        raise HTTPException(status_code=404,detail="User not found")

    return {
        "message": "User deleted successfully"
    }