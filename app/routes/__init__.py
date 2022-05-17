from flask import Blueprint


main = Blueprint("main", __name__, url_prefix="/")
coupon_api = Blueprint("coupon_api", __name__, url_prefix="/api/coupon")
scrum_api = Blueprint("scrum_api", __name__, url_prefix="/api/scrum")

from . import coupon, routes, scrum