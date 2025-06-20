from dataclasses import dataclass
from typing import List, Optional


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
    def parse(self) -> List[KvEeListing]:
        # TODO: Implement actual parsing logic
        return []
