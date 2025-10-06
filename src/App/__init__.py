from flask import Flask

app = Flask(__name__)

from App.routes.api   import *
from App.routes.views import *