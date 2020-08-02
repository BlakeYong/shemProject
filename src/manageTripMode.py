from models import houseTable
from src.util import Util
from starlette.status import HTTP_200_OK
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_404_NOT_FOUND

class ManageTripMode:

    # __init__ 에는 에러, db 설정 해줌
    def __init__(self):
        Util.createTables(houseTable)

    # db에 tripmode 설정을 해줌
    # id, tripFrom, tripTo 받아줘서 db 에 접근
    def setTripMode(self, tripModeInfoRaw):
        tripModeInfo = tripModeInfoRaw.__dict__

        if not houseTable.select().where(houseTable.id == tripModeInfo['houseId']):
            message = {
                "statusCode" : 404,
                "error" : "Doesn't Exist",
                "message" : "존재하지 않는 houseId 입니다."
            }
            return HTTP_404_NOT_FOUND, message

        

        try:
            result = houseTable.update({
                houseTable.isTrip : tripModeInfo['isTrip'],
                houseTable.tripFrom : tripModeInfo['tripFrom'],
                houseTable.tripTo : tripModeInfo['tripTo']
            }).where(houseTable.id == tripModeInfo['houseId']).execute()
        except e:
            message = {
                "statusCode" : 500,
                "error" : "Internal server error",
                "message" : "예기치 못한 오류가 발생했습니다"
            }
            return HTTP_500_INTERNAL_SERVER_ERROR ,message
            
        return HTTP_200_OK, result