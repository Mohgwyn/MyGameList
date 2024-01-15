import sys
import click
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json


mongo_client = None
games_db = None


def create(title, developer, year, pegi, rating):
    print(games_db.list_collection_names())
    doc = {
        'title': title,
        'developer': developer,
        'year': year,
        'pegi': pegi,
        'rating': rating
    }
    res = games_db['mohgwyn16'].insert_one(doc)
    print(res.acknowledged)
    print(res.inserted_id)
    

def read(developer, year, rating):
    """Lee juegos de la base de datos

    Obtiene aquellos juegos que tengan el developer/year/rating especificado en la base de datos

    Parametros
    ----------

    --developer: Desarrollador por el que filtrar
    --year: Año por el que filtrar
    --rating: Valoración por la que filtrar
    """

    pipeline = []
    if (developer or year or rating):
        if developer:
            pipeline.append({'$match': {'developer': developer}})
        if year:
            pipeline.append({'$match': {'year': year}})
        if rating:
            pipeline.append({'$match': {'rating': rating}})
    
        games_db['mohgwyn16'].aggregate(pipeline)
    else:
        pass #Error


def update(title, rating):
    """Actualiza rating

    Actualiza la puntuación de un juego según su nombre

    Parametros
    ----------

    --title: Título del juego que se quiere actualizar
    --rating: Puntuación actualizada
    """

    filter = {'title': title}
    update_value = {'$set': {'rating': rating}}
    games_db['mohgwyn16'].update_one(filter, update_value)


def delete(title):
    """Borra juego

    Permite borra un juego de la lista a través de su título

    Parametros
    ----------

    --title: Titulo del juego que se quiere borrar
    """

    games_db['mohgwyn16'].delete_one({'title': title})


@click.command
@click.option('--function', 
              type=click.Choice(['c', 'r', 'u', 'd'], case_sensitive=False),
              help= """Enter c to call create function\n
                       Enter r to call read function\n
                       Enter u to call update function\n
                       Enter d to call delete function\n"""
              )
@click.option('--title')
@click.option('--developer')
@click.option('--year', type=int)
@click.option('--pegi', type=int)
@click.option('--rating', type=int)
def cli_manager(function, title, developer, year, pegi, rating):
    operaciones = {
        'c': create(title, developer, year, pegi, rating),
        'r': read(developer, year, rating),
        'u': update(title, rating),
        'd': delete(title)
    }
    
    operaciones[function]


def mongo_connect():
    try:
        uri = f"mongodb+srv://python_client:WqPhsyelSCLDIygt@cluster0.rodolom.mongodb.net/?retryWrites=true&w=majority"
        mongo_client = MongoClient(uri, server_api=ServerApi('1'))
        mongo_client.admin.command('ping')
        print("You successfully connected to MongoDB!")
        games_db = mongo_client.games
        return games_db
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    games_db = mongo_connect()
    cli_manager()
    mongo_client.close()
    