import endpoints
from protorpc import message_types
from protorpc import messages
from protorpc import remote
from google.appengine.ext.ndb import Key
from dateutil import parser
from datetime import date,timedelta
import uuid

import settings
from models import *
from apis.api_messages import *
from apis.stats_messages import *
from apis.api_utils import *

import pprint


EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
WEB_CLIENT_ID = settings.WEB_CLIENT_ID
