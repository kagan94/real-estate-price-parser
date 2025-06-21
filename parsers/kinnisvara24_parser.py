from dataclasses import dataclass
from typing import List, Optional

import requests

from config import KINNISVARA24_API_SEARCH_URL, KINNISVARA24_API_PAYLOAD
from .common import ListingBase


@dataclass
class Kinnisvara24Listing(ListingBase):
    created_at: Optional[str]


class Kinnisvara24Parser:
    def parse(self) -> List[Kinnisvara24Listing]:
        print(f"Fetching page 1 to determine total pages...")
        response_json = self.fetch_data(page=1)

        total_pages = response_json['meta']['last_page']
        items_per_page = len(response_json['data'])
        print(f"Total pages to fetch: {total_pages}, items per page: {items_per_page}")

        all_results: List[Kinnisvara24Listing] = []
        all_results.extend(self.parse_listings(response_json['data']))

        for page in range(2, total_pages + 1):
            print(f"Fetching page {page} of {total_pages}...")
            response_json = self.fetch_data(page=page)
            all_results.extend(self.parse_listings(response_json['data']))

        return all_results

    def fetch_data(self, page):
        url = KINNISVARA24_API_SEARCH_URL
        headers = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json"}
        payload = {
            **KINNISVARA24_API_PAYLOAD,
            "page": page
        }
        response = requests.post(url, json=payload, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def parse_listings(self, apartments) -> List[Kinnisvara24Listing]:
        results = []

        for apartment in apartments:
            listing = self.parse_listing(apartment)
            results.append(listing)
        return results

    def parse_listing(self, apartment):
        obj_id = apartment.get('id')
        link = apartment.get('permalink')
        address = self.parse_address(apartment)
        price = apartment.get('hind')
        price_m2 = apartment.get('price_per_m2')
        area_m2 = apartment.get('area')
        img_url = apartment['images'][0].get('url') \
            if apartment.get('images') and len(apartment['images']) > 0 else None
        rooms = apartment.get('rooms')
        created_at = apartment.get('created_at')

        listing = Kinnisvara24Listing(
            id=obj_id,
            address=address,
            rooms=rooms,
            area_m2=area_m2,
            price=price,
            price_m2=price_m2,
            link=link,
            img_url=img_url,
            created_at=created_at,
        )
        # print(listing)
        return listing

    def parse_address(self, apartment):
        address = apartment.get('address')
        if address['address']:
            return address['address']
        return address['short_address']
