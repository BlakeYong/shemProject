from starlette.responses import FileResponse, StreamingResponse, JSONResponse
from models.helper import Helper
from src.util import Util
import ast
import traceback
import time
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
import os, io
import urllib
import urllib.request
import json
import sys
from boto3 import client
from shem_configs import shem_configs

class Polly:
    def __init__(self):
        self.dbClass = Helper()

    def polly(self, Text, language, appToken):
        languages = {
            "English" : "Salli",
            "Korean" : "Seoyeon",
            "Japanese" : "Mizuki"
        }

        # try:
        #     user = self.dbClass.getUser(appToken)
        #     userId = self.utilClass.getStrUserId(user)
        # except:
        #     return HTTP_503_SERVICE_UNAVAILABLE, {
        #         "statusCode": 503,
        #         "error": "Bad Request",
        #         "message": "허용되지 않은 토큰 값입니다."
        #     }

        if language not in languages:
            return HTTP_503_SERVICE_UNAVAILABLE, {
                "statusCode": 503,
                "error": "Bad Request",
                "message": "지원하지 않는 언어코드입니다."
            }

        Polly = client("polly", aws_access_key_id=shem_configs['aws_access_key_id'],
                        aws_secret_access_key=shem_configs['aws_secret_access_key'],
                                     region_name="ap-northeast-2")

        try:
            response = Polly.synthesize_speech(
                    Text=Text,
                    OutputFormat="mp3", VoiceId=languages[language])

            stream = response.get("AudioStream")

            with open('test1.mp3', 'wb') as f:
                data = stream.read()
                f.write(data)
            return HTTP_201_CREATED, {
                "statusCode": 201,
                "error": "Bad Request",
                "message": "변환이 완료되었습니다."
            }
        except:
            print(traceback.format_exc())
            return HTTP_500_INTERNAL_SERVER_ERROR, {
                "statusCode": 500,
                "error": "Bad Request",
                "message": "잘못된 접근입니다."
            }
            pass