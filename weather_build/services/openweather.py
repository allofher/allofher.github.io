import httpx
from httpx import Response
from typing import Optional, Tuple
from infrastructure import weather_cache
from models.validation_error import ValidationError

api_key: Optional[str] = None


async def get_current_weather(city: str, province: Optional[str], country: str, units: str) -> dict:
    city, province, country, units = validate_units(city, province, country, units)

    forecast = weather_cache.get_weather(city, province, country, units)
    if forecast:
        return forecast

    if province:
        q = f'{city},{province},{country}'
    else:
        q = f'{city},{country}'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={api_key}&units={units}'

    async with httpx.AsyncClient() as client:
        resp: Response = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()
    current_weather = data['main']

    weather_cache.set_weather(city, province, country, units, current_weather)
    return current_weather


def validate_units(city: str, province: Optional[str], country: Optional[str], units: str) -> \
        Tuple[str, Optional[str], str, str]:

    city = city.lower().strip()
    if not country:
        country = "ca"
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as US or GB."
        raise ValidationError(status_code=400, error_msg=error)

    if province:
        province = province.strip().lower()

    if province and len(province) != 2:
        error = f"Invalid province: {province}. It must be a two letter abbreviation such as CA or KS (use for US only)."
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units = units.strip().lower()

    valid_units = {'standard', 'metric', 'imperial'}
    if units not in valid_units:
        error = f"Invalid units '{units}', it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, province, country, units
