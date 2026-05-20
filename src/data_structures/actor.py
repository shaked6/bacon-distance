from typing import Optional


class Actor:
    def __init__(self, name: str, movies: Optional[list[str]] = None):
        self.name = name
        self.movies = movies or []
        self.bacon_distance = -1

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "movies": self.movies,
            "bacon_distance": self.bacon_distance,
        }

    @staticmethod
    def from_dict(name: str, data: dict) -> "Actor":
        actor = Actor(name=name, movies=data.get("movies", []))
        actor.bacon_distance = data.get("bacon_distance", -1)
        return actor
