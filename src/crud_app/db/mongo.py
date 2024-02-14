from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from db import DataBase


class MongoDataBase(DataBase):

    def __init__(self, mongo_connection_str: str):
        self._client = MongoClient(mongo_connection_str, server_api=ServerApi("1"))
        self._db = self._client["MyGameList"]
        self._users = self._db["user_list"]


    def add_game(self, user: str, title: str, hours: float, start_date: datetime, finish_date: datetime, rating: float):
        """Add game

        Adds a game to the user list of games

        Parametres
        ----------

        --title: Title of the game to add
        --hours: Hours spennt on the game
        --start-date: Date in dd/mm/YYYY format when user started playing
        --finish-date: Date in dd/mm/YYYY format when user rolled credits
        --rating: Rating of the game out of 10
        """
        nuevo_juego = {
            "title": title,
            "hours": float(hours),
            "start_date": datetime.strptime(start_date, '%d/%m/%Y'),
            "finish_date": datetime.strptime(finish_date, '%d/%m/%Y'),
            "rating": float(rating),
        }
        res = self._users.update_one(
            {"user": user},
            {"$push": {"game_list": nuevo_juego}})

    
    def search_game_by(self, developer: str, year: int, rating: int):
        """Lee juegos de la base de datos

        Obtiene aquellos juegos que tengan el developer/year/rating especificado en la base de datos

        Parametros
        ----------

        --developer: Desarrollador por el que filtrar
        --year: Año por el que filtrar
        --rating: Valoración por la que filtrar
        """

        pipeline = []
        if developer or year or rating:
            if developer:
                pipeline.append({"$match": {"developer": developer}})
            if year:
                pipeline.append({"$match": {"year": year}})
            if rating:
                pipeline.append({"$match": {"rating": rating}})

            self._users.aggregate(pipeline)
        else:
            pass  # Error
    

    def delete_game(self, user: str, title: str):
        """Delete game

        Deletes a game from the user game list by title

        Parametres
        ----------

        --title: Title of the game to drop from game list
        """
        drop_criterion = {
            'game_list': {
                'title': title
            }
        }
        res = self._users.update_one(
            {"user": user},
            {"$pull": drop_criterion}
        )

    
    def update(self, title: str, rating: int):
        """Actualiza rating

        Actualiza la puntuación de un juego según su nombre

        Parametros
        ----------

        --title: Título del juego que se quiere actualizar
        --rating: Puntuación actualizada
        """

        filter = {"title": title}
        update_value = {"$set": {"rating": rating}}
        self._users.update_one(filter, update_value)
    

    def create_user(self, user: str, hashed_pw: str):
        # comprobar que el usuario es unico
        if self._users.find_one({'user': user}) is None:
            new_user = {
                'user': user,
                'password': hashed_pw,
                'game_list': []
            }
            self._users.insert_one(new_user)
            return True
        else: 
            return False


    def user_exists(self, user: str):
        response = self._users.find_one({'user': user})
        return response

        
    def sync(self):
        ...