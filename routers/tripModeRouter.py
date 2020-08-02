from pydantic import BaseModel
from starlette.responses import Response
from fastapi import FastAPI, File, Header, Form, APIRouter
from src import manageTripMode

router = APIRouter()

class TripModeInfo(BaseModel):
    houseId : int
    isTrip : bool
    tripFrom : str = '2018-04-04 10:00:00'
    tripTo : str = '2018-04-04 10:00:00'
    
@router.post("/house/tripmode")
def manageTripmode(response:Response, tripModeInfo : TripModeInfo):
    response.status_code, result = manageTripMode.ManageTripMode().setTripMode(tripModeInfo)
    return result