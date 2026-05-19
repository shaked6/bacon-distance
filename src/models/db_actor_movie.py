from sqlalchemy import Column, String, ForeignKey

from .base import Base
from .table_consts import ACTOR_MOVIES


class DBActorMovie(Base):
    __tablename__ = ACTOR_MOVIES

    actor_name = Column(String, ForeignKey("actors.name"), primary_key=True)
    movie_title = Column(String, primary_key=True)
