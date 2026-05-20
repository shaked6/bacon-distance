from collections import deque

from src.consts import KEVIN_BACON
from src.data_structures.actor import Actor


def build_compact_adjacency(actors: dict[str, Actor]) -> dict[str, set[str]]:
    movie_to_cast = {}

    for name, actor in actors.items():
        for movie in actor.movies:
            movie_to_cast.setdefault(movie, set()).add(name)

    adjacency = {name: set() for name in actors}

    for cast in movie_to_cast.values():
        cast_list = list(cast)
        for i in range(len(cast_list)):
            for j in range(i + 1, len(cast_list)):
                a, b = cast_list[i], cast_list[j]
                adjacency[a].add(b)
                adjacency[b].add(a)

    return adjacency


def bfs_from_bacon(adjacency: dict[str, set[str]]) -> dict[str, int]:
    if KEVIN_BACON not in adjacency:
        return {}

    distance = {KEVIN_BACON: 0}
    queue = deque([KEVIN_BACON])

    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                queue.append(v)

    return distance


def compute_bacon_distances(actors: dict[str, Actor]) -> dict[str, Actor]:
    adjacency = build_compact_adjacency(actors)
    distance = bfs_from_bacon(adjacency)

    for name, actor in actors.items():
        actor.bacon_distance = distance.get(name, -1)

    print("Computed Bacon distances")
    return actors
