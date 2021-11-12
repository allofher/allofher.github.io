from typing import Optional
from pydantic import BaseModel

class Location(BaseModel):
    city: str
    province: Optional[str] = None
    country: str = 'CA'