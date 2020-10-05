from starlette.responses import Response
from fastapi import APIRouter
from typing import List
router = APIRouter()

class HouseInfo():
    users : List[int]
    

@router.post("/house")
def create_house(response:Response, houseInfo:HouseInfo)
