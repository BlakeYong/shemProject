import json

import peewee as pw
import sys
from src.util import Util
from shem_configs import shem_configs
from playhouse.pool import PooledMySQLDatabase

utilClass = Util()

shemdb = pw.MySQLDatabase(shem_configs['prod_db_schema'], host=shem_configs['prod_db_host'], port=3306,
                          user=shem_configs['prod_db_user'], passwd=shem_configs['prod_db_passwd'])

class JSONField(pw.TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)

class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = shemdb

class usersTable(MySQLModel):
    class Meta:
        db_table = 'usersTable'

    id = pw.IntegerField()
    username = pw.CharField()
    email = pw.CharField()
    nickname = pw.CharField()
    password = pw.CharField()
    resetPasswordToken = pw.CharField()
    confirmed = pw.IntegerField()
    name = pw.CharField()
    resetPasswordRequestDatetime = pw.DateTimeField()
    resetPasswordVerifyLink = pw.CharField()
    resetPasswordVerifyTokenID = pw.CharField()
    emailVerifyRequestDatetime = pw.CharField()
    emailVerifyDatetime = pw.CharField()
    emailVerifyTokenID = pw.CharField()
    emailVerifyLink = pw.CharField()
    emailChangeValue = pw.CharField()
    emailChangeRequestDatetime = pw.CharField()
    created_at = pw.DateTimeField()
    updated_at = pw.DateTimeField()
    emailVerifiedYN = pw.CharField()
    emailTokenCode = pw.CharField()
    token = pw.TextField()
    gender = pw.CharField()
    birth = pw.DateField
    appTokenCode = pw.CharField()
    appTokenCodeUpdatedAt = pw.DateTimeField()
    address = pw.CharField()
    isDeleteRequested = pw.IntegerField