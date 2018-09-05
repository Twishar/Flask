
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///payments.db', echo=True)
Base = declarative_base()


class Payments(Base):
    """"""
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    payment_amount = Column(Float)
    payment_currency = Column(String)
    description = Column(Text)

    def __init__(self, payment_amount, payment_currency, description):

        self.payment_amount = payment_amount
        self.payment_currency = payment_currency
        self.description = description


Base.metadata.create_all(engine)
