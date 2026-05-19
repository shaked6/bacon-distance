from sqlalchemy import Column, String, Integer

from src.models.base import Base
from src.models.table_consts import ACTORS


class DBActor(Base):
    __tablename__ = ACTORS

    name = Column(String, primary_key=True)
    bacon_distance = Column(Integer)
