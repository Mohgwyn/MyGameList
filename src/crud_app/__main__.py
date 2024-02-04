import os
import argparse

from db import DataBase
from db.mongo import MongoDataBase

from auth import login, logout


connection_string = os.getenv('CRUD_APP_CONNECTION_STRING')
if connection_string is None:
    print(
        "Provide the MongoDB Connection String via the environment variable CRUD_APP_CONNECTION_STRING"
    )
    exit(-1)
print(connection_string)
connection_string.replace("<password>", "jEMV5dRc55rn3QY6")
print(connection_string)


def main(): 
    parser = argparse.ArgumentParser(description='CRUD operations over MyGameListDB')

    subparsers = parser.add_subparsers(help='Subcommands', dest='command')

    login_parser = subparsers.add_parser('login', help='Login to the DB')
    login_parser.add_argument('--user', help='User to authenticate as', required=True)

    logout_parser = subparsers.add_parser('logout', help='Logout of the DB')

    create_parser = subparsers.add_parser('add', help='Add a game to the DB')
    create_parser.add_argument('--title', help='Name of the game', required=True)
    create_parser.add_argument('--hours', help='Time spent (hours)', required=True)
    create_parser.add_argument('--start-date', help='Game start date', required=True)
    create_parser.add_argument('--finish-date', help='Game finish date', required=True)
    create_parser.add_argument('--platform', help='Platform played on', required=True)
    create_parser.add_argument('--developer', help='Developer of the game', required=True)
    create_parser.add_argument('--rating', help='Rating of the game', required=True)

    search_parser = subparsers.add_parser('search', help='Search in the game db')
    search_parser.add_argument('--title', help='Name of the game', default=None)
    search_parser.add_argument('--developer', help='Developer of the game', default=None)


    args = parser.parse_args()


    db: DataBase = MongoDataBase(connection_string)

    operaciones = {
        "login": login(user=args.user, db=db),
        "logout": logout(),
        "add": db.add_game(args.title, args.hours, args.start_date, args.finish_date, args.platform, args.developer, args.rating),
        "search": db.search_game_by(args.title, args.developer),
        "update": None,
        "delete": None,
    }
    operaciones[args.command]

    db.sync()


if __name__ == "__main__":
    main()