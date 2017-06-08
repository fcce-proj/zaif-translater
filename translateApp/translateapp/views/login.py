import json
import hashlib
import logging
from pyramid.response import Response
from pyramid.view import view_config, forbidden_view_config
from ..models.users import Users, Phrase
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound,
    )

log = logging.getLogger(__name__)


@view_config(route_name='login', request_method='GET', renderer='../templates/login.pt')
def loginlo(request):
    log.debug('+++++++++[login get]+++++++++')
    return {}


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    log.debug('+++++++++[login post]+++++++++')
    login_model = request.dbsession.query(Users).filter(Users.name == request.params['name']).first()
    type_password = request.params['password']
    checkPass = createHash(login_model.password_hash.encode('utf-8'))
    password = createHash(type_password.encode('utf-8'))

    if login_model is not None and checkPass == password:
        log.debug('login success')
        headers = remember(request, login_model.id)
        return Response(json.dumps({'query': 'register'}), headers=headers)
    else:
        log.debug('login failed')
        return Response()

def createHash(password):
    hashObj = hashlib.sha1()
    hashObj.update(password)

    return hashObj.hexdigest()
