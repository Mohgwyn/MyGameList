from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from db import DataBase

class MongoDataBase(DataBase):

    def __init__(self, mongo_connection_str: str):
        self._client = MongoClient(mongo_connection_str, server_api=ServerApi("1"))
        self._db = self._client["MyGameList"]
        self._games = self._db["games"]
        self._auth = self._db["auth"]


    def add_game(self, title: str, hours: float, start_date: datetime, finish_date: datetime, platform: str, developer: str, rating: int):
        doc = {
            "title": title,
            "hours": hours,
            "start_date": start_date,
            "finish_date": finish_date,
            "platform": platform,
            "developer": developer,
            "rating": rating,
        }
        res = self._games.insert_one(doc)


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

            self._games.aggregate(pipeline)
        else:
            pass  # Error


    def delete_game(self, title: str):
        """Borra juego

        Permite borra un juego de la lista a través de su título

        Parametros
        ----------

        --title: Titulo del juego que se quiere borrar
        """

        self._games.delete_one({"title": title})


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
        self._games.update_one(filter, update_value)


    def sync(self):
        ...

    def user_exists(self, user: str):
        return {"user_id": user} if self._auth.find_one({'user': user}) else None
