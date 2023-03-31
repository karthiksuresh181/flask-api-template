from flask import Blueprint
from flask_restx import Api
from flask import current_app as app

blueprint = Blueprint('deadpool-alerts', __name__)
__doc_location__ = False
api = Api(blueprint, version="1.0", title="Deadpool Alerts",
          description="Rest API related to deadpool alert service", doc=__doc_location__)


@api.errorhandler(Exception)
def error_handler(error):
    """ Error Handler for the App """
    app.logger.error("Error thrown::")
    app.logger.error(error.args)
    return {'message': error.args}, 400
