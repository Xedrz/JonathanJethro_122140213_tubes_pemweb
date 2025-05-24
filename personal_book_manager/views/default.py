from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from .. import models
import json

@view_config(route_name='home', renderer='json')
def my_view(request):
    try:
        query = request.dbsession.query(models.MyModel).all()
        result = [{'id': q.id, 'name': q.name, 'value': q.value} for q in query]
        return {'data': result}
    except DBAPIError:
        return Response(
            json.dumps({'error': db_err_msg}),
            content_type='application/json',
            status=500
        )


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
