import traceback
import bcrypt
import re
import uuid
import datetime
import jwt

from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_301_MOVED_PERMANENTLY
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_403_FORBIDDEN
from starlette.status import HTTP_423_LOCKED
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_507_INSUFFICIENT_STORAGE
from models.helper import Helper
import requests
import json

class Hardware:
    def __init__(self):
        self.dbClass = Helper()

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


