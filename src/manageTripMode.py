from models import HouseTable
from src.util import Util
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_404_NOT_FOUND
from models.helper import *
from fastapi import WebSocket
import typing
from .ConnectionManager import ConnectionManager
class ManageTripMode:

    # __init__ 에는 에러, db 설정 해줌
    def __init__(self):
        self.dbclass = Helper()
        Util.createTables(HouseTable)

    # db에 tripmode 설정을 해줌
    # id, tripFrom, tripTo 받아줘서 db 에 접근
    def setTripMode(self, tripModeInfoRaw):
        tripModeInfo = tripModeInfoRaw.__dict__
        houseInfo = self.dbclass.getHouse(tripModeInfo['houseId'])
        
        if not houseInfo:
            message = {
                "statusCode" : 404,
                "error" : "Doesn't Exist",
                "message" : "존재하지 않는 houseId 입니다."
            }
            return HTTP_404_NOT_FOUND, message
        
        try:
            data = {
                'isTrip' : tripModeInfo['isTrip'],
                'tripFrom' : tripModeInfo['tripFrom'],
                'tripTo' : tripModeInfo['tripTo']
            }
            result = self.dbclass.updateHouse(tripModeInfo['houseId'],data)
        except Exception as e:
            message = {
                "statusCode" : 500,
                "error" : "Internal server error",
                "message" : "예기치 못한 오류가 발생했습니다"
            }
            print(e)
            return HTTP_500_INTERNAL_SERVER_ERROR ,message
        return HTTP_200_OK, result, int(tripModeInfo['houseId'])
    