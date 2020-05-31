import datetime
import traceback
import bcrypt
import peewee

from models import *
import functools

class Helper():

    def __exit__(self, exc_type, exc_value, traceback):

        if not shemdb.is_closed():
            shemdb.close()

    def loginUser(self, identifier, password):
        user = usersTable.get(usersTable.email == identifier)
        if bcrypt.checkpw(password.encode(), user.password.encode()):
            return user
        else:
            return None