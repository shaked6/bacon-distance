from src.data_structures.actor import Actor
from src.models.db_actor import DBActor
from src.models.db_actor_movie import DBActorMovie
from src.models.db_session_manager import DBSessionManager


class DBWriter:
    def __init__(self):
        self.db_session_manager = DBSessionManager()

    def upsert_actor(self, actor: Actor):
        with self.db_session_manager.session() as session:
            db_actor = session.query(DBActor).filter_by(name=actor.name).first()
            if db_actor:
                db_actor.bacon_distance = actor.bacon_distance
            else:
                session.add(DBActor(
                    name=actor.name,
                    bacon_distance=actor.bacon_distance
                ))

    def upsert_actor_movie(self, actor_name: str, movie_title: str):
        with self.db_session_manager.session() as session:
            exists = session.query(DBActorMovie).filter_by(
                actor_name=actor_name,
                movie_title=movie_title
            ).first()

            if not exists:
                session.add(DBActorMovie(
                    actor_name=actor_name,
                    movie_title=movie_title
                ))

    def bulk_upsert_actors(self, actors: dict[str, Actor]):
        for actor in actors.values():
            self.upsert_actor(actor)

    def bulk_upsert_actor_movies(self, actors_movies: dict[str, list[str]]):
        for actor_name, movies in actors_movies.items():
            for movie in set(movies):
                self.upsert_actor_movie(actor_name, movie)

    def update_bacon_distances(self, actors: dict[str, Actor]):
        with self.db_session_manager.session() as session:
            for name, actor in actors.items():
                session.query(DBActor).filter_by(name=name).update(
                    {"bacon_distance": actor.bacon_distance}
                )
