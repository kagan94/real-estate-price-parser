from dataclasses import dataclass
from typing import List, Optional
import re
from xmlrpc.client import Error

import requests

from config import CITY24_BASE_URL, CITY24_API_SEARCH_URL
from .common import ListingBase, AddressComponents


@dataclass
class City24Listing(ListingBase):
    object_important_note: Optional[str]
    date_published: Optional[str]
    floor: Optional[int]
    total_floors: Optional[int]
    year_built: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]

class City24Parser:
    def parse(self) -> List[City24Listing]:
        page, limit = 1, 1000
        results: List[City24Listing] = []

        while True:
            print(f"Fetching page {page}, limit={limit}")
            response_json = self.fetch_data_as_json(limit=limit, page=page)
            listings = self.parse_listings(response_json)
            results.extend(listings)
            print(f"Parsed {len(listings)} total listings for page {page}")

            if len(listings) < limit:
                break
            page += 1
        return results

    def fetch_data_as_json(self, limit, page):
        url = CITY24_API_SEARCH_URL.format(limit=limit, page=page)
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,de;q=0.8,ru;q=0.7,et;q=0.6,zh-CN;q=0.5,zh;q=0.4,ko;q=0.3,lv;q=0.2,it;q=0.1,uk;q=0.1',
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            'referer': 'https://www.city24.ee/',
            'origin': 'https://www.city24.ee',
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def parse_listings(self, apartments) -> List[City24Listing]:
        results = []

        for apartment in apartments:
            listing = self.parse_listing(apartment)
            results.append(listing)
        return results

    def parse_listing(self, apartment):
        obj_id = apartment.get('friendly_id')
        link = f"{CITY24_BASE_URL}/real-estate/skip/skip/{obj_id}"
        address = self.build_address(apartment['address']) if apartment.get('address') else None
        address_components = self.parse_address_components(address)

        price = int(float(apartment.get('price'))) if apartment.get('price') else None
        price_m2 = int(apartment.get('price_per_unit')) if apartment.get('price_per_unit') else None
        img_url = apartment['main_image']['url'].replace('{fmt:em}', '24') \
            if apartment.get('main_image') and apartment['main_image'].get('url') else None

        slogans = apartment.get('slogans')
        object_important_note = slogans['ru_RU'].get('slogan') if slogans and slogans.get('ru_RU') else None
        object_important_note = slogans['et_EE'].get('slogan') if not object_important_note and slogans and slogans.get('et_EE') else None

        attributes = apartment.get('attributes', {})
        floor = int(attributes.get('FLOOR')) if attributes.get('FLOOR') else None
        total_floors = int(attributes.get('TOTAL_FLOORS')) if attributes.get('TOTAL_FLOORS') else None

        listing = City24Listing(
            id=obj_id,
            address=address,
            city=address_components.city,
            street_with_building=address_components.street_with_building,
            apartment_number=address_components.apartment_number,
            rooms=apartment.get('room_count'),
            area_m2=apartment.get('property_size'),
            price=price,
            price_m2=price_m2,
            link=link,
            img_url=img_url,
            object_important_note=object_important_note,
            date_published=apartment.get('date_published'),
            floor=floor,
            total_floors=total_floors,
            year_built=apartment.get('year_built'),
            latitude=apartment.get('latitude'),
            longitude=apartment.get('longitude'),
        )
        # print(listing)
        return listing

    def parse_address_components(self, address: Optional[str]) -> AddressComponents:
        """Parse address into street_with_building, apartment_number, and city."""
        if not address:
            return AddressComponents(None, None, None)

        # Examples:
        # "Tallinn, Lasnamäe linnaosa, Punane tn-15"
        # "Tallinn, Põhja-Tallinna linnaosa, Kalaranna tn-8/8"
        # "Tallinn, Kesklinna linnaosa, Pirita tee-26b/4"
        # "Tallinn, Põhja-Tallinna linnaosa, Uus-Maleva tn-3"
        # "Tallinn, Kesklinna linnaosa, Tiiu tn-12/3"

        parts = [part.strip() for part in address.split(',')]
        
        if len(parts) < 2:
            return AddressComponents(None, None, None)
        
        city = parts[0]
        street_with_building = parts[-1]

        # Only normalize dashes that separate street from building number
        # Pattern: street name followed by dash and building number
        street_with_building = re.sub(r'-(\d+[A-Za-z]?(?:/\d+)?)$', r' \1', street_with_building)

        if '/' not in street_with_building:
            return AddressComponents(city, street_with_building, None)

        apartment_number = None
        # Handle cases like "Mäepealse tn 9/1" or "Pirita tee 26b/4"
        match = re.search(r'([A-Za-z0-9]+)/(\d+)$', street_with_building)
        if match:
            building_num = match.group(1)
            apartment_number = match.group(2)

            # Remove apartment number, keep building number only
            street_with_building = street_with_building.replace(f'/{apartment_number}', '')

        return AddressComponents(city, street_with_building, apartment_number)

    def build_address(self, address: dict):
        city = address.get("parish_name", "")
        district = address.get("city_name", "")
        street = address.get("street_name", "")
        house = address.get("house_number", "")
        return f"{city}, {district}, {street}-{house}".strip(", ")
