from dataclasses import dataclass
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from .config import KVEE_BASE_URL, KVEE_SEARCH_URL


@dataclass
class KvEeListing:
    id: str
    address: Optional[str]
    rooms: Optional[str]
    area_m2: Optional[str]
    price: Optional[str]
    price_m2: Optional[str]
    link: Optional[str]
    first_img_url: Optional[str]
    description: Optional[str]


class KvEeParser:
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
        return response.json().get('content')

    def extract_img_url(self, img_el):
        if not img_el:
            return None
        if img_el.get("data-src"):
            return img_el.get("data-src")
        return img_el.get("src")

    def parse_listings(self, html: str) -> List[KvEeListing]:
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', attrs={'data-object-id': True})
        results = []

        for art in articles:
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

            price_tag = art.find("div", attrs={"data-price": True})
            price = price_tag['data-price'] if price_tag else None

            first_img = art.select_one("div.images img")
            first_img_url = self.extract_img_url(first_img)

            area_div = art.find('div', class_='area')
            area_m2 = area_div.get_text(strip=True).replace('\u00a0m\u00b2', '') if area_div else None
            price_m2 = int(float(price) / float(area_m2)) if price and area_m2 else None

            desc_p = art.find('p', class_='object-excerpt')
            description = desc_p.get_text(strip=True) if desc_p else None

            rooms_div = art.find('div', class_='rooms')
            rooms = rooms_div.get_text(strip=True) if rooms_div else None

            results.append(KvEeListing(
                id=obj_id,
                address=address,
                rooms=rooms,
                area_m2=area_m2,
                price=price,
                price_m2=str(price_m2) if price_m2 is not None else None,
                link=link,
                first_img_url=first_img_url,
                description=description,
            ))
        return results

    def parse(self) -> List[KvEeListing]:
        offset = 0
        html = self.fetch_page(offset)
        return self.parse_listings(html)
