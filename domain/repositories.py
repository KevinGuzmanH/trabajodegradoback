from abc import ABC, abstractmethod

class MovieRepository(ABC):
    @abstractmethod
    def get_movie_info(self, title: str):
        pass
