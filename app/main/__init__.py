from flask import Blueprint

main_bp = Blueprint("main", __name__, url_prefix="")

from . import pages_routes
from . import items_routes
from . import myset_routes
from . import travel_routes
from . import custom_routes
from . import weather_routes