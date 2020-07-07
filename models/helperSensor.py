import datetime
import traceback
import bcrypt
import peewee

from models import *
import functools
class HelperSensor():
    def __init__(self, init=False):
        ""
        # if init:
        #     Shem.connect(reuse_if_open=True)

    def __exit__(self, exc_type, exc_value, traceback):

        if not shemdb.is_closed():
            shemdb.close()

    def wrapper(func):
        @functools.wraps(func)
        def wrap(self, *args, **kwargs):
            with shemdb.connection_context():
                return func(self, *args, **kwargs)
        return wrap

    @wrapper
    def analogTestInput(self, data):
        print("hello")
        return hardwareTable.insert(value=data).execute()