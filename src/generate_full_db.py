from math import inf
from collections import deque

from src.data_structures.actor import Actor
from src.export_json import load_actor_json, write_actor_json


# ---------------------------------------------------------
# Build adjacency list
# ---------------------------------------------------------
def build_adjacency_list(actors: dict[str, Actor]) -> dict[str, set[str]]:
    """
    Build actor → connected actors adjacency list.
    Two actors are connected if they share at least one movie.
    """
    movie_to_actors: dict[str, set[str]] = {}

    # Reverse index: movie → actors
    for actor in actors.values():
        for movie in actor.movies:
            movie_to_actors.setdefault(movie, set()).add(actor.name)

    # Build adjacency list
    adjacency = {name: set() for name in actors}

    for cast in movie_to_actors.values():
        for a in cast:
            adjacency[a].update(cast - {a})

    return adjacency


# ---------------------------------------------------------
# BFS from Kevin Bacon
# ---------------------------------------------------------
def compute_bacon_distances(actors: dict[str, Actor],
                            adjacency: dict[str, set[str]]) -> None:
    """
    BFS starting from Kevin Bacon.
    Assigns:
      - distance (∞ initially)
      - closest_actor
      - shortest_path
    """
    if "Kevin Bacon" not in actors:
        raise ValueError("Kevin Bacon must exist in the dataset.")

    # Initialize all distances to infinity
    for actor in actors.values():
        actor.distance = -1
        actor.closest_actor = None
        actor.shortest_path = []

    # BFS setup
    queue = deque()
    bacon = actors["Kevin Bacon"]
    bacon.distance = 0
    bacon.shortest_path = ["Kevin Bacon"]
    queue.append("Kevin Bacon")

    # BFS loop
    while queue:
        current = queue.popleft()
        current_actor = actors[current]

        for neighbor in adjacency[current]:
            neighbor_actor = actors[neighbor]

            # If not visited yet
            if neighbor_actor.distance == -1:
                neighbor_actor.distance = current_actor.distance + 1
                neighbor_actor.closest_actor = current
                neighbor_actor.shortest_path = current_actor.shortest_path + [neighbor]
                queue.append(neighbor)


def compute_initial_bacon_distances(json_path: str):
    actors = load_actor_json(json_path)
    adjacency = build_adjacency_list(actors)
    compute_bacon_distances(actors, adjacency)
    write_actor_json(json_path, actors)

    print("Initial Bacon distances computed and saved to", json_path)
