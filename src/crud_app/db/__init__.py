from abc import ABC, abstractmethod
from datetime import datetime


class DataBase(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def user_exists(self, user: str):
        pass

    @abstractmethod
    def add_game(
        self, title: str, hours: float, start_date: datetime, 
        finish_date: datetime, platform: str, developer: str, rating: int
    ):
        pass

    @abstractmethod
    def search_game_by(self, developer: str, year: int, rating: int):
        pass

    @abstractmethod
    def sync(self):
        pass
