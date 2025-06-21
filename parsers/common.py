from dataclasses import dataclass
from typing import Optional


@dataclass
class AddressComponents:
    city: Optional[str]
    street_with_building: Optional[str]
    apartment_number: Optional[str]


@dataclass
class ListingBase:
    id: str
    address: Optional[str]
    city: Optional[str]
    street_with_building: Optional[str]
    apartment_number: Optional[str]
    rooms: Optional[int]
    area_m2: Optional[float]
    price: Optional[int]
    price_m2: Optional[int]
    link: Optional[str]
    img_url: Optional[str]
