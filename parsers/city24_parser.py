from dataclasses import dataclass
from typing import List, Optional

import requests

from .config import CITY24_BASE_URL, CITY24_API_SEARCH_URL


@dataclass
class City24Listing:
    id: str
    address: Optional[str]
    rooms: Optional[str]
    area_m2: Optional[str]
    year_built: Optional[str]
    price: Optional[int]
    price_m2: Optional[int]
    link: Optional[str]
    main_img_url: Optional[str]
    description: Optional[str]

class City24Parser:
    def fetch_data(self, page):
        url = CITY24_API_SEARCH_URL + str(page)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def build_address(self, address: dict):
        city = address.get("parish_name", "")
        district = address.get("city_name", "")
        street = address.get("street_name", "")
        house = address.get("house_number", "")
        return f"{city}, {district}, {street}-{house}".strip(", ")

    def parse_listings(self, apartments) -> List[City24Listing]:
        results = []

        for apartment in apartments:
            obj_id = apartment.get('friendly_id')
            link = f"{CITY24_BASE_URL}/real-estate/skip/skip/{obj_id}"
            address = self.build_address(apartment['address']) if apartment.get('address') else None
            price = int(apartment.get('price').replace('.00', '')) if apartment.get('price') else None
            price_m2 = int(apartment.get('price_per_unit')) if apartment.get('price_per_unit') else None
            area_m2 = apartment.get('property_size')
            main_img_url = apartment['main_image']['url'].replace('{fmt:em}', '24') if apartment.get('main_image') and apartment['main_image'].get('url') else None
            rooms = apartment.get('room_count')
            year_built = apartment.get('year_built')
            slogans = apartment.get('slogans')
            description = slogans['et_EE'].get('slogan') if slogans and slogans.get('et_EE') else None

            results.append(City24Listing(
                id=obj_id,
                address=address,
                rooms=rooms,
                area_m2=area_m2,
                price=price,
                price_m2=price_m2,
                link=link,
                main_img_url=main_img_url,
                year_built=year_built,
                description=description,
            ))
        return results

    def parse(self) -> List[City24Listing]:
        page = 1
        response_json = self.fetch_data(page)
        return self.parse_listings(response_json)
