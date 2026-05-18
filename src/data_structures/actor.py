from typing import Optional


class Actor:
    def __init__(self, name: str, movies: Optional[list[str]] = None):
        self.name = name
        self.movies = movies or []
        self.neighbors = []
        self.bacon_distance = -1
        self.bacon_parent = None
        self.version = 0

    def bump_version(self):
        self.version += 1

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "movies": self.movies,
            "neighbors": self.neighbors,
            "bacon_distance": self.bacon_distance,
            "bacon_parent": self.bacon_parent,
            "version": self.version
        }

    @staticmethod
    def from_dict(name: str, data: dict) -> "Actor":
        actor = Actor(name=name, movies=data.get("movies", []))
        actor.neighbors = data.get("neighbors", [])
        actor.bacon_distance = data.get("bacon_distance", -1)
        actor.bacon_parent = data.get("bacon_parent")
        actor.version = data.get("version", 0)
        return actor
