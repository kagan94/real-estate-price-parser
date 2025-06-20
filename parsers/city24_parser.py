from dataclasses import dataclass
from typing import List, Optional


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
    def parse(self) -> List[City24Listing]:
        # TODO: Implement actual parsing logic
        return []
