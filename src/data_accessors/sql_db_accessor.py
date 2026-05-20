from src.data_accessors.base_db_accessor import BaseDBAccessor
from src.exceptions.actor_not_found_exception import ActorNotFoundException
from src.models.db_actor import DBActor
from src.models.db_actor_movie import DBActorMovie
from src.models.db_session_manager import DBSessionManager


class SQLDBAccessor(BaseDBAccessor):
    def __init__(self):
        self.db_session_manager = DBSessionManager()

    def get_bacon_distance(self, actor_name: str) -> str:
        with self.db_session_manager.session() as session:
            actor = session.query(DBActor).filter(DBActor.name.ilike(actor_name)).first()
            if actor is None:
                raise ActorNotFoundException(actor_name=actor_name)

            return str(actor.bacon_distance)

    def get_movies_for_actor(self, actor_name: str) -> list[str]:
        with self.db_session_manager.session() as session:
            rows = session.query(DBActorMovie).filter(DBActorMovie.actor_name == actor_name).all()
            return [row.movie_title for row in rows]

    def get_actors_in_movie(self, movie_title: str) -> list[str]:
        with self.db_session_manager.session() as session:
            rows = session.query(DBActorMovie).filter(DBActorMovie.movie_title == movie_title).all()
            return [row.actor_name for row in rows]

    def get_all_actor_names(self) -> list[str]:
        with self.db_session_manager.session() as session:
            return [row.name for row in session.query(DBActor).all()]
