from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    Director = Column(String)


