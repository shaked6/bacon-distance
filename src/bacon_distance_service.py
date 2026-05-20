from src.bfs_utils import compute_bacon_distances
from src.data_accessors.base_db_accessor import BaseDBAccessor
from src.data_accessors.db_writer import DBWriter
from src.data_structures.actor import Actor


class BaconDistanceService:
    def __init__(self, data_accessor: BaseDBAccessor, data_writer: DBWriter):
        self.data_accessor = data_accessor
        self.data_writer = data_writer

    def recompute(self):
        actors = {
            name: Actor(name=name, movies=self.data_accessor.get_movies_for_actor(name))
            for name in self.data_accessor.get_all_actor_names()
        }

        distances = compute_bacon_distances(actors)

        for name, actor in actors.items():
            actor.bacon_distance = distances.get(name, -1)
            actor.bump_version()

        self.data_writer.update_bacon_distances(actors)