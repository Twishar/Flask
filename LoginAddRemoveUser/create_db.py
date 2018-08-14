
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///users.db')
Base = declarative_base()


class Users(Base):
    """"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    parent_name = Column(String, default='')
    password = Column(String)

    def __init__(self, name, password, parent_name):

        self.name = name
        self.password = password
        self.parent_name = parent_name


Base.metadata.create_all(engine)
