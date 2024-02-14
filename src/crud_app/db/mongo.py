from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

from db import DataBase
import bcrypt

class MongoDataBase(DataBase):

    def __init__(self, mongo_connection_str: str):
        self._client = MongoClient(mongo_connection_str, server_api=ServerApi("1"))
        self._db = self._client["MyGameList"]
        self._users = self._db["user_list"]


    def add_game(self, title: str, hours: float, start_date: datetime, finish_date: datetime, rating: float):
        nuevo_juego = {
            "title": title,
            "hours": float(hours),
            "start_date": datetime.strptime(start_date, '%d/%m/%Y'),
            "finish_date": datetime.strptime(finish_date, '%d/%m/%Y'),
            "rating": float(rating),
        }
        res = self._users.update_one(
            {"user": user_id},
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


    def delete_game(self, title: str):
        """Borra juego

        Permite borra un juego de la lista a través de su título

        Parametros
        ----------

        --title: Titulo del juego que se quiere borrar
        """

        self._users.delete_one({"title": title})


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


    def signup(self, user: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = {
            'user': user,
            'password': hashed_password,
            'game_list': []
        }

        self._users.insert_one(new_user)


    def user_exists(self, user: str, password: str):
        user_doc = self._users.find_one({'user': user})
        doc = None

        if bcrypt.checkpw(password.encode('utf-8'), user_doc['password']):
            doc = {'user_id': user,
                   'password': password}
            
        return doc


    def sync(self):
        ...