import json
import os

from src.data_accessors.base_db_accessor import BaseDBAccessor
from src.exceptions.actor_not_found_exception import ActorNotFoundException


class JsonDBAccessor(BaseDBAccessor):

    def __init__(self, db_path: str):
        if not os.path.exists(db_path):
            raise Exception(f"Actors DB not found at {db_path}. Initialize it first.")
        self.db_path = db_path
        self.db = self._load()

    def _load(self) -> dict:
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_all_actor_names(self) -> list[str]:
        return list(self.db)

    def get_movies_for_actor(self, actor_name: str) -> list[str]:
        if actor_name in self.db:
            return self.db[actor_name]
        return []

    def get_bacon_distance(self, actor_name: str) -> str:
        normalized = actor_name.strip().lower()

        for name, info in self.db.items():
            if name.lower() == normalized:
                dist = info.get("bacon_distance", -1)
                return "infinity" if dist == -1 else str(dist)

        raise ActorNotFoundException(actor_name=actor_name)
