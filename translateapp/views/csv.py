import logging
import os
import csv
import uuid
import pandas as pd
import pandas.errors
from pyramid.view import view_config, view_defaults
import io
from ..models import Phrase


log = logging.getLogger(__name__)


@view_defaults(route_name='get_csv')
class GetCsv:
    COLUMNS_LIST = {'key_lang', 'ja', 'en', 'zh'}

    def __init__(self, request):
        self._request = request

    def _save_csv(self):
        pass

    @staticmethod
    def _create_csv(bytes_stream):
        def _get_path_name():
            root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            filename = '{}.csv'.format(uuid.uuid4())
            return os.path.join(root, 'csv', filename)

        buffer = io.StringIO(bytes_stream.decode('utf-8'))
        reader = csv.reader(buffer)
        path = _get_path_name()
        with open(path, 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(reader)
        return path

    @staticmethod
    def _is_all_columns_included(data_df, columns):
        return set(data_df.columns) == columns

    @view_config(request_method='POST', renderer='../templates/register.pt')
    def get_csv(self):
        log.debug('+++++++++[get_csv]+++++++++')

        csv_data_list = []
        csv_data_error_list = []

        try:
            filepath = self._create_csv(self._request.POST['csv'].value)
        except Exception as e:
            log.error(e)
            csv_data_error_list.append({'err_msg': "csvの読み込みに失敗しました: {}".format(e)})
            return dict(
                csv_data_list=csv_data_list,
                csv_data_error_list=csv_data_error_list
            )

        try:
            csv_data_df = pd.read_csv(filepath)
            csv_data_df.fillna('--', inplace=True)
        except pandas.errors.ParserError as e:
            log.error(e)
            csv_data_error_list.append({'err_msg': "csvデータのパースに失敗しました: {}".format(e)})
            return dict(
                csv_data_list=csv_data_list,
                csv_data_error_list=csv_data_error_list
            )

        if not self._is_all_columns_included(csv_data_df, self.COLUMNS_LIST):
            csv_data_error_list.append({'err_msg': "csvのカラムに誤りがあります:　{}　が必要です".format(self.COLUMNS_LIST)})
            return dict(
                csv_data_list=csv_data_list,
                csv_data_error_list=csv_data_error_list
            )

        #  save phrases to database
        for key, row in csv_data_df.iterrows():
            if '--' in row.values:
                csv_data_error_list.append({'err_msg': dict(row)})
                continue

            new_phrase = Phrase(**dict(row))
            self._request.dbsession.add(new_phrase)
            csv_data_list.append(dict(row))
        return dict(
            csv_data_list=csv_data_list,
            csv_data_error_list=csv_data_error_list
        )
