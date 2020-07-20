import traceback

from models import *
import functools

class HelperHouse():
    def __init__(self, init = False):
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
    def getHouse(self, house_id):
        return HouseTable.get(HouseTable.id == house_id).__dict__['__data__']
    
    @wrapper
    def updateHouse(self,house_id,data):
        return HouseTable.update(data).where(HouseTable.id == house_id).execute()
