import os

from db import DataBase


def login(user: str, db: DataBase):
    response = db.user_exists(user=user)
    print(response)

    if response is not None:
        with open(".cookie", "w") as f:
            f.write(str(response["user_id"]))
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
            user_id = f.read()
            if db.user_exists(user_id=user_id):
                return True
            else:
                return False
    except FileNotFoundError as _:
        return False
