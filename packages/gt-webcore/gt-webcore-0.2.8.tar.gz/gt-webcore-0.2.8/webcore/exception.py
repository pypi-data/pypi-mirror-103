# coding:utf-8
from .constant import Error

class GtBaseError(Exception):
    def __init__(self, code, msg, sub_code=None):
        self.code = code
        self.msg = msg
        self.sub_code = sub_code
class ParamsError(GtBaseError):
    def __init__(self, msg = None, sub_code=None):
        self.code = Error.PARAMS_ERROR
        self.msg = msg or "Parameters Error"
        self.sub_code = sub_code
class ObjectNotExistError(GtBaseError):
    def __init__(self, msg = None, sub_code=None):
        self.code = Error.OBJECT_NOT_EXSIT
        self.msg = msg or "Object Not Exist"
        self.sub_code = sub_code

class ObjectIsExistError(GtBaseError):
    def __init__(self, msg = None, sub_code=None):
        self.code = Error.OBJECT_IS_EXSIT
        self.msg = msg or "Object Is Exist"
        self.sub_code = sub_code
