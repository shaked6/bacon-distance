from src.data_structures.actor import Actor
from src.models.db_actor import DBActor
from src.models.db_actor_movie import DBActorMovie
from src.models.db_engine import SessionLocal


class DBWriter:
    def write_actors(self, actors: dict[str, Actor]):
        session = SessionLocal()
        try:
            for actor_name, actor_obj in actors.items():
                session.add(DBActor(
                    name=actor_obj.name,
                    bacon_distance=actor_obj.bacon_distance
                ))
            session.commit()
            print("Wrote actors to db")
        finally:
            session.close()

    def write_actor_movies(self, actors_movies: dict[str, list[str]]):
        session = SessionLocal()
        try:
            for actor_name, movies in actors_movies.items():
                unique_movies = set(movies)

                for movie_title in unique_movies:
                    session.add(DBActorMovie(
                        actor_name=actor_name,
                        movie_title=movie_title
                    ))
            session.commit()
            print("Wrote actor's movies to db")
        finally:
            session.close()

    def insert_actor_if_not_exists(self, actor_name: str):
        session = SessionLocal()
        try:
            actor = session.query(DBActor).filter_by(name=actor_name).first()
            if actor:
                return

            session.add(DBActor(name=actor_name, bacon_distance=None))
            session.commit()
        finally:
            session.close()

    def link_actor_to_movie(self, actor_name: str, movie_name: str):
        session = SessionLocal()
        try:
            link = session.query(DBActorMovie).filter_by(
                actor_name=actor_name,
                movie_title=movie_name
            ).first()

            if link:
                return

            session.add(DBActorMovie(
                actor_name=actor_name,
                movie_title=movie_name
            ))
            session.commit()
        finally:
            session.close()

    def update_bacon_distances(self, actors: dict[str, Actor]):
        session = SessionLocal()
        try:
            for name, actor in actors.items():
                session.query(DBActor).filter_by(name=name).update(
                    {"bacon_distance": actor.bacon_distance}
                )
            session.commit()
            print("Updated Bacon distances in db")
        finally:
            session.close()
