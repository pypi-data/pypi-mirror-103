# pylint: disable=logging-fstring-interpolation, too-many-nested-blocks, too-few-public-methods

import collections
import logging

import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
from oauth2client.service_account import ServiceAccountCredentials

from data_tap.base_tap import BaseTap
from data_tap.decorators import _retry_handler, _delay_handler
from data_tap.utils import _date_range, _date_handler


class GoogleAnalyticsTap(BaseTap):
    """
    The Google Analytics TAP gives you access to the power of the Google Analytics platform.
    The API provides these key features:
        - Metric expressions
        - Multiple date ranges & date batching
        - Multiple segments

    from data_tap.google_tap.google_analytics import GoogleAnalyticsTap

    ga_tap = GoogleAnalyticsTap(
        config_file='',
        creds_file='',
        auth_method='',
        service_account_email='',

        log_level='',
        log_file=''
    )

    for report in ga_tap.run_query():
        print(report)

    """

    def __init__(self, auth_method, **kwargs):
        super().__init__(**kwargs)

        self.auth_method = auth_method
        self.version = 'v4'
        self.service_name = 'analyticsreporting'
        self.scopes = ['https://www.googleapis.com/auth/analytics.readonly']
        self.service_account_email = kwargs['service_account_email']
        self.analytics = self._authenticate()

    def _authenticate(self):
        """
        Standard GA authentication method.
        :return: object. GA authentication object.
        """
        logging.info('Authenticating connection')
        if self.auth_method == 'json':
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                filename=self.creds_file,
                scopes=self.scopes
            )
        elif self.auth_method == 'p12':
            credentials = ServiceAccountCredentials.from_p12_keyfile(
                filename=self.creds_file,
                scopes=self.scopes,
                service_account_email=self.service_account_email
            )
        else:
            raise ValueError('Auth method type is not valid: [json, p12].')

        return build(serviceName=self.service_name, version=self.version, credentials=credentials)

    @staticmethod
    def _de_normalize_report(reports: dict, view_id: str) -> dict:
        """
        Converts a ga reort into a de normalized flat file structure.
        :return: dict. ga report.
        """
        data_set = pd.DataFrame()
        for report in reports:
            column_header = report['columnHeader']['dimensions']
            metric_header = report['columnHeader']['metricHeader']['metricHeaderEntries']

            columns = column_header
            for metric in metric_header:
                columns.append(metric['name'])

            data = pd.json_normalize(report['data']['rows'])
            data_dimensions = pd.DataFrame(data['dimensions'].tolist())
            data_metrics = pd.DataFrame(data['metrics'].tolist())
            data_metrics = data_metrics.applymap(lambda x: x['values'])
            data_metrics = pd.DataFrame(data_metrics[0].tolist())
            result = pd.concat([data_dimensions, data_metrics], axis=1, ignore_index=True)
            result.columns = column_header

            data_set = data_set.append(result, ignore_index=True)
            data_set['ga:viewId'] = view_id

        return data_set.to_dict(orient='records')

    @_delay_handler()
    @_retry_handler((TimeoutError, OSError, ServerNotFoundError, HttpError))
    def _query(self, query_config: dict) -> dict:
        """
        Separated query method to handle retry and delay methods.
        :param query_config: dict. standardised query structure.
        :return: dict. ga response object.
        """
        logging.info(f'Running query: {query_config}')
        return self.analytics.reports().batchGet(
            body={'reportRequests': [
                {
                    'viewId': query_config.get('view_id', None),
                    'dateRanges': [
                        {
                            'startDate': query_config.get('start_date', None),
                            'endDate': query_config.get('end_date', None)
                        }
                    ],
                    'metrics': query_config.get('metrics', None),
                    'dimensions': query_config.get('dimensions', None),
                    'orderBys': query_config.get('order_bys', None),
                    'pageSize': query_config.get('page_size', None),
                    'pageToken': query_config.get('page_token', '0')
                }
            ]}).execute()

    def run_query(self) -> collections.Iterable:
        """
        Run Google Analytics query that queries per view_id and
        is able to batch by date.

        ga_tap = GoogleAnalyticsTap(
            config_file='',
            creds_file='',
            auth_method='',
            service_account_email=''
        )

        for report in ga_tap.run_query():
            print(report)

        :yield: dict. de_normalised google analytics report
        """
        view_ids = self.config.get('view_ids')
        for view_id in view_ids:
            logging.info(f'Querying view id: {view_id}')
            if self.config.get('batch_dates', True):
                logging.info('Batching query by date.')

                # date chunking is needed so get range of dates
                date_ranges = _date_range(
                    start_date=self.config.get('start_date'),
                    end_date=self.config.get('end_date')
                )
                for date in date_ranges:
                    logging.info(f'Querying at date: {date}')

                    page_token = 0
                    # run until page token is None
                    while page_token is not None:
                        logging.info(f'Querying API at page token: {page_token}')
                        response = self._query(
                            query_config={
                                'page_token': str(page_token),
                                'view_id': view_id,
                                'start_date': date,  # date chunking is needed so update dates
                                'end_date': date,  # date chunking is needed so update dates
                                'metrics': self.config.get('metrics', None),
                                'dimensions': self.config.get('dimensions', None),
                                'order_bys': self.config.get('order_bys', None),
                                'pageSize': self.config.get('pageSize', None)
                            }
                        )
                        for report in response.get('reports', []):
                            # set page token to value or None
                            page_token = report.get('nextPageToken', None)

                        yield self._de_normalize_report(response.get('reports', []), view_id)

            else:
                # date chunking is not needed so set range of dates once
                start_date = _date_handler(self.config.get('start_date'))
                end_date = _date_handler(self.config.get('end_date'))
                if start_date != end_date:
                    logging.warning('Date batching is recommended for date ranges')

                page_token = 0
                # run until page token is None
                while page_token is not None:
                    logging.info(f'Querying API at page token: {page_token}')

                    response = self._query(
                        query_config={
                            'page_token': str(page_token),
                            'view_id': view_id,
                            'start_date': start_date,
                            'end_date': end_date,
                            'metrics': self.config.get('metrics', None),
                            'dimensions': self.config.get('dimensions', None),
                            'order_bys': self.config.get('order_bys', None),
                            'pageSize': self.config.get('pageSize', 1000)
                        }
                    )
                    for report in response.get('reports', []):
                        # set page token to value or None
                        page_token = report.get('nextPageToken', None)

                    yield self._de_normalize_report(response.get('reports', []), view_id)
