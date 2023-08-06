# coding:utf-8
import datetime
import decimal
from enum import Enum, EnumMeta

from flask.json import JSONEncoder

from .result import Error, Result

class ApiEncoder(JSONEncoder):
    _encoders = []

    def default(self, obj):
        for encoder in self._encoders:
            try:
                result = encoder.default(obj)

                if result is not None:
                    return self.default(result)
            except Exception:
                pass

        if isinstance(obj, Result):
            return self.default(obj.__dict__)
        elif isinstance(obj, Enum):
            return self.default(obj.value)
        elif isinstance(obj, list):
            obj_list = []

            for o in obj:
                obj_list.append(self.default(o))
            return obj_list
        elif isinstance(obj, dict):
            for k in obj:
                try:
                    obj[k] = self.default(obj[k])
                except TypeError:
                    obj[k] = None
            return obj
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        elif isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return obj
            
    @classmethod
    def add_encoder(cls, encoder):
        cls._encoders.append(encoder)

    @classmethod
    def remove_encoder(cls, encoder):
        cls._encoders.remove(encoder)
