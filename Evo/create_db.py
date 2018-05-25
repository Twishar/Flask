
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = create_engine('sqlite:///notes.db', echo=True)
Base = declarative_base()


class Note(Base):
    """"""
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    note_title = Column(String)
    note_body = Column(String)


    def __init__(self, note_title, note_body):

        self.note_title = note_title
        self.note_body = note_body


Base.metadata.create_all(engine)
