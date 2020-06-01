import json
import sys
import time
import traceback
import os
import requests

from backend_Test.src.backend import Backend

class BackendTest():

    def __init__(self):

        config = sys.argv[1]

        self.bk = Backend(config=config)


        if config == "Dev" or config == "Local":
            print("dev, local 시 테스트 로그인")
        elif config == "Prod":
            print("운영서버시 테스트 로그")

        self.testGroupName = f"{config}_" + str(time.time())
        self.serverName = f"{config}_"
        self.email = 'testUnittest2@test.com'
        self.password = 'Test12345!'
        self.userEmail = "unitest@naver.com"
        self.testGroupName = f"{config}_" + str(time.time())
        self.serverName = f"{config}_"
        self.testNum = 0
        self.totalTestNum = 1
        self.successCount = 0
        self.failTestNames = []
        self.baseResult = {
            "testGroupName": self.testGroupName,
            "serverName": self.serverName,
        }

    def start(self):

        self.test_login()
        self.tearDown()

    def tearDown(self):
        print(f"총 {str(self.totalTestNum)}개 테스트 중 {str(self.successCount)}개 성공")
        print(f"실패 테스트 목록 : {str(self.failTestNames)}")

        # try:
        #     self.bk.deleteUser(self.masterHeader, self.userId)        #나중에 데이터 지우는 부분
        # except:
        #     pass

    def sendUnittestResultFail(self, testName, errorMessage):
        self.failTestNames.append(testName)
        print({
            **self.baseResult,
            "testName": testName,
            "isFail": 1,
        })
        print(errorMessage)
        self.sendSlackMessage(f"({str(self.testNum + 1)}/{str(self.totalTestNum)}){testName} 실패 :heavy_exclamation_mark:")
        self.sendSlackMessage(str(errorMessage))
        self.bk.sendUnittestResult(self.masterHeader, {
            **self.baseResult,
            "testName": testName,
            "isFail": 1,
            "errorMessage": str(errorMessage),
        })

    def sendUnittestResultFail(self, testName, errorMessage):
        self.failTestNames.append(testName)
        print({
            **self.baseResult,
            "testName": testName,
            "isFail": 1,
        })
        print(errorMessage)
        self.testNum
        self.totalTestNum

    def sendUnittestResultSuccess(self, testName):
        print(testName + " 성공")
        self.successCount += 1
        self.testNum
        self.totalTestNum

    def testDecorator(func):
        def decorated(self):
            functionName = func.__name__
            try:
                func(self)
                self.sendUnittestResultSuccess(functionName)
            except:
                self.sendUnittestResultFail(functionName, traceback.format_exc())
                pass

        return decorated

    @testDecorator
    def test_login(self):

        code, result = self.bk.login(self.userEmail, self.password)

        result = json.dumps(result)

        assert (code == 200), 'login - Response Code: '+str(code)

if __name__=='__main__':

    BackendTest().start()