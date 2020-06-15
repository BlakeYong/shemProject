import datetime
import traceback
import bcrypt
import peewee

from models.helperCreate import HelperCreate
from models import *
import functools

class Helper():

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
    def getUser(self, token, raw=False):
        return usersTable.get(usersTable.token == token).__dict__['__data__'] if not raw else usersTable.get(
            usersTable.token == token)

    @wrapper
    def loginUser(self, identifier, password):
        user = usersTable.get(usersTable.email == identifier)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return None

    @wrapper
    def updateUser(self, rowId, data):

        return usersTable.update(**data).where(usersTable.id == rowId).execute()

for helperClass in [HelperCreate]:
    methodList = [func for func in dir(helperClass) if callable(getattr(helperClass, func)) and '__' not in func]
    for i, methodRaw in enumerate(methodList):
        setattr(Helper, methodRaw, classmethod(getattr(helperClass, methodRaw)))
