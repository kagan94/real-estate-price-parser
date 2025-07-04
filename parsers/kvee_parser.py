import re
from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from config import KVEE_BASE_URL, KVEE_SEARCH_URL
from .common import ListingBase, AddressComponents


@dataclass
class KvEeListing(ListingBase):
    object_important_note: Optional[str]
    description: Optional[str]
    date_activated: Optional[str]
    advertisement_level: Optional[int]
    floor: Optional[int]
    total_floors: Optional[int]
    year_built: Optional[int]


class KvEeParser:
    def parse(self) -> List[KvEeListing]:
        print(f"Fetching page 0 (offset=0) to determine total count...")
        first_response = self.fetch_page(start=0)

        total_items = first_response['countsOverall']
        items_per_page = len(first_response['objects'])
        total_pages = (total_items + items_per_page - 1) // items_per_page
        print(f"Total listings to fetch: {total_items}, total pages: {total_pages}, items per page: {items_per_page}")

        all_results: List[KvEeListing] = []
        all_results.extend(self.parse_listings(first_response))
        current_page = 1

        for offset in range(items_per_page, total_items, items_per_page):
            current_page += 1
            print(f"Fetching page {current_page} of {total_pages} (offset={offset})...")
            response = self.fetch_page(start=offset)
            all_results.extend(self.parse_listings(response))

        return all_results

    def fetch_page(self, start):
        url = KVEE_SEARCH_URL + str(start)
        headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9,de;q=0.8,ru;q=0.7,et;q=0.6,zh-CN;q=0.5,zh;q=0.4,ko;q=0.3,lv;q=0.2,it;q=0.1,uk;q=0.1',
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            'referer': 'https://www.kv.ee/',
            'origin': 'https://www.kv.ee',
        }
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()

    def parse_listings(self, response: dict) -> List[KvEeListing]:
        objects = response.get('objects') or []
        object_data_by_id_map = {str(data['object_id']): data for data in objects}

        html = response.get('content') or ''
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', attrs={'data-object-id': True})

        results = []
        for art in articles:
            listing = self.parse_listing(art, object_data_by_id_map)
            results.append(listing)
        return results

    def parse_listing(self, art, object_data_by_id_map: dict) -> KvEeListing:
        obj_id = art['data-object-id']
        address = None
        link = None
        h2 = art.find('h2')
        if h2:
            for a in h2.find_all('a'):
                if 'object-promoted' not in (a.get('class') or []):
                    address = a.get_text(strip=True)
                    link = a.get('href')
                    break

        if link and link.startswith('/'):
            link = KVEE_BASE_URL + link

        address_components = self.parse_address_components(address)

        price_tag = art.find("div", attrs={"data-price": True})
        price = price_tag['data-price'] if price_tag else None
        price = int(float(price)) if price else None

        first_img = art.select_one("div.images img")
        img_url = self.extract_img_url(first_img)

        area_div = art.find('div', class_='area')
        area_m2 = area_div.get_text(strip=True).replace('\u00a0m\u00b2', '') if area_div else None
        area_m2 = float(area_m2) if area_m2 else None
        price_m2 = int(float(price) / float(area_m2)) if price and area_m2 else None

        object_important_note_p = art.find('p', class_='object-important-note')
        object_important_note = object_important_note_p.get_text(strip=True) if object_important_note_p else None

        desc_p = art.find('p', class_='object-excerpt')
        description = desc_p.get_text(strip=True) if desc_p else None

        floor = self.parse_floor(description)
        total_floors = self.parse_total_floors(description)
        year_built = self.parse_year_built(description)

        rooms_div = art.find('div', class_='rooms')
        rooms = rooms_div.get_text(strip=True) if rooms_div else None
        rooms = int(rooms) if rooms else None

        extra_data = object_data_by_id_map.get(obj_id, {})
        date_activated = extra_data.get('date_activated')
        advertisement_level = extra_data.get('advertisment_level')

        return KvEeListing(
            id=obj_id,
            address=address,
            city=address_components.city,
            street_with_building=address_components.street_with_building,
            apartment_number=address_components.apartment_number,
            rooms=rooms,
            area_m2=area_m2,
            price=price,
            price_m2=price_m2,
            link=link,
            img_url=img_url,
            object_important_note=object_important_note,
            description=description,
            date_activated=date_activated,
            advertisement_level=advertisement_level,
            floor=floor,
            total_floors=total_floors,
            year_built=year_built
        )

    def parse_address_components(self, address: Optional[str]) -> AddressComponents:
        """Parse address into street_with_building, apartment_number, and city."""
        if not address:
            return AddressComponents(None, None, None)

        # Examples:
        # "Tallinn, Lasnamäe, Punane tn 21-1"
        # "Tallinn, Lasnamäe, Varraku peatus, Punane tn 65"
        # "Tallinn, Lasnamäe, Punane tn 27"

        parts = [part.strip() for part in address.split(',')]

        if len(parts) < 2:
            return AddressComponents(None, None, None)

        city = parts[0]
        street_with_building = parts[-1]

        # Handle apartment numbers with space before dash (e.g., "Punane tn 21-1")
        apartment_number = None
        # First, try dash pattern (e.g., '21-1', '26b-15')
        dash_match = re.search(r'([A-Za-z0-9]+(?:/\d+)?)\s*-(\d+)$', street_with_building)
        if dash_match:
            building_part = dash_match.group(1)
            apartment_number = dash_match.group(2)
            street_with_building = street_with_building.replace(f' {building_part}-{apartment_number}', f' {building_part}')
        else:
            # Only check for slash pattern if dash pattern did not match
            slash_match = re.search(r'([A-Za-z0-9]+)/(\d+)$', street_with_building)
            if slash_match:
                building_part = slash_match.group(1)
                apartment_number = slash_match.group(2)
                street_with_building = street_with_building.replace(f'/{apartment_number}', '')

        return AddressComponents(city, street_with_building, apartment_number)

    def extract_img_url(self, img_el):
        if not img_el:
            return None
        if img_el.get("data-src"):
            return img_el.get("data-src")
        return img_el.get("src")

    def parse_floor(self, description: Optional[str]) -> Optional[int]:
        if not description:
            return None
        floor_match = re.search(r'Этаж\s*(\d+)(?:/\d+)?', description)
        if floor_match:
            return int(floor_match.group(1))
        floor_match = re.search(r'(\d+)\.\s*этаж', description)
        if floor_match:
            return int(floor_match.group(1))
        return None

    def parse_total_floors(self, description: Optional[str]) -> Optional[int]:
        if not description:
            return None
        floor_match = re.search(r'Этаж\s*\d+/(\d+)', description)
        if floor_match:
            return int(floor_match.group(1))
        return None

    def parse_year_built(self, description: Optional[str]) -> Optional[int]:
        if not description:
            return None
        year_match = re.search(r'год постройки\s*(\d{4})', description)
        if year_match:
            return int(year_match.group(1))
        return None
