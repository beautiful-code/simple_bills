from google.appengine.ext import ndb

# TODO: Use a standard cloud endpoint exception as documented on https://cloud.google.com/appengine/docs/python/endpoints/exceptions
class AccountUnauthorizedAccess(Exception):
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return repr(self.value)
