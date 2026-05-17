from typing import Optional


class Actor:
    def __init__(self, name: str, movies: list[Optional[str]] = None):
        self.name = name
        self.movies = movies or [] # todo not like this?

        # -1 means "infinite distance" (unreachable)
        self.distance: int = -1
        self.closest_actor: str | None = None
        self.shortest_path: list[str] = []

    def to_dict(self):
        return {
            "movies": self.movies,
            "distance": self.distance,
            "closest_actor": self.closest_actor,
            "shortest_path": self.shortest_path
        }

    @staticmethod
    def from_dict(name: str, data: dict):
        actor = Actor(name=name, movies=data.get("movies", []))
        actor.distance = data.get("distance", -1)
        actor.closest_actor = data.get("closest_actor")
        actor.shortest_path = data.get("shortest_path", [])
        return actor
