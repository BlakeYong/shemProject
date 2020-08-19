import traceback
import bcrypt
import re
import uuid
import datetime
import jwt

from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_301_MOVED_PERMANENTLY
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_403_FORBIDDEN
from starlette.status import HTTP_423_LOCKED
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_507_INSUFFICIENT_STORAGE
from src.utils.util import Util
from models.helper import Helper
import requests
import json

class Hardware:
    def __init__(self):
        self.dbClass = Helper()
        self.utilClass = Util()

    def digital(self, hardware, status):
        return HTTP_200_OK ,not status

    def analog(self, value):
        test = {"value" : value}
        self.dbClass.analogTestInput(value)
        return HTTP_200_OK, {'result' : value}

    def analogTest(self):
        data = {
            "value" : 52.789
        }

        req = requests.post("http://52.78.65.114/analog/", data=json.dumps(data))

        return req.status_code, req.text

    def registerParents(self, hardwareName, token):

        try:
            user = self.dbClass.getUser(token, False)

            hardwareInfo = {'hardwareName': hardwareName, 'userId' : user['id'], 'childrenId' : []}

            self.dbClass.createParentsHardware(hardwareInfo)
        except:
            self.utilClass.send_message(
                f'부모 하드웨어 등록 중 에러\n=============================================\n{traceback.format_exc()}\n=============================================',
                "error")
            pass

        self.utilClass.send_message(f'부모 하드웨어 등록 정보\n=============================================\n{hardwareInfo}\n=============================================',"log")
        return HTTP_201_CREATED, hardwareInfo

    def registerChildren(self, hardwareName, parentsId, token):

        try:
            self.dbClass.getParentsHardwareById(parentsId)
        except:
            self.utilClass.send_message(
                f'자식 하드웨어 등록 중 에러\n=============================================\ndetail:부모 하드웨어 정보가 없습니다. | parentsId : {parentsId}\n=============================================',
                "error")
            return HTTP_404_NOT_FOUND, {'detail':'하드웨어 정보가 없습니다.'}

        try:
            user = self.dbClass.getUser(token, False)

            hardwareInfo = {'hardwareName': hardwareName, 'userId': user['id'], 'parentsHardwareId' : parentsId}

            self.dbClass.createChildrenHardware(hardwareInfo)
        except:
            self.utilClass.send_message(
                f'자식 하드웨어 등록 중 에러\n=============================================\n{traceback.format_exc()}\n=============================================',
                "error")

        self.utilClass.send_message(
            f'자식 하드웨어 등록 정보\n=============================================\n{hardwareInfo}\n=============================================',
            "log")

        return HTTP_201_CREATED, hardwareInfo