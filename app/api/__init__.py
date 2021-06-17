
""" Package Constructor for The API blueprint """

from flask import Blueprint

api = Blueprint('api', __name__)

from . import users