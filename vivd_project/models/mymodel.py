import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    String,
    Float,
    Boolean,
    DateTime,
    PrimaryKeyConstraint
)

from .meta import Base


class seed(Base):
    __tablename__ = 'seed'
    event_id = Column(Integer, primary_key = True)
    section = Column(String(255))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, default=0.00, nullable=False)
    rownum = Column(String(255))

class tickets(Base):
    __tablename__ = 'tickets'
    event_id = Column(Integer, primary_key = True)
    section = Column(String(255), primary_key = True)
    rownum = Column(String(255), primary_key = True)
    seat = Column(String(255), primary_key = True)
    price = Column(Float, default=0.00, nullable=False)
    seller_id = Column(String(255), nullable=False)
    status =  Column(Boolean, primary_key = True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    PrimaryKeyConstraint('event_id', 'section','rownum','seat','status' , name='tickets_pk')
    Index('idx_tickets_on_event_id', event_id)

    def __str__(self):
        return str(self.event_id)

class sessions(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, nullable=False,primary_key=True , autoincrement=True)
    session_data =  Column(String(255))
    event_id = Column(Integer)
    buyer_id = Column(Integer)
    referral = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class events(Base):
    __tablename__ = 'events'
    id = Column(Integer, nullable=False,primary_key=True , autoincrement=True)
    name =  Column(String(255))
    type = Column(Integer)
    venue_id = Column(Integer, nullable=False)
    event_dt = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    Index('idx_events_on_venue_id', venue_id)
    Index('idx_events_on_event_dt', event_dt)

class venues(Base):
    __tablename__ = 'venues'
    id = Column(Integer, nullable=False,primary_key=True , autoincrement=True)
    name =  Column(String(255))
    address_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class seats(Base):
    __tablename__ = 'seats'
    id = Column(Integer, nullable=False,primary_key=True , autoincrement=True)
    venue_id =  Column(Integer, nullable=False)
    section = Column(String(255))
    rownum = Column(String(255))
    seat = Column(String(255))
    best_rank = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    Index('idx_seats_on_venue_id', venue_id)

class addresses(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, nullable=False,primary_key=True , autoincrement=True)
    address1 =  Column(String(255))
    address2 = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zipcode = Column(String(255))
    phone = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    Index('idx_addresses_on_city', city)



