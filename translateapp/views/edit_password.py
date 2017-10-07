import json
import logging
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from ..models import User, Phrase
from ..security import hash_password, check_password


log = logging.getLogger(__name__)


@view_config(route_name='edit_password', request_method='GET', renderer='../templates/edit_password.pt')
def edit_password_log(request):
    log.debug('+++++++++[edit_password get]+++++++++')
    return {}


@view_config(route_name='edit_password', request_method='POST', renderer='json')
def edit_password(request):
    userid = authenticated_userid(request)
    log.debug('+++++++++[edit_password post]+++++++++')
    login_model = request.dbsession.query(User).filter(User.id == userid).first()
    input_password = request.params['password']
    new_password = request.params['new_password']
    log.debug(new_password)
    new_hash_password = hash_password(new_password)
    hashed_pw = login_model.password

    if login_model and check_password(input_password, hashed_pw):
        request.dbsession.query(User).filter(User.id == userid).update({User.password: new_hash_password})
        log.debug('edit_password success')
        return Response(json.dumps({'result': 1, 'message': 'パスワードを変更しました。'}))
    else:
        log.debug('edit_password failed')
        return Response(json.dumps({'result': 0, 'message': 'パスワード変更に失敗しました。'}))

