import json
import logging
from pyramid.response import Response
from pyramid.view import view_config
from ..models import User
from pyramid.security import remember, forget
from pyramid.httpexceptions import HTTPFound


logger = logging.getLogger(__name__)


@view_config(route_name='login', request_method='GET', renderer='../templates/login.pt')
def login_log(request):
    logger.debug('+++++++++[login get]+++++++++')
    return {}


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    logger.debug('+++++++++[login post]+++++++++')
    login_model = request.dbsession.query(User).filter(User.name == request.params['name']).first()

    if login_model.check_password(request.params['password']):
        logger.debug('login success')
        headers = remember(request, login_model.id, max_age='86400')
        return Response(json.dumps({'query': 'register'}), headers=headers)

    logger.debug('login failed')
    return Response()


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('login')
    return HTTPFound(location=url, headers=headers)
