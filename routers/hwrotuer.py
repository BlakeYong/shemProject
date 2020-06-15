from starlette.responses import Response
from pydantic import BaseModel
from starlette.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.service.Transcribe import transcribe
from src.service.Polly import polly
from src import hardware
from pydantic import BaseModel
from fastapi import FastAPI, File, Header, Form, APIRouter

router = APIRouter()
Hardware = hardware


class DigitalObject(BaseModel):
    hardwareId : str
    status : bool

@router.post("/digital/")
def digitalPin(response: Response, digitalObject : DigitalObject):
    response.code, result = Hardware.Hardware().digital(digitalObject.hardwareId, digitalObject.status)
    return response.code, result