import json
import os
from http.client import HTTPException

from pywin.dialogs import status

from src.data_accessors.base_db_accessor import BaseDBAccessor


class JsonDBAccessor(BaseDBAccessor):
    def __init__(self, db_path: str):
        if not os.path.exists(db_path):
            raise Exception(f"Actors DB not found at {db_path}. Initialize it first.")

        self.db_path = db_path
        self.db = self._load()

    def _load(self) -> dict:
        with open(self.db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_bacon_distance(self, actor_name: str) -> str:
        normalized = actor_name.strip().lower()

        for name, info in self.db.items():
            if name.lower() == normalized:
                dist = info.get("bacon_distance", -1)
                return "infinity" if dist == -1 else str(dist)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Actor '{actor_name}' does not exist in the database."
        )
