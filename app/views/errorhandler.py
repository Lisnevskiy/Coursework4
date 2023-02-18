from flask import Blueprint

errorhandler_bp = Blueprint('errorhandler_bp', __name__)


@errorhandler_bp.app_errorhandler(404)
def page_not_found(error):
    return 'Page not found', 404
