# pylint: disable=logging-fstring-interpolation, too-many-nested-blocks, too-few-public-methods

import logging
import time
from functools import wraps
from random import uniform


def _retry_handler(
        exceptions,
        total_tries: int = 5,
        initial_wait: float = 0.5,
        backoff_factor: int = 2,
        should_raise: bool = False
):
    def retry_decorator(function):
        @wraps(function)
        def func_with_retries(*args, **kwargs):
            """
            Decorate function with retry functionality.
            """
            _tries, _delay = total_tries, initial_wait
            while _tries > 0:
                try:
                    return function(*args, **kwargs)
                except exceptions as exception:
                    if should_raise:
                        raise exception

                    logging.info(f'Function: {function.__name__}. '
                                 f'Exception: {exception}. '
                                 f'Retrying in {_delay} seconds!')

                    _tries -= 1
                    time.sleep(_delay)
                    _delay = _delay * backoff_factor

        return func_with_retries

    return retry_decorator


def _delay_handler(
        interval_max: int = 3,
        interval_min: int = 1
):
    def delay_decorator(function):
        @wraps(function)
        def func_with_delays(*args, **kwargs):
            """
            Decorate function with delay functionality.
            """
            _delay = round(uniform(interval_min, interval_max), 2)
            logging.info(f'Staggering request with a {_delay} second delay')
            time.sleep(_delay)

            return function(*args, **kwargs)

        return func_with_delays

    return delay_decorator
