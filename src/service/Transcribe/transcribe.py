from starlette.responses import FileResponse, StreamingResponse, JSONResponse
# from fastai.vision import *
import random
from models.helper import Helper
from src.utils.util import Util
import ast
import traceback
import time
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.status import HTTP_201_CREATED
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
import os, io
import boto3
import urllib
import urllib.request
import json
from shem_configs import Config


class Transcribe:

    def __init__(self):
        self.dbClass = Helper(init=True)
        self.utilClass = Util()

    def transcribe(self, file, filename, token):
        # try:
        #     user = self.dbClass.getUser(token)
        #     userId = self.utilClass.getStrUserId(user)
        # except:
        #     return HTTP_503_SERVICE_UNAVAILABLE, {
        #         "statusCode": 503,
        #         "error": "Bad Request",
        #         "message": "허용되지 않은 토큰 값입니다."
        #     }  => 차후 유저 인증부분 구현

        s3 = boto3.client('s3', aws_access_key_id=Config['aws_access_key_id'], aws_secret_access_key=Config['aws_secret_access_key'], region_name='ap-southeast-1')
        s3.upload_file(f'temp/{filename}', 'assetdslab' , f'transcribe/{filename}')
        job_uri = f'https://assetdslab.s3.ap-northeast-1.amazonaws.com/transcribe/{filename}'

        Transcribe = boto3.client('transcribe', aws_access_key_id=Config['aws_access_key_id'], aws_secret_access_key=Config['aws_secret_access_key'], region_name='ap-southeast-1')

        try:
            try:
                job_name = token + str(random.randint(0, 1000))
                Transcribe.start_transcription_job(TranscriptionJobName=job_name, Media={'MediaFileUri': job_uri}, MediaFormat=filename.split('.')[-1], LanguageCode='ko-KR') #ko-KR   en-US
            except:
                print(traceback.format_exc())
                Util.send_message(traceback.format_exc())
                try:
                    Transcribe.delete_transcription_job(TranscriptionJobName=job_name)
                except:
                    pass
                return HTTP_503_SERVICE_UNAVAILABLE, {}
                pass

            while True:
                status = Transcribe.get_transcription_job(TranscriptionJobName=job_name)
                if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                    break
                time.sleep(1)
            if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
                response = urllib.request.urlopen(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                data = json.loads(response.read())
                text = data['results']['transcripts'][0]['transcript']
                Transcribe.delete_transcription_job(TranscriptionJobName=job_name)
            return HTTP_200_OK, {"transcrible-text":text}
        except:
            Transcribe.delete_transcription_job(TranscriptionJobName=job_name)
            print(traceback.format_exc())
            Util.error_message(traceback.format_exc())
            return HTTP_500_INTERNAL_SERVER_ERROR, {
                "statusCode": 500,
                "error": "Bad Request",
                "message": "잘못된 접근입니다."
            }
            pass


