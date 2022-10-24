from datetime import date
from enum import Enum
from fastapi import FastAPI
from bcrypt import checkpw
from typing import Optional, Dict
from pydantic import BaseModel
from uuid import UUID


app = FastAPI()

valid_users = dict()
pending_users = dict()
valid_profiles = dict()
discussion_posts = dict()


class User(BaseModel):
    username: str
    password: str


class UserType(str, Enum):
    admin = "admin"
    teacher = "teacher"
    alumni = "alumni"
    student = "student"


class UserProfile(BaseModel):
    firstname: str
    lastname: str
    middle_initial: str
    age: Optional[int] = 0
    salary: Optional[int] = 0
    birthday: date
    user_type: UserType


@app.get("/")
def index():
    return {"message": "Welcome to FastAPI Nerds"}


@app.get("/login")
def login(username: str, password: str):
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
        if checkpw(password.encode(), user.passphrase.encode()):
            return user
        else:
            return {"message": "invalid user"}


@app.post("/login/signup")
def signup(uname: str, password: str):
    if (uname is None and password is None):
        return {"message": "invalid user"}
    elif not valid_users.get(uname) is None:
        return {"message": "user exists"}
    else:
        user = User(username=uname, password=password)
        pending_users[uname] = user
        return user


@app.put("/account/profile/update/{username}")
def update_profile(username: str, id: UUID, new_profile: UserProfile):
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            valid_profiles[username] = new_profile
            return {"message": "successfully updated"}
        else:
            return {"message": "user does not exist"}


@app.put("/account/profile/update/names/{username}")
def update_profile_names(username: str, id: UUID, new_names: Dict[str, str]):
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    elif new_names is None:
        return {"message": "new names are required"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            profile = valid_profiles[username]
            profile.firstname = new_names['fname']
            profile.lastname = new_names['lname']
            profile.middle_initial = new_names['mi']
            valid_profiles[username] = profile
            return {"message": "successfully updated"}
        else:
            return {"message": "user does not exist"}


@app.delete("/discussion/posts/remove/{username}")
def delete_discussion(username: str, id: UUID):
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    elif discussion_posts.get(id) is None:
        return {"message": "post does not exist"}
    else:
        del discussion_posts[id]
        return {"message": "main post deleted"}
