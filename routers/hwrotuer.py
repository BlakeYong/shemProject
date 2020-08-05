from starlette.responses import Response
from src import hardware
from pydantic import BaseModel
from fastapi import Form, APIRouter, HTTPException, Depends
from models.helper import Helper

dbClass = Helper()
router = APIRouter()
Hardware = hardware

async def checkToken(token: str = Form(...)):
    try:
        user = dbClass.getUser(token)
    except:
        raise HTTPException(status_code=503, detail="허용되지 않은 토큰 값입니다.")


class DigitalObject(BaseModel):
    hardwareId : str
    status : bool

@router.post("/digital/")
def digitalPin(response: Response, digitalObject : DigitalObject):
    response.status_code, result = Hardware.Hardware().digital(digitalObject.hardwareId, digitalObject.status)
    return result

class AnalogObject(BaseModel):
    value : float

@router.post("/analog/")
def analogPin(response: Response, analogObject : AnalogObject):
    response.status_code, result = Hardware.Hardware().analog(analogObject.value)
    return result

@router.post("/registerparents/", dependencies=[Depends(checkToken)])
def registerParentsHw(response: Response, hardwareName : str = Form(...), token : str = Form(...)):

    response.status_code, result = Hardware.Hardware().registerParents(hardwareName, token)

    return result
