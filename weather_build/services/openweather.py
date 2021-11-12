from typing import Optional

def get_current_weather(city: str, state: Optional[str], country: str, units: str) -> dict:
    q = f'{city},{state},{country}'
    key = 123
    url=f'https://api.openweathermap.org/data/2.5/weather?q={q}&appid={key}&units={units}'