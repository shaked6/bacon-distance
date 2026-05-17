from collections import deque
from src.data.consts import KEVIN_BACON
from src.data_structures.actor import Actor
from src.export_json import load_actor_json, write_actors_to_json


# ---------------------------------------------------------
# Build adjacency: actor → list of (movie, other_actor)
# ---------------------------------------------------------
def build_actor_adjacency(actors: dict[str, Actor]) -> dict[str, list[tuple[str, str]]]:
    """
    adjacency[actor_name] = list of (movie_title, other_actor_name)
    """
    movie_to_actors: dict[str, set[str]] = {}

    # Reverse index: movie → actors
    for actor in actors.values():
        for movie in actor.movies:
            movie_to_actors.setdefault(movie, set()).add(actor.name)

    adjacency: dict[str, list[tuple[str, str]]] = {name: [] for name in actors}

    # Build adjacency with movie info
    for movie, cast in movie_to_actors.items():
        cast_list = list(cast)
        for i in range(len(cast_list)):
            for j in range(i + 1, len(cast_list)):
                a = cast_list[i]
                b = cast_list[j]

                adjacency[a].append((movie, b))
                adjacency[b].append((movie, a))

    return adjacency


# ---------------------------------------------------------
# BFS using actor → (movie, other_actor) edges
# ---------------------------------------------------------
def compute_bacon_distances(actors: dict[str, Actor],
                            adjacency: dict[str, list[tuple[str, str]]]) -> None:

    if KEVIN_BACON not in actors:
        raise ValueError(f"{KEVIN_BACON} must exist in the dataset.")

    # Reset all actors
    for actor in actors.values():
        actor.distance = -1
        actor.closest_actor = None
        actor.shortest_path = []

    # BFS init
    queue = deque([KEVIN_BACON])
    actors[KEVIN_BACON].distance = 0
    actors[KEVIN_BACON].shortest_path = [KEVIN_BACON]

    # BFS loop
    while queue:
        current = queue.popleft()
        current_actor = actors[current]

        for movie, neighbor in adjacency[current]:
            neighbor_actor = actors[neighbor]

            if neighbor_actor.distance == -1:
                neighbor_actor.distance = current_actor.distance + 1
                neighbor_actor.closest_actor = current

                # Insert movie between actors
                neighbor_actor.shortest_path = (
                    current_actor.shortest_path + [movie, neighbor]
                )

                queue.append(neighbor)


# ---------------------------------------------------------
# Main entry point for first-time computation
# ---------------------------------------------------------
def compute_initial_bacon_distances(json_path: str):
    actors = load_actor_json(json_path)
    adjacency = build_actor_adjacency(actors)
    compute_bacon_distances(actors, adjacency)
    write_actors_to_json(json_path, actors)
    print(f"Initial Bacon distances computed and saved to {json_path}")
