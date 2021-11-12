import fastapi
from fastapi import Depends
from typing import Optional
from models.location import Location
from services import openweather

router = fastapi.APIRouter()

@router.get('/api/weather/{city}')
def weather(loc: Location = Depends(),
            units: Optional[str] = 'metric'):
    report = openweather.get_current_weather(loc.city, loc.province, loc.country, units)
    return report