from abc import ABC, abstractmethod


class BaseDBAccessor(ABC):

    @abstractmethod
    def get_bacon_distance(self, actor_name: str) -> str:
        pass

    @abstractmethod
    def get_all_actor_names(self) -> list[str]:
        pass

    @abstractmethod
    def get_movies_for_actor(self, actor_name: str) -> list[str]:
        pass
