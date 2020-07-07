from pydantic import BaseModel
from fastapi import FastAPI, File, Header, Form, APIRouter

router = APIRouter()

class HouseObject(BaseModel):
    houseId : str
    