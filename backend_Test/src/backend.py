# -*- coding: utf-8 -*-

import json
import os
import time
import traceback
import requests
from models.helper import Helper

class Backend:

    def __init__(self, config="Dev"):
        # self.dbClass = Helper(init=True)
        self.server = config
        if config == "Local":
            self.backEndURL = 'http://0.0.0.0:2052/'
            self.directBackEndURL = ''
        elif config == "Prod":
            self.directBackEndURL = ''
            self.backEndURL = ''
            # self.backEndURL = 'http://loadv1-359056607.ap-northeast-2.elb.amazonaws.com/'

    def login(self, id, password) :
        datas = {
            "identifier" : id,
            "password" : password
        }

        req = requests.post(self.backEndURL + 'login/', data=json.dumps(datas))
        time.sleep(0.1)
        return req.status_code, json.loads(req.text)