#from google.appengine.ext.webapp import template
from base import BaseHandler
from oauth import *

import jinja2
import os

import settings
from views.utils import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + "/../templates/"),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
