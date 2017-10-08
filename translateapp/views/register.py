import logging
import os
import uuid
import shutil
import pandas as pd
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid

from ..models import (
    get_engine,
    get_session_factory,
    User,
    Phrase,
)


log = logging.getLogger(__name__)


@view_config(route_name='register', renderer='../templates/register.pt')
def register_view(request):
    log.debug('+++++++++[register get]+++++++++')
    userid = authenticated_userid(request)
    login_user = request.dbsession.query(User).filter(User.id == userid).first()

    if login_user is None:
        return HTTPFound(location=request.route_url('login'))

    language_list = request.dbsession.query(Phrase).all()
    return dict(login_user=login_user, Language_list=language_list)


@view_config(route_name='register', request_method='POST', renderer='json')
def register(request):
    log.debug('+++++++++[register post]+++++++++')
    japanese = request.params['ja']
    english = request.params['en']
    chinese = request.params['zh']

    if japanese is None:
        return dict(key=japanese, register_flag=False)

    phrases = request.dbsession.query(Phrase).filter(Phrase.key_lang == japanese).all()
    if japanese in phrases:
        log.debug('already registered: {}'.format(japanese))
        return dict(key=japanese, register_flag=False)

    new_phrase = Phrase(key_lang=japanese, ja=japanese, en=english, zh=chinese)
    request.dbsession.add(new_phrase)
    log.debug('registered: {}'.format(japanese))
    return dict(key=japanese, register_flag=True)


@view_config(route_name='edit', request_method='POST', renderer='json')
def edit(request):
    log.debug('+++++++++[edit]+++++++++')
    edit_id = int(request.params['edit_id'])
    new_key_lang = request.params['edit_key']
    new_japanese = request.params['edit_ja']
    new_english = request.params['edit_en']
    new_chinese = request.params['edit_zh']

    request.dbsession.query(Phrase).filter(Phrase.id == edit_id).update({
        Phrase.key_lang: new_key_lang,
        Phrase.ja: new_japanese,
        Phrase.en: new_english,
        Phrase.zh: new_chinese,
    })


@view_config(route_name='search', request_method='POST', renderer='../templates/register.pt')
def search(request):
    log.debug('+++++++++[search]+++++++++')
    search_words = request.params['search']

    for key in ('key_lang', 'ja', 'en', 'zh'):
        phrases = request.dbsession.query(Phrase).filter(
            eval("Phrase." + key + ".ilike('%" + search_words + "%')")).all()
        if phrases:
            return dict(Phrase=phrases)

    return dict(Phrase=[])


@view_defaults(route_name='get_csv')
class GetCsv:
    def __init__(self, request):
        self._request = request

    @view_config(request_method='POST', renderer='../templates/register.pt')
    def get_csv(self):
        log.debug('+++++++++[get_csv]+++++++++')
        filename = self._request.POST['csv'].filename
        input_file = self._request.POST['csv'].file
        file_path = os.path.join('translateapp/csv', '%s.csv' % uuid.uuid4())
        temp_file_path = file_path + '~'
        input_file.seek(0)

        with open(temp_file_path, 'wb') as output_file:
            shutil.copyfileobj(input_file, output_file)

        os.rename(temp_file_path, file_path)
        os.chdir("translateapp/csv")
        csv_filename = str(file_path.replace('translateapp/csv/', ''))
        csv_data = pd.read_csv(csv_filename)
        csv_data_list = []
        csv_data_error_list = []
        os.chdir("../..")

        if self._check_csv_columname(csv_data, csv_data_list) is False:
            return dict(
                csv_data_list=csv_data_list,
                csv_data_error_list=''
                )

        self._csv_commit(csv_data, csv_data_list, csv_data_error_list)

        return dict(
            csv_data_list=csv_data_list,
            csv_data_error_list=csv_data_error_list
            )

    def _check_csv_columname(self, csv_data, csv_data_list):
        if csv_data.columns[0] == 'key_lang' and csv_data.columns[1] == 'ja' and csv_data.columns[2] == 'en' and csv_data.columns[3] == 'zh':
            return True
        else:
            csv_data_list.append({'key_lang': '添付ファイルのカラム名が正しくありません 正しくは: key_lang', 'ja': 'ja', 'en': 'en', 'zh': 'zh'})
            return False

    def _csv_commit(self, csv_data, csv_data_list, csv_data_error_list):
        if not len(csv_data['key_lang']) == 0 and not len(csv_data['ja']) == 0 and not len(csv_data['en']) == 0 and not len(csv_data['zh']) == 0:
            stop_loop = len(csv_data['key_lang'])
            num = 0
            while num < stop_loop:
                Language_list_key = self._request.dbsession.query(Phrase).filter(Phrase.key_lang == csv_data['key_lang'][num]).all()
                log.debug('+++++++++[get_csv test]+++++++++')
                csv_data_list.append({'key_lang': csv_data['key_lang'][num], 'ja': csv_data['ja'][num], 'en': csv_data['en'][num], 'zh': csv_data['zh'][num]})
                if len(Language_list_key) == 0 and not csv_data['key_lang'][num] != csv_data['key_lang'][num] and not csv_data['ja'][num] != csv_data['ja'][num] and not csv_data['en'][num] != csv_data['en'][num] and not csv_data['zh'][num] != csv_data['zh'][num]:
                    '''nanの判定'''
                    register_list = Phrase(key_lang=csv_data['key_lang'][num], ja=csv_data['ja'][num], en=csv_data['en'][num], zh=csv_data['zh'][num])
                    session.add(register_list)
                    log.debug('commit')
                else:
                    csv_data_error_list.append({'err_msg': csv_data['key_lang'][num]})
                    log.debug('not commit')
                num += 1
            session.commit()
