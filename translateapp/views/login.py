import json
import logging
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from ..models.models import Users, Phrase
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )
from pyramid.security import authenticated_userid
from ..security import (
    hash_password,
    check_password
    )


log = logging.getLogger(__name__)


@view_config(route_name='login', request_method='GET', renderer='../templates/login.pt')
def login_log(request):
    log.debug('+++++++++[login get]+++++++++')
    return {}


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    userid = authenticated_userid(request)
    log.debug('+++++++++[login post]+++++++++')
    login_model = request.dbsession.query(Users).filter(Users.name == request.params['name']).first()
    input_password = request.params['password']
    hashed_pw = login_model.password

    if login_model and check_password(input_password, hashed_pw):
        log.debug('login success')
        headers = remember(request, login_model.id, max_age='86400')
        return Response(json.dumps({'query': 'register'}), headers=headers)
    else:
        log.debug('login failed')
        return Response()


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    url = request.route_url('login')
    return HTTPFound(location=url, headers=headers)
