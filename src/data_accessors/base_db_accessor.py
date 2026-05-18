from abc import ABC, abstractmethod


class BaseDBAccessor(ABC):

    @abstractmethod
    def get_bacon_distance(self, actor_name: str) -> str:
        pass
