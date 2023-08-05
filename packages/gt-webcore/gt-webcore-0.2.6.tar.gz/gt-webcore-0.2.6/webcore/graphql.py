# -*- coding: utf-8 -

import graphene
from dotdict import DotDict
from flask_graphql import GraphQLView
from graphene import ObjectType

from webcore import app, http_request
from webcore.exception import ObjectNotExistError
from webcore.permission import check_perm
from webcore.request_parser import parse_args
from webcore.result import Result

_gpl_view = None

def init_graphql_view(bp, schema, module_name):
  @bp.route('/view', methods=['GET', 'POST', 'PUT', 'DELETE'])
  def graph_view():
    global _gpl_view

    if not _gpl_view:
      _gpl_view = GraphQLView(name='graphql', schema=schema, graphiql=True)

    return _gpl_view.dispatch_request()

  @bp.route('/exec', methods=['POST'])
  @check_perm(action='global:exec:graphql', 
    resource={'name': '$r.name', 'module': module_name})
  def exec_graphql():
    args = parse_args([
      DotDict(name='name', type=str, required=True, help='Schema 名称不能为空'),
      DotDict(name='variables', type=dict),
    ])

    schema_data = http_request.get(app.config['GRAPHQL_URL'], params={ 'module': module_name, 'name': args.name })

    if not schema_data:
      app.logger.error('Schema 数据为空, module: {}, name: {}'.format(module_name, args.name))
      raise ObjectNotExistError('Schema 数据为空')
    
    result = schema.execute(schema_data.schema, variables=args.variables)
    
    if result.data:
      return Result.ok(result.data)
    else:
      error_msgs = []

      for error in result.errors:
        error_msgs.append(error.message)

      return Result.error().set_data(error_msgs)

class PageSchema(ObjectType):
  page = graphene.Int(description='总页数')
  size = graphene.Int(description='每页数量')
  total = graphene.Int(description='总数量')
