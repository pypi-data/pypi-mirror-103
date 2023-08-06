# pylint: disable=logging-fstring-interpolation, too-many-nested-blocks, too-few-public-methods

import logging
import pickle

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import ServerNotFoundError
from oauth2client.client import OAuth2WebServerFlow

from data_tap.base_tap import BaseTap
from data_tap.decorators import _retry_handler, _delay_handler
from data_tap.utils import _date_range, _date_handler


class GoogleSeachConsoleTap(BaseTap):
    """
    The Google Search Console TAP gives you access to the power of the Google Search Console.
    The API provides these key features:
        - Metric expressions
        - Multiple date ranges & date batching
        - Multiple segments
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.version = 'v3'
        self.service_name = 'webmasters'
        self.oauth_scope = 'https://www.googleapis.com/auth/webmasters.readonly'
        self.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

        self.service = self._authenticate()

    def generate_authentication(self, auth_file='gsc_credentials.pickle'):
        """
        A user friendly method to generate a .pickle file for future authentication.
        For the first time, you would need to log in with your web browser based on
        this web authentication flow. After that, it will save your credentials in
        a pickle file. Every subsequent time you run the script, it will use the
        “pickled” credentials stored in credentials.pickle to build the
        connection to Search Console.
        """
        client_id = self.creds['installed'].get('client_id')
        client_secret = self.creds['installed'].get('client_secret')

        flow = OAuth2WebServerFlow(
            client_id=client_id,
            client_secret=client_secret,
            scope=self.oauth_scope,
            redirect_uri=self.redirect_uri
        )

        authorize_url = flow.step1_get_authorize_url()
        logging.info(f'Go to the following link in your browser: {authorize_url}')
        code = input('Enter verification code: ').strip()
        credentials = flow.step2_exchange(code)
        pickle.dump(credentials, open(auth_file, 'wb'))

    def _authenticate(self):
        """
        Makes use of the .pickle cred file to establish a webmaster connection.
        """
        logging.info('Authenticating connection')
        credentials = pickle.load(open(self.creds, 'rb'))
        return build(
            serviceName=self.service_name,
            version=self.version,
            credentials=credentials
        )

    def _de_normalize_report(self, response, site_url, search_type) -> list:
        """
        Converts a ga report into a de normalized flat file structure.
        :return: dict. gsc report.
        """
        data_set = []
        for row in response['rows']:
            row['site_url'] = site_url
            row['search_type'] = search_type

            row.update(
                dict(zip(self.config.get('dimensions'), row.get('keys')))
            )
            del row['keys']

            data_set.append(row)

        return data_set

    @_delay_handler()
    @_retry_handler((TimeoutError, OSError, ServerNotFoundError, HttpError))
    def _query(self, query_config, site_url) -> dict:
        """
        Separated query method to handle retry and delay methods.
        :param query_config: dict. standardised query structure.
        :return: dict. ga response object.
        """
        logging.info(f'Running query: {query_config}')
        # pylint: disable=no-member
        return self.service.searchanalytics().query(
            siteUrl=site_url,
            body=query_config
        ).execute()

    def run_query(self):
        """
        Run Google Search Console query that queries per search type and url and
        is able to batch by date.

        gsc_tap = GoogleSeachConsoleTap(
            config_file='',
            creds_file=''
        )

        for report in gsc_tap.run_query():
            print(report)

        :yield: dict. de_normalised google search console report
        """
        site_urls = self.config.get('site_urls')
        search_types = self.config.get('search_types')

        for site_url in site_urls:
            logging.info(f'Querying site url: {site_url}')
            for search_type in search_types:
                if self.config.get('batch_dates', True):
                    logging.info('Batching query by date.')

                    # date chunking is needed so get range of dates
                    date_ranges = _date_range(
                        start_date=self.config.get('start_date'),
                        end_date=self.config.get('end_date')
                    )
                    for date in date_ranges:
                        logging.info(f'Querying at date: {date}')

                        row_index = 0
                        # run until page token is None
                        while True:
                            logging.info(f'Querying API at row index: {row_index}')

                            query_config = {
                                'startDate': date,
                                'endDate': date,
                                'dimensions': self.config.get('dimensions'),
                                'metrics': self.config.get('metrics'),
                                'searchType': search_type,
                                'rowLimit': self.config.get('maxRows', 25000),
                                'startRow': row_index * self.config.get('maxRows', 25000)
                            }

                            response = self._query(
                                site_url=site_url,
                                query_config=query_config
                            )

                            if response is None:
                                logging.info('Response is None, stopping.')
                                break
                            if 'rows' not in response:
                                logging.info('No more data in Response.')
                                break

                            yield self._de_normalize_report(
                                response=response,
                                site_url=site_url,
                                search_type=search_type
                            )

                            row_index += 1

                else:
                    # date chunking is not needed so set range of dates once
                    start_date = _date_handler(self.config.get('start_date'))
                    end_date = _date_handler(self.config.get('end_date'))

                    if start_date != end_date:
                        logging.warning('Date batching is recommended for date ranges')

                    row_index = 0
                    # run until page token is None
                    while True:
                        logging.info(f'Querying API at row index: {row_index}')

                        query_config = {
                            'startDate': start_date,
                            'endDate': end_date,
                            'dimensions': self.config.get('dimensions'),
                            'metrics': self.config.get('metrics'),
                            'searchType': search_type,
                            'rowLimit': self.config.get('maxRows', 25000),
                            'startRow': row_index * self.config.get('maxRows', 25000)
                        }

                        response = self._query(
                            site_url=site_url,
                            query_config=query_config
                        )

                        if response is None:
                            logging.info('Response is None, stopping.')
                            break
                        if 'rows' not in response:
                            logging.info('No more data in Response.')
                            break

                        yield self._de_normalize_report(
                            response=response,
                            site_url=site_url,
                            search_type=search_type
                        )

                        row_index += 1
