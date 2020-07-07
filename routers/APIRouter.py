from starlette.responses import Response
from pydantic import BaseModel
from starlette.responses import Response
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from src.service.Transcribe import transcribe
from src.service.Polly import polly
#from src import manageAI
from pydantic import BaseModel
from fastapi import FastAPI, File, Header, Form, APIRouter
from shem_configs import shem_configs
import requests
import xml.etree.ElementTree as ET

router = APIRouter()
#AIstore = manageAI

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

class Location(BaseModel):
    x : float
    y : float

@router.post("/busapi/station")
async def nearbyStation(location : Location):
    url = "{0}?serviceKey={1}&x={2}&y={3}&".format(shem_configs["bus_url"],shem_configs["bus_key"],location.x,location.y)
    r = requests.get(url)
    root = ET.fromstring(r.text)
    idx  = []
    name =[]

    for stationId in root.iter('stationId'):
        idx.append(stationId.text)
    for stationName in root.iter('stationName'):
        name.append(stationName.text)

    result = {"idx":idx,"name":name}
    return result

