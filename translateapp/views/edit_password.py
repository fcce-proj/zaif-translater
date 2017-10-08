import json
import logging
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.security import authenticated_userid
from ..models import User


logger = logging.getLogger(__name__)


@view_config(route_name='edit_password', request_method='GET', renderer='../templates/edit_password.pt')
def edit_password_log(request):
    logger.debug('+++++++++[edit_password get]+++++++++')
    return {}


@view_config(route_name='edit_password', request_method='POST', renderer='json')
def edit_password(request):
    userid = authenticated_userid(request)
    logger.debug('+++++++++[edit_password post]+++++++++')

    login_model = request.dbsession.query(User).filter(User.id == userid).first()
    input_password = request.params['password']
    if not (login_model and login_model.check_password(input_password)):
        logger.debug('edit_password failed')
        return Response(json.dumps({'result': 0, 'message': 'パスワード変更に失敗しました。'}))

    login_model.set_password(request.params['new_password'])
    logger.debug('edit_password success')
    return Response(json.dumps({'result': 1, 'message': 'パスワードを変更しました。'}))




