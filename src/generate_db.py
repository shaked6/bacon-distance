import gzip
from typing import Optional

from src.data.consts import ACTOR_CATEGORIES, REQUIRED_ACTORS
from src.export_json import write_actors_to_json, build_actor_objects
from src.generate_full_db import compute_initial_bacon_distances


def stream_tsv(path: str) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            yield dict(zip(header, line.strip().split("\t")))


def get_actor_id_by_name(names_path: str, target_name: str) -> Optional[tuple[str, str]]:  # todo i dont like tuples
    for row in stream_tsv(names_path):
        if row["primaryName"] == target_name:
            professions = row["primaryProfession"]
            if is_actor(professions):
                return row["nconst"], row["primaryName"]
    return None


def is_actor(professions: list) -> bool:
    return professions is not None and ("actor" in professions or "actress" in professions)

def load_n_actors(names_path: str, num_of_actors: int) -> dict[str, str]:
    actors: dict[str, str] = {}
    count = 0

    for row in stream_tsv(names_path):
        professions = row["primaryProfession"]

        if is_actor(professions):
            actor_id = row["nconst"]
            actor_name = row["primaryName"]

            actors[actor_id] = actor_name
            count += 1

            if count >= num_of_actors:
                break

    return actors


def ensure_required_actors(names_path: str, actors: dict[str, str]) -> None:
    for name in REQUIRED_ACTORS:
        result = get_actor_id_by_name(names_path, name)
        if result is not None:
            actor_id, actor_name = result
            actors[actor_id] = actor_name
        else:
            print(f"ERROR: Could not find {name} in TSV!")
            raise Exception # todo genuine boot failure


def main():
    names_path = "data/name.basics.tsv.gz"
    principals_path = "data/title.principals.tsv.gz"
    titles_path = "data/title.basics.tsv.gz"

    actors = load_n_actors(names_path, num_of_actors=10)
    ensure_required_actors(names_path, actors)
    actors_movies = build_actor_movie_map(principals_path, titles_path, actors)
    actors = build_actor_objects(actors_movies)
    write_actors_to_json("actors.json", actors)

    compute_initial_bacon_distances("actors.json")
    print("JSON written to actors.json")


def build_actor_movie_map(principals_path: str,
                          titles_path: str,
                          actors: dict[str, str]) -> dict[str, list[str]]:
    actor_ids = set(actors.keys())

    actor_movies = {actor_id: set() for actor_id in actor_ids}

    # Pass 1: collect movie IDs
    for row in stream_tsv(principals_path):
        actor_id = row["nconst"]
        if actor_id in actor_ids and row["category"] in ACTOR_CATEGORIES:
            actor_movies[actor_id].add(row["tconst"])

    all_movie_ids = {movie_id for movie_ids in actor_movies.values() for movie_id in movie_ids}

    # Map movie IDs → titles
    movie_titles = {}
    for row in stream_tsv(titles_path):
        if row["tconst"] in all_movie_ids and row["titleType"] == "movie":
            movie_titles[row["tconst"]] = row["primaryTitle"]

    return {
        actors[actor_id]: [
            movie_titles[movie_id] for movie_id in movie_ids if movie_id in movie_titles
        ]
        for actor_id, movie_ids in actor_movies.items()
    }


if __name__ == "__main__":
    main()
