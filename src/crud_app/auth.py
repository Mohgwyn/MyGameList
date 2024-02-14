import os

from db import DataBase
import json


def login(user: str, password: str, db: DataBase):
    response = db.user_exists(user=user, password=password)

    if response is not None:
        with open(".cookie", "w") as f:
            f.write(json.dumps(response))
        print("Logged in as user with ID", str(response["user_id"]))
    else:
        print(f"Invalid user: {user}, contact your admin to create an account")


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
            doc = json.loads(f.read())
            if db.user_exists(user_id=doc['user_id'], password=['password']):
                return True
            else:
                return False
    except FileNotFoundError as _:
        return False
