import json

from src.data_structures.actor import Actor


def build_actor_objects(actor_to_movies: dict[str, list[str]]) -> dict[str, Actor]:
    actors: dict[str, Actor] = {}

    for actor_name, movie_list in actor_to_movies.items():
        actors[actor_name] = Actor(name=actor_name, movies=movie_list)

    return actors


def write_actors_to_json(path: str, actors: dict[str, Actor]) -> None:
    data = {name: actor.to_dict() for name, actor in actors.items()}

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_actor_json(path: str) -> dict[str, Actor]:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return {name: Actor.from_dict(name, info) for name, info in raw.items()}
