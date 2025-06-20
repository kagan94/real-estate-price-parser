import sqlite3
from typing import List
from parsers.kvee_parser import KvEeListing
from parsers.city24_parser import City24Listing
from parsers.kinnisvara24_parser import Kinnisvara24Listing


class Database:
    def __init__(self, db_path: str = 'listings.db'):
        self.conn = sqlite3.connect(db_path)
        # TODO: Create tables if not exist

    def save_kvee_listings(self, listings: List[KvEeListing]):
        # TODO: Implement saving KvEeListing objects to DB
        pass

    def save_city24_listings(self, listings: List[City24Listing]):
        # TODO: Implement saving City24Listing objects to DB
        pass

    def save_kinnisvara24_listings(self, listings: List[Kinnisvara24Listing]):
        # TODO: Implement saving Kinnisvara24Listing objects to DB
        pass

    def close(self):
        self.conn.close()
