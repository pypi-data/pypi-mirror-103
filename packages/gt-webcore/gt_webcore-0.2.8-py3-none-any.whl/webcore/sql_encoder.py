# -*- encoding: utf-8 -*-
'''
@File    :   sql_encoder.py
@Time    :   2021/04/27 14:25:00
@Author  :   wunan
@Version :   1.0
@Contact :   wunan799@163.com
@License :   (C)Copyright 人和未来生物科技（长沙）有限公司
@Desc    :   SQLALCHEMY 模型JSON序列化
'''
from flask_sqlalchemy.model import Model
from sqlalchemy.util._collections import AbstractKeyedTuple
from flask.json import JSONEncoder 

class SqlEncoder(JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Model):
        return {i.name: getattr(obj, i.name) for i in obj.__table__.columns}
    elif isinstance(obj, AbstractKeyedTuple):
        return obj._asdict()

    return None