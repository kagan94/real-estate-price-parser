from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from parsers.city24_parser import City24Listing
from parsers.kinnisvara24_parser import Kinnisvara24Listing
from parsers.kvee_parser import KvEeListing
from .models import KvEeListingModel, City24ListingModel, Kinnisvara24ListingModel, Base


class Database:
    def __init__(self):
        db_path = 'sqlite:///real_estate_prices.db'
        self.session = create_engine_and_session(db_path)

    def save_kvee_listings(self, listings: List[KvEeListing]):
        for listing in listings:
            db_listing = KvEeListingModel(
                id=listing.id,
                address=listing.address,
                rooms=listing.rooms,
                area_m2=listing.area_m2,
                price=listing.price,
                price_m2=listing.price_m2,
                link=listing.link,
                first_img_url=listing.first_img_url,
                object_important_note=listing.object_important_note,
                description=listing.description,
                date_activated=listing.date_activated,
                advertisement_level=listing.advertisement_level,
                floor=listing.floor,
                total_floors=listing.total_floors,
                year_built=listing.year_built,
            )
            self.session.merge(db_listing)
        self.session.commit()

    def save_city24_listings(self, listings: List[City24Listing]):
        for listing in listings:
            db_listing = City24ListingModel(
                id=listing.id,
                address=listing.address,
                rooms=listing.rooms,
                area_m2=listing.area_m2,
                year_built=listing.year_built,
                price=listing.price,
                price_m2=listing.price_m2,
                link=listing.link,
                main_img_url=listing.main_img_url,
                description=listing.description
            )
            self.session.merge(db_listing)
        self.session.commit()

    def save_kinnisvara24_listings(self, listings: List[Kinnisvara24Listing]):
        for listing in listings:
            db_listing = Kinnisvara24ListingModel(
                id=listing.id,
                address=listing.address,
                rooms=listing.rooms,
                area_m2=listing.area_m2,
                year_built=listing.year_built,
                price=listing.price,
                price_m2=listing.price_m2,
                link=listing.link,
                main_img_url=listing.main_img_url,
                description=listing.description,
                created_at=listing.created_at
            )
            self.session.merge(db_listing)
        self.session.commit()

    def close(self):
        self.session.close()


def create_engine_and_session(db_path: str):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
