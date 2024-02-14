import os

from db import DataBase
import bcrypt


def login(user: str, password: str, db: DataBase):
    response = db.user_exists(user=user)

    if response is not None:
        if bcrypt.checkpw(password.encode('utf-8'), response['password']):
            with open(".cookie", "w") as f:
                f.write(response['user'])
            return True
        else:
            return False


def logout():
    try:
        # Attempt to remove the file
        os.remove(".cookie")
        print(f"Logout succesfull")
    except OSError as e:
        # Handle the case where the file couldn't be removed (e.g., file not found)
        print(f"Error deleting file '.cookie'", e)


def is_logged_in(db: DataBase):
    try:
        with open(".cookie", "r") as f:
            user = f.read()
            if db.user_exists(user=user):
                return user
            else:
                return None
    except FileNotFoundError as _:
        return None
    

def signup(db: DataBase, user: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    if db.create_user(user, hashed_password):
        return True
    else:
        return False
    
