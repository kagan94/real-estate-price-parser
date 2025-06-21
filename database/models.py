from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class KvEeListingModel(Base):
    __tablename__ = 'kvee_listing'

    id = Column(String, primary_key=True)
    address = Column(Text)
    rooms = Column(String)
    area_m2 = Column(String)
    price = Column(String)
    price_m2 = Column(String)
    link = Column(Text)
    img_url = Column(Text)
    object_important_note = Column(Text)
    description = Column(Text)
    date_activated = Column(String)
    advertisement_level = Column(Integer)
    floor = Column(String)
    total_floors = Column(String)
    year_built = Column(String)


class City24ListingModel(Base):
    __tablename__ = 'city24_listing'

    id = Column(String, primary_key=True)
    address = Column(Text)
    rooms = Column(String)
    area_m2 = Column(String)
    price = Column(Integer)
    price_m2 = Column(Integer)
    link = Column(Text)
    img_url = Column(Text)
    object_important_note = Column(Text)
    description = Column(Text)
    date_published = Column(Text)
    floor = Column(Text)
    total_floors = Column(Text)
    year_built = Column(String)
    latitude = Column(String)
    longitude = Column(String)


class Kinnisvara24ListingModel(Base):
    __tablename__ = 'kinnisvara24_listing'

    id = Column(String, primary_key=True)
    address = Column(Text)
    rooms = Column(String)
    area_m2 = Column(String)
    year_built = Column(String)
    price = Column(Integer)
    price_m2 = Column(Integer)
    link = Column(Text)
    img_url = Column(Text)
    description = Column(Text)
    created_at = Column(String)
