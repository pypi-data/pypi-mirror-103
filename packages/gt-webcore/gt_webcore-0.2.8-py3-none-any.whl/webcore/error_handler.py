from json import JSONDecodeError

from flask import current_app as app
from werkzeug.exceptions import HTTPException

from . import exception
from .constant import Error
from .result import Result

def _handle_error(e):
    if isinstance(e, HTTPException):
        app.logger.error('Http Exception, code: {}, message: {}'
            .format(e.code, e.description))
        return Result.http_error(e.name, e.code)
    elif isinstance(e, JSONDecodeError):
        app.logger.error('JSON Exception.', exc_info = True)
        return Result.json_error()
    elif isinstance(e, exception.GtBaseError):
        return Result.error(e)
    elif isinstance(e, TypeError):
        app.logger.error('Type Error.', exc_info = True)
    elif isinstance(e, Exception):
        app.logger.error('Unkown Exception.', exc_info = True)

    return Result.error()

def init_error_handler(app):
    app.register_error_handler(Exception, _handle_error)
