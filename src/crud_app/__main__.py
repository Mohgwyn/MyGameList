import os
import argparse
import getpass

from db import DataBase
from db.mongo import MongoDataBase

from auth import login, logout, signup, is_logged_in


connection_string = os.getenv('CRUD_APP_CONNECTION_STRING')
if connection_string is None:
    print("Provide the MongoDB Connection String via the environment variable CRUD_APP_CONNECTION_STRING")
    exit(-1)

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)


def main(): 
    parser = argparse.ArgumentParser(description='CRUD operations over MyGameListDB')

    subparsers = parser.add_subparsers(help='Subcommands', dest='command')

    signup_parser = subparsers.add_parser('signup', help='signup user')
    signup_parser.add_argument('--user', help='Name of the game')
    signup_parser.add_argument('--password', action=Password, dest='password', help='Developer of the game')

    login_parser = subparsers.add_parser('login', help='Login to the DB')
    login_parser.add_argument('--user', help='User to authenticate as', required=True)
    login_parser.add_argument('--password', action=Password, dest='password', help='Developer of the game')

    logout_parser = subparsers.add_parser('logout', help='Logout of the DB')

    create_parser = subparsers.add_parser('add', help='Add a game to the DB')
    create_parser.add_argument('--title', help='Name of the game', required=True)
    create_parser.add_argument('--hours', help='Time spent (hours)', required=True)
    create_parser.add_argument('--start-date', help='Game start date', required=True)
    create_parser.add_argument('--finish-date', help='Game finish date', required=True)
    create_parser.add_argument('--rating', help='Rating of the game', required=True)

    search_parser = subparsers.add_parser('search', help='Search in the game db')
    search_parser.add_argument('--title', help='Name of the game', default=None)
    search_parser.add_argument('--developer', help='Developer of the game', default=None)


    args = parser.parse_args()
    print(args)

    db: DataBase = MongoDataBase(connection_string)


    user_logged = is_logged_in(db)
    if user_logged is not None:
        if args.command == "search":
            # Not implemented
            #db.search_game_by(args.title, args.developer)
            pass
        elif args.command == "add":
            db.add_game(user_logged, args.title, args.hours, args.start_date, args.finish_date, args.rating)
        elif args.command == "update":
            # Not implemented
            #db.update(args.title, args.rating)
            pass
        elif args.command == "delete":
            db.delete_game(args.title)
        elif args.command == "logout":
            logout()
        else:
            print("Invalid command when logged in")
    else: 
        if args.command == "login":
            login(user=args.user, password=args.password, db=db)
        elif args.command == "signup":
            signup(db, args.user, args.password)
        else:
            print("Invalid command when not logged in")


    db.sync()


if __name__ == "__main__":
    main()