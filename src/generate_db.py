import gzip
import os
from typing import Optional

from fastapi import requests

from src.actor_json_utils import write_actors_to_json, build_actor_objects
from src.bfs_utils import compute_initial_bacon_distances
from src.consts import ACTOR_CATEGORIES, REQUIRED_ACTORS, DATA_DIR, DB_DIR


def create_dir_if_not_exists(directory: str) -> None:
    if not os.path.isdir(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")


def build_path(directory: str, filename: str) -> str:
    return os.path.join(directory, filename)


def download_if_missing(url: str, directory: Optional[str], filename: str) -> str:
    path = build_path(directory=directory, filename=filename)

    if os.path.exists(path):
        print(f"Skipping download, exists: {path}")
        return path

    print(f"Downloading {url}")
    response = requests.get(url)
    response.raise_for_status()

    with open(path, "wb") as f:
        f.write(response.content)

    print(f"Saved: {path}")
    return path


def stream_tsv(path: str) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            yield dict(zip(header, line.strip().split("\t")))


def get_actor_id_by_name(names_path: str, target_name: str) -> Optional[tuple[str, str]]:
    for row in stream_tsv(names_path):
        if row["primaryName"] == target_name:
            professions = row["primaryProfession"]
            if is_actor(professions):
                return row["nconst"], row["primaryName"]
    return None


def is_actor(professions: list) -> bool:
    return professions is not None and ("actor" in professions or "actress" in professions)


def load_n_actors(names_path: str, num_of_actors: int) -> dict[str, str]:
    actors = {}
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
        result = get_actor_id_by_name(names_path=names_path, target_name=name)
        if result is not None:
            actor_id, actor_name = result
            actors[actor_id] = actor_name
        else:
            print(f"ERROR: Could not find {name} in TSV!")
            raise Exception("Failed to boot app missing required actors")


def map_actors_movies_ids(actor_ids: set[str], principals_path: str) -> dict[str, set[str]]:
    actors_movies = {actor_id: set() for actor_id in actor_ids}

    for row in stream_tsv(principals_path):
        actor_id = row["nconst"]
        if actor_id in actor_ids and row["category"] in ACTOR_CATEGORIES:
            actors_movies[actor_id].add(row["tconst"])
    return actors_movies


def movie_id_to_title(movie_ids: set[str], titles_path: str) -> dict[str, str]:
    movie_titles = {}
    for row in stream_tsv(titles_path):
        if row["tconst"] in movie_ids and row["titleType"] == "movie":
            movie_titles[row["tconst"]] = row["primaryTitle"]
    return movie_titles


def build_actor_movie_map(principals_path: str,
                          titles_path: str,
                          actors: dict[str, str]) -> dict[str, list[str]]:
    actor_ids = set(actors.keys())
    actors_movies = map_actors_movies_ids(actor_ids=actor_ids, principals_path=principals_path)
    all_movie_ids = {movie_id for movie_ids in actors_movies.values() for movie_id in movie_ids}
    movie_titles = movie_id_to_title(movie_ids=all_movie_ids, titles_path=titles_path)

    return {
        actors[actor_id]: [
            movie_titles[movie_id] for movie_id in movie_ids if movie_id in movie_titles
        ]
        for actor_id, movie_ids in actors_movies.items()
    }


def main():
    create_dir_if_not_exists(DATA_DIR)
    create_dir_if_not_exists(DB_DIR)

    principals_path = download_if_missing(
        url="https://datasets.imdbws.com/title.principals.tsv.gz",
        directory=DATA_DIR,
        filename="title.principals.tsv.gz"
    )
    names_path = download_if_missing(
        url="https://datasets.imdbws.com/name.basics.tsv.gz",
        directory=DATA_DIR,
        filename="name.basics.tsv.gz"
    )
    titles_path = download_if_missing(
        url="https://datasets.imdbws.com/title.basics.tsv.gz",
        directory=DATA_DIR,
        filename="title.basics.tsv.gz"
    )

    actors_path = f"{DB_DIR}/actors.json"

    actors = load_n_actors(names_path, num_of_actors=10)
    ensure_required_actors(names_path, actors)
    actors_movies = build_actor_movie_map(principals_path=principals_path, titles_path=titles_path, actors=actors)
    actors = build_actor_objects(actors_movies)
    actors = compute_initial_bacon_distances(actors=actors)
    write_actors_to_json(path=actors_path, actors=actors)

    print("JSON written to actors.json")


if __name__ == "__main__":
    main()
