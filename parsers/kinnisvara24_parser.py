from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Kinnisvara24Listing:
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
    created_at: Optional[str]


class Kinnisvara24Parser:
    def parse(self) -> List[Kinnisvara24Listing]:
        # TODO: Implement actual parsing logic
        return []
