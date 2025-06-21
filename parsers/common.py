from dataclasses import dataclass
from typing import Optional


@dataclass
class ListingBase:
    id: str
    address: Optional[str]
