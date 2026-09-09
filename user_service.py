from sqlalchemy.orm import Session
from user_schema import User
from security import verify_password,hash_password

def validate_credentials(email:str,password:str,session:Session):
    user=session.query(User).filter(User.email==email).first()
    db_password=user.password
    return verify_password(password,db_password)

def all_users_data(session: Session):
    return session.query(User).all()

def add_user_to_db(session: Session, input_data):
    user_password=hash_password(input_data.password)
    user_data = User(name=input_data.name,email=input_data.email,password=user_password)
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    return user_data

def find_user_with_name(session: Session, name: str):
    return session.query(User).filter(User.name == name).first()

def delete_user_with_name(session: Session, name: str):
    user = (session.query(User).filter(User.name == name).first())

    if not user:
        return None

    session.delete(user)
    session.commit()
    return user

def update_user(session: Session,name: str,input_data):
    user = (session.query(User).filter(User.name == name).first())

    if not user:
        return None

    user.email = input_data.email
    user.password = input_data.password
    session.commit()
    session.refresh(user)
    return user