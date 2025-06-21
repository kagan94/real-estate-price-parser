from dataclasses import dataclass
from typing import List, Optional

import requests

from .common import ListingBase
from .config import KINNISVARA24_API_SEARCH_URL


@dataclass
class Kinnisvara24Listing(ListingBase):
    year_built: Optional[str]
    main_img_url: Optional[str]
    description: Optional[str]
    created_at: Optional[str]


class Kinnisvara24Parser:
    def fetch_data(self, page):
        url = KINNISVARA24_API_SEARCH_URL
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        payload = {
            "deal_types": ["sale"],
            "object_types": ["apartment"],
            "addresses": [{"A1": "Harju maakond", "A2": "Tallinn"}],
            "sort_by": "created_at",
            "sort_order": "desc",
            "page": page
        }
        response = requests.post(url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def parse_listings(self, apartments) -> List[Kinnisvara24Listing]:
        results = []

        for apartment in apartments:
            obj_id = apartment.get('id')
            link = apartment.get('permalink')
            address = apartment['address']['address'] if apartment.get('address') else None
            price = apartment.get('hind')
            price_m2 = apartment.get('price_per_m2')
            area_m2 = apartment.get('area')
            main_img_url = apartment['images'][0].get('url') \
                if apartment.get('images') and len(apartment['images']) > 0 else None
            rooms = apartment.get('rooms')
            created_at = apartment.get('created_at')

            results.append(Kinnisvara24Listing(
                id=obj_id,
                address=address,
                rooms=rooms,
                area_m2=area_m2,
                price=price,
                price_m2=price_m2,
                link=link,
                main_img_url=main_img_url,
                year_built=None,
                description=None,
                created_at=created_at,
            ))
        return results

    def parse(self) -> List[Kinnisvara24Listing]:
        page = 1
        response_json = self.fetch_data(page)
        return self.parse_listings(response_json['data'])
