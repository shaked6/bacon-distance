import gzip

from src.data.consts import KEVIN_BACON_NAME, KEVIN_BACON_MOVIES, ACTOR_CATEGORIES
from src.export_json import write_actor_json, build_actor_objects
from src.generate_full_db import compute_initial_bacon_distances


def stream_tsv(path: str) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        header = f.readline().strip().split("\t")
        for line in f:
            yield dict(zip(header, line.strip().split("\t")))


def load_n_actors(names_path: str, num_of_actors: int) -> dict[str, str]:
    actors: dict[str, str] = {}
    count = 0

    for row in stream_tsv(names_path):
        professions = row["primaryProfession"]

        if professions and ("actor" in professions or "actress" in professions):
            actor_id = row["nconst"]
            actor_name = row["primaryName"]

            actors[actor_id] = actor_name
            count += 1

            if count >= num_of_actors:
                break

    return actors


def add_kevin_bacon(actors: dict[str, str]) -> None:
    actors["kbacon"] = KEVIN_BACON_NAME


def build_regular_actor_movie_map(principals_path: str,
                                  titles_path: str,
                                  actors: dict[str, str]) -> dict[str, list[str]]:
    actor_ids = {actor_id for actor_id in actors if actor_id != "kbacon"}

    actor_movies = {actor_id: set() for actor_id in actor_ids}

    for row in stream_tsv(principals_path):
        actor_id = row["nconst"]
        if actor_id in actor_ids and row["category"] in ACTOR_CATEGORIES:
            actor_movies[actor_id].add(row["tconst"])

    # Collect all movie IDs
    all_movie_ids = {movie_id for movie_ids in actor_movies.values() for movie_id in movie_ids}

    # Map movie IDs → titles
    movie_titles = {}
    for row in stream_tsv(titles_path):
        if row["tconst"] in all_movie_ids and row["titleType"] == "movie":
            movie_titles[row["tconst"]] = row["primaryTitle"]

    # Build final mapping
    return {
        actors[actor_id]: [
            movie_titles[movie_id] for movie_id in movie_ids if movie_id in movie_titles
        ]
        for actor_id, movie_ids in actor_movies.items()
    }


def build_bacon_movie_map(actors: dict[str, str]) -> dict[str, list[str]]:
    bacon_name = actors["kbacon"]
    return {bacon_name: list(KEVIN_BACON_MOVIES)}


def main():
    names_path = "data/name.basics.tsv.gz"
    principals_path = "data/title.principals.tsv.gz"
    titles_path = "data/title.basics.tsv.gz"

    # Load first N actors
    actors = load_n_actors(names_path, num_of_actors=15)

    # Add Kevin Bacon (constant)
    add_kevin_bacon(actors)

    # Build mapping
    actors_movies = build_actor_movie_map(principals_path, titles_path, actors)

    actors = build_actor_objects(actors_movies)

    # Write JSON
    write_actor_json("actors.json", actors)
    compute_initial_bacon_distances("actors.json")

    print("JSON written to actors.json")


def build_actor_movie_map(principals_path: str,
                          titles_path: str,
                          actors: dict[str, str]) -> dict[str, list[str]]:
    regular = build_regular_actor_movie_map(principals_path, titles_path, actors)
    bacon = build_bacon_movie_map(actors)

    return {**regular, **bacon}


if __name__ == "__main__":
    main()
