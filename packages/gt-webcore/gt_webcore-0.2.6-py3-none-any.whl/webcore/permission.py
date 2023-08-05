# -*- coding: utf-8 -
from flask import current_app as app
from flask import request, g
from webcore.constant import Error
from webcore import exception
from webcore import http_request
import functools

def check_perm(action='', resource={}, context={}):
    """
    权限判断
    :param action: 动作，字符串表示函数标识，字典表示动作属性
    :param resource: 资源
    :param context: 环境，默认会传请求ip
    """
    if isinstance(action, str):
        action = { 'method': action }

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __replace_resource_value(resource)
            token = request.headers.get('Authorization')
            system_id = app.config['SYSTEM_ID']
            auth_url = app.config['AUTH_URL']

            if not system_id:
                raise exception.ParamsError('没有配置系统标识')

            if not auth_url:
                raise exception.ParamsError('没有配置授权服务地址')

            try:
                payload = http_request.post(auth_url, json = {
                    'system_id': system_id,
                    'token': token,
                    'action': action,
                    'resource': resource,
                    'context': dict(context, ip=request.remote_addr)
                })
            except Exception as e:
                app.logger.error('请求授权服务出错: {}'.format(e))
                raise exception.GtBaseError(Error.AUTHOR_ERROR, '访问授权服务出错')

            if not payload:
                raise exception.GtBaseError(Error.AUTHOR_ERROR, '没有访问授权')

            g.__dict__.update(payload)
            return func(*args, **kwargs)

        return wrapper
    return decorator

def __replace_resource_value(resource):
    for k in resource:
        v = resource[k]

        if not isinstance(v, str):
            continue

        if v.startswith('$r.'):
            arr = v.split('.')

            if len(arr) < 2:
                continue

            new_value = request.values.get(arr[1])
            resource[k] = new_value
            app.logger.debug('替换授权资源内容: {}={}'.format(v, new_value))