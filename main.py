from datetime import date
from enum import Enum
from random import random
from string import ascii_lowercase
from fastapi import FastAPI
from bcrypt import checkpw, hashpw, gensalt
from typing import Optional, Dict, List
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

#
# Static routes
#


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


@app.get("/login/details/info")
def login_info():
    return {"message": "username and password needed"}


@app.delete("/login/remove/all")
def delete_users(username: List[str]):
    for user in username:
        del valid_users[user]
    return {"message": "deleted users"}


@app.delete("/delete/users/pending")
def delete_pending_users(accounts: List[str] = []):
    for user in accounts:
        del pending_users[user]
    return {"message": "deleted pending users"}


@app.get("/login/password/change")
def change_password(username: str, old_passw: str = '', new_passw: str = ''):
    passwd_len = 8
    if valid_users.get(username) is None:
        return {"message": "user does not exists"}
    elif old_passw == '' or new_passw == '':
        characters = ascii_lowercase
        temporary_passwd = ''.join(random.choice(characters)
                                   for i in range(passwd_len))
        user = valid_users.get(username)
        user.password = temporary_passwd
        user.passphrase = hashpw(temporary_passwd.encode(), gensalt())
        return user
    else:
        user = valid_users.get(username)
        if user.password == old_passw:
            user.password = new_passw
            user.passphrase = hashpw(new_passw.encode(), gensalt())
            return user
        else:
            return {"message": "invalud user"}


@app.post("/login/username/unlock")
def unlock_username(id: Optional[UUID] = None):
    if id is None:
        return {"message": "token needed"}
    else:
        for key, val in valid_users.items():
            if val.id == id:
                return {"username": val.username}
        return {"message": "user does not exist"}


@app.post("/login/password/unlock")
def unlock_password(username: Optional[str] = None, id: Optional[UUID] = None):
    if username is None:
        return {"message": "username is required"}
    elif valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        if id is None:
            return {"message": "token needed"}
        else:
            user = valid_users.get(username)
            if user.id == id:
                return {"password": user.password}
            else:
                return {"message": "invalid token"}


#
# Dynamic routes
#


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


@app.delete("/discussion/posts/remove/{username}")
def delete_discussion(username: str, id: UUID):
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    elif discussion_posts.get(id) is None:
        return {"message": "post does not exist"}
    else:
        del discussion_posts[id]
        return {"message": "main post deleted"}


@app.delete("/login/remove/{username}")
def delete_user(username: str):
    if username is None:
        return {"message": "invalid user"}
    else:
        del valid_users[username]
        return {"message": "user deleted"}


@app.get("/login/{username}/{password}")
def login_with_token(username: str, password: str, id: UUID):
    if valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        user = valid_users[username]
        if user.id == id and checkpw(password.encode(), user.passphrase):
            return user
        else:
            return {"message": "invalid user"}


@app.patch("/account/profile/update/names/{username}")
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
