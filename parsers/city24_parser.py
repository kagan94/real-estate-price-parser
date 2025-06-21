from dataclasses import dataclass
from typing import List, Optional

import requests

from config import CITY24_BASE_URL, CITY24_API_SEARCH_URL
from .common import ListingBase


@dataclass
class City24Listing(ListingBase):
    main_img_url: Optional[str]
    object_important_note: Optional[str]
    description: Optional[str]
    date_published: Optional[str]
    floor: Optional[str]
    total_floors: Optional[str]
    year_built: Optional[str]

class City24Parser:
    def parse(self) -> List[City24Listing]:
        response_json = self.fetch_data(limit=10, page=1)
        return self.parse_listings(response_json)

    def fetch_data(self, limit, page):
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
        price = int(apartment.get('price').replace('.00', '')) if apartment.get('price') else None
        price_m2 = int(apartment.get('price_per_unit')) if apartment.get('price_per_unit') else None
        area_m2 = apartment.get('property_size')
        main_img_url = apartment['main_image']['url'].replace('{fmt:em}', '24') \
            if apartment.get('main_image') and apartment['main_image'].get('url') else None
        rooms = apartment.get('room_count')
        year_built = apartment.get('year_built')
        date_published = apartment.get('date_published')

        attributes = apartment.get('attributes', {})
        floor = attributes.get('FLOOR')
        total_floors = attributes.get('TOTAL_FLOORS')

        slogans = apartment.get('slogans')
        object_important_note = slogans['ru_RU'].get('slogan') if slogans and slogans.get('ru_RU') else None
        object_important_note = slogans['et_EE'].get('slogan') if not object_important_note and slogans and slogans.get('et_EE') else None

        listing = City24Listing(
            id=obj_id,
            address=address,
            rooms=rooms,
            area_m2=area_m2,
            price=price,
            price_m2=price_m2,
            link=link,
            main_img_url=main_img_url,
            year_built=year_built,
            object_important_note=object_important_note,
            description=None,
            date_published=date_published,
            floor=floor,
            total_floors=total_floors,
        )
        print(listing)
        return listing

    def build_address(self, address: dict):
        city = address.get("parish_name", "")
        district = address.get("city_name", "")
        street = address.get("street_name", "")
        house = address.get("house_number", "")
        return f"{city}, {district}, {street}-{house}".strip(", ")
