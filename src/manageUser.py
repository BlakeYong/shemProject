import traceback
import bcrypt
import re
import uuid
import datetime
import jwt
import peewee
import pymysql


from starlette.status import HTTP_200_OK
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_301_MOVED_PERMANENTLY
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_403_FORBIDDEN
from starlette.status import HTTP_423_LOCKED
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_507_INSUFFICIENT_STORAGE
from models.helper import *

from src.util import Util

class ManageUser:
    def __init__(self):
        
        self.dbClass = Helper()
        self.invaildUserAuthResponse = {
            "statusCode": 500,
            "error": "Bad Request",
            "message": "잘못된 접근입니다."
        }
        self.failUserAuthResponse = {
            "statusCode": 500,
            "error": "Bad Request",
            "message": "유저 정보를 찾을 수 없습니다."
        }
        self.dbClass = Helper()

    def registerUser(self, userInfoRaw):
        userInfo = userInfoRaw.__dict__
        salt = bcrypt.gensalt(10)

        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', userInfo["password"]):
            return HTTP_500_INTERNAL_SERVER_ERROR, {
                "statusCode": 500,
                "error": "Bad Request",
                "message": "비밀번호가 양식에 맞지 않습니다. 다시 시도하여 주시길 바랍니다."
            }
 
        if len(re.findall("[a-z]", userInfo["password"])) == 0 or len(re.findall("[0-9]", userInfo["password"])) == 0 or len(re.findall("[!@#$%^&+=]",userInfo["password"])) == 0:
            return HTTP_500_INTERNAL_SERVER_ERROR, {
                "statusCode": 500,
                "error": "Bad Request",
                "message": "영어, 숫자, 특수기호가 최소 1개이상 포함되어야 합니다."
            }

        userInfo["password"] = bcrypt.hashpw(
            userInfo["password"].encode(), salt)
        try:
            userInfoRaw = self.dbClass.createUser(userInfo)  # 나중에 db 구축 이후
            userInfo = userInfoRaw.__dict__['__data__']  # db 구축후 불러오면 딕셔너리로 변환하기
        except:
            print(traceback.format_exc())
            return HTTP_400_BAD_REQUEST, {
                "statusCode": 400,
                "error": "Bad Request",
                "message" : "DB 설정 오류 또는 이미 가입된 이메일 입니다"
                #"message": "이미 가입된 이메일입니다."
            }
            pass
        utilClass.send_message()
        return HTTP_201_CREATED, userInfo

    def loginUser(self, userLoginInfo):

        userInfo = {}
        try:
            userInfo['user'] = self.dbClass.loginUser(
                userLoginInfo.email, userLoginInfo.password).__dict__['__data__']
        except:
            return HTTP_400_BAD_REQUEST, {
                "status_code": 400,
                "message": "비밀번호가 일치하지 않습니다."
            }
            pass

        if userInfo.get('user'):  # db에서 값 받으면

            userInfo['jwt'] = userInfo['user']["token"]
            if not userInfo['user']["token"]:
                token = jwt.encode(
                    {'email': userInfo['user']["email"]}, 'aiShemwayswinning', algorithm='HS256')
                self.dbClass.updateUser(userInfo['user']["id"], {
                    'token': token
                })
                userInfo['jwt'] = token
                userInfo['user']["token"] = token

            # if userInfo['user']['confirmed'] and not userInfo['user']['isDeleteRequested']:
            #     return HTTP_200_OK, userInfo
            # elif userInfo['user']['isDeleteRequested']:
            #     return HTTP_400_BAD_REQUEST, {
            #         "status_code": 400,
            #         "message": "삭제된 회원입니다."
            #     }
            # else:
            #     return HTTP_400_BAD_REQUEST, {
            #         "status_code": 400,
            #         "message": "Email verification is not confirmed."
            #     }
            utilClass.send_message(f"로그인 유저 정보\n===============\nid : {userInfo['user']['id']} | email : {userInfo['user']['email']} | username : {userInfo['user']['username']}\n===============", "log")
        return HTTP_200_OK, userInfo


