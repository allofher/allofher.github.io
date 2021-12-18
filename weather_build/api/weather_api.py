import fastapi
from fastapi import Depends
from typing import Optional, List
from models.location import Location
from models.validation_error import ValidationError
from models.reports import ReportSubmittal, Report
from services import openweather, report_service

router = fastapi.APIRouter()


@router.get('/api/weather/{city}')
async def weather(loc: Location = Depends(), units: Optional[str] = 'metric'):
    try:
        return await openweather.get_current_weather(loc.city, loc.province, loc.country, units)
    except ValidationError as ve:
        return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
    except Exception as x:
        return fastapi.Response(content=str(x), status_code=500)


@router.get('/api/reports', name='all_reports')
async def reports_get() -> List[Report]:
    return await report_service.get_reports()


@router.post('/api/reports', name='add_reports', status_code=201)
async def reports_post(report_submittal: ReportSubmittal) -> Report:
    d = report_submittal.description
    loc = report_submittal.location
    return await report_service.add_report(d, loc)
