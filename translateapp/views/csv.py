import logging
import os
import csv
import uuid
import shutil
import pandas as pd
from pyramid.view import view_config, view_defaults

from ..models import (
    get_engine,
    get_session_factory,
    User,
    Phrase,
)

session = None
log = logging.getLogger(__name__)


@view_defaults(route_name='get_csv')
class GetCsv:
    def __init__(self, request):
        self._request = request

    @view_config(request_method='POST', renderer='../templates/register.pt')
    def get_csv(self):
        log.debug('+++++++++[get_csv]+++++++++')
        #filename = self._request.POST['csv'].filename
        input_file = self._request.POST['csv'].file
        print(input_file)
        print('====================================================')

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


# ['GET', 'POST', 'ResponseClass', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__',
# '__ge__', '__getattribute__', '__gt__', '__hash__', '__implemented__', '__init__', '__le__', '__lt__', '__module__',
# '__ne__', '__new__', '__providedBy__', '__provides__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
#  '__sizeof__', '__str__', '__subclasshook__', '__view__', '__weakref__', '_cache_control__del', '_cache_control__get',
#  '_cache_control__set', '_charset', '_check_charset', '_content_type__get', '_content_type__set', '_content_type_raw',
#  '_get_authentication_policy', '_headers', '_headers__get', '_headers__set', '_host__del', '_host__get', '_host__set',
#  '_json_body__del', '_json_body__get', '_json_body__set', '_partial_application_url', '_process_finished_callbacks',
#  '_process_response_callbacks', '_setattr_stacklevel',
#  '_text__del', '_text__get', '_text__set', '_update_cache_control',
#  '_urlargs__del', '_urlargs__get', '_urlargs__set', '_urlvars__del',
# '_urlvars__get', '_urlvars__set', 'accept', 'accept_charset',
#  'accept_encoding', 'accept_language', 'add_finished_callback', 'add_response_callback',
# 'application_url', 'as_bytes', 'as_text',
#  'authenticated_userid', 'authorization', 'blank', 'body', 'body_file', 'body_file_raw',
# 'body_file_seekable', 'cache_control',
# 'call_application', 'charset', 'client_addr', 'content_length', 'content_type', 'context',
#  'cookies', 'copy', 'copy_body', 'copy_get',
#  'current_route_path', 'current_route_url', 'date', 'dbsession',
# 'debug_toolbar', 'decode', 'domain', 'effective_principals',
#  'encget', 'encset', 'environ', 'exc_info', 'exception', 'finished_callbacks', 'from_bytes', 'from_file', 'from_text',
#  'get_response', 'has_permission', 'headers', 'host', 'host_port',
#  'host_url', 'http_version', 'if_match', 'if_modified_since',
# 'if_none_match', 'if_range', 'if_unmodified_since', 'invoke_exception_view', 'invoke_subrequest', 'is_body_readable',
#  'is_body_seekable', 'is_response', 'is_xhr', 'json', 'json_body', 'locale_name', 'localizer', 'make_body_seekable',
#  'make_default_send_app', 'make_tempfile', 'matchdict', 'matched_route', 'max_forwards', 'method', 'model_url',
#  'params', 'path', 'path_info', 'path_info_peek', 'path_info_pop',
# 'path_qs', 'path_url', 'pdtb_id', 'pdtb_sqla_queries',
#  'pragma', 'query_string', 'range', 'referer', 'referrer', 'registry', 'relative_url', 'remote_addr', 'remote_user',
# 'remove_conditional_headers', 'request_body_tempfile_limit', '
# request_iface', 'resource_path', 'resource_url', 'response',
# 'response_callbacks', 'root', 'route_path', 'route_url', 'scheme', 'script_name',
# 'send', 'server_name', 'server_port',
#  'session', 'set_property', 'static_path', 'static_url', 'subpath', 'text', 'tm', 'tmpl_context', 'traversed',
# 'unauthenticated_userid', 'upath_info', 'url', 'url_encoding', 'urlargs', 'urlvars', 'uscript_name', 'user',
#  'user_agent', 'view_name', 'virtual_root', 'virtual_root_path']
