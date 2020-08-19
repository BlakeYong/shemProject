from starlette.responses import Response
from pydantic import BaseModel
from starlette.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.service.Transcribe import transcribe
from src.service.Polly import polly
from src import manageAI, manageDirection
from pydantic import BaseModel
from fastapi import FastAPI, File, Header, Form, APIRouter
from shem_configs import Config
import requests
import xml.etree.ElementTree as ET

router = APIRouter()
AIstore = manageAI
Direction = manageDirection

@router.post("/transcribe")
def exportVoiceToText(response: Response, file: bytes = File(...), filename: str = Form(...), apptoken: str = Form(...)):
    if filename.split('.')[-1] in ['mp4','mp3','wav','flac']:
        response.status_code, result = transcribe.Transcribe().transcribe(file, filename, apptoken)
        return result
    else:
        response.status_code = HTTP_422_UNPROCESSABLE_ENTITY
        return response.status_code, {
            "statusCode": 422,
            "error": "Invaild File type",
            "message": "허용되지 않는 파일 확장자입니다."
        }

class PollyObject(BaseModel):
    language : str = "Korean"
    text : str
    apptoken : str

@router.post("/predict/polly/")
async def exportTextToVoice(response: Response, pollyObject : PollyObject):
    response.status_code, result = polly.Polly().polly(pollyObject.text, pollyObject.language, pollyObject.apptoken)
    return result

@router.post("/preidct/face/")
def faceDetect(response: Response, file : bytes = File(...), filename : str = Form(...), token: str = Form(...)):
    response.status_code, result = AIstore.AiStore().DetectFace(file, filename, token)
    return result

class PointObject(BaseModel):
    origin : str
    destination : str

@router.post("/directions")
def directions(response: Response,pointObject : PointObject):
    result = Direction.ManageDirection().find_direction(pointObject.origin,pointObject.destination)
    return result
    
