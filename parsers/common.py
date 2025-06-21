from dataclasses import dataclass
from typing import Optional


@dataclass
class ListingBase:
    id: str
    address: Optional[str]
    rooms: Optional[str]
    area_m2: Optional[str]
    price: Optional[int]
    price_m2: Optional[int]
    link: Optional[str]
