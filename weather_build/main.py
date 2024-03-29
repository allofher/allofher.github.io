import json
import fastapi
import uvicorn
from starlette.staticfiles import StaticFiles
from pathlib import Path
from api import weather_api
from views import home
from services import openweather

api = fastapi.FastAPI()

def configure():
    configure_routing()
    configure_api_keys()

def configure_api_keys():
    file = Path('settings.json').absolute()

    if not file.exists():
        print("no settings file")
        raise Exception("no settings file")

    with open('settings.json') as fin:
        settings = json.load(fin)
        openweather.api_key = settings.get('api_key')

def configure_routing():
    api.mount('/static', StaticFiles(directory='static'), name='static')
    api.include_router(home.router)
    api.include_router(weather_api.router)

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()