from sqlalchemy.orm import Session

from src.data_structures.actor import Actor
from src.models.db_actor import DBActor
from src.models.db_actor_movie import DBActorMovie
from src.models.db_engine import SessionLocal


class DBWriter:
    def write_actors(self, actors: dict[str, Actor]):
        session: Session = SessionLocal()
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
        session: Session = SessionLocal()
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
