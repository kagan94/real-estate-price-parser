from sqlalchemy import Column, String, Integer, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ListingModelBase:
    # NB! This is a mixin. It is not a model.
    id = Column(String, primary_key=True)
    address = Column(Text)
    rooms = Column(Integer)
    area_m2 = Column(Float)
    price = Column(Integer)
    price_m2 = Column(Integer)
    link = Column(Text)
    img_url = Column(Text)


class KvEeListingModel(Base, ListingModelBase):
    __tablename__ = 'kvee_listing'

    object_important_note = Column(Text)
    description = Column(Text)
    date_activated = Column(String)
    advertisement_level = Column(Integer)
    floor = Column(Integer)
    total_floors = Column(Integer)
    year_built = Column(Integer)


class City24ListingModel(Base, ListingModelBase):
    __tablename__ = 'city24_listing'

    object_important_note = Column(Text)
    date_published = Column(Text)
    floor = Column(Integer)
    total_floors = Column(Integer)
    year_built = Column(Integer)
    latitude = Column(String)
    longitude = Column(String)


class Kinnisvara24ListingModel(Base, ListingModelBase):
    __tablename__ = 'kinnisvara24_listing'

    created_at = Column(String)
