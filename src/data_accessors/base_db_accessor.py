from abc import ABC, abstractmethod


class BaseDBAccessor(ABC):

    @abstractmethod
    def get_bacon_distance(self, actor_name: str) -> str:  # todo expand methods to include get_all_actors and get_actor_movies
        pass