#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import tzset
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from requests.structures import CaseInsensitiveDict

__all__ = ['_timespan']
__docformat__ = 'restructuredtext'


def _set_timezone(timezone):
    os.environ['TZ'] = timezone
    tzset()


def _timespan(timespan, timezone):
    """
    Right -7 timezone, TODO: make it configured.
        :param timespan:

    """
    _set_timezone(timezone=timezone)
    td = datetime.today()
    _timespans = CaseInsensitiveDict({
        "TODAY": (datetime(td.year, td.month, td.day).timestamp(), td.timestamp()),
        "THIS_HOUR": (datetime(td.year, td.month, td.day, td.hour).timestamp(), td.timestamp()),
        "THIS_WEEK": (datetime(td.year, td.month, td.day - td.weekday()).timestamp(), td.timestamp()),
        "THIS_MONTH": (datetime(td.year, td.month, 1).timestamp(), td.timestamp()),
        "THIS_YEAR": (datetime(td.year, 1, 1).timestamp(),
                      td.timestamp()),
        "YESTERDAY": ((datetime(td.year, td.month, td.day) - relativedelta(days=1)).timestamp(),
                      datetime(td.year, td.month, td.day).timestamp()),
        "LAST_HOUR": ((datetime(td.year, td.month, td.day, td.hour) - relativedelta(hours=1)).timestamp(),
                      datetime(td.year, td.month, td.day, td.hour).timestamp()),
        "LAST_24_HOURS": ((datetime(td.year, td.month, td.day, td.hour) - relativedelta(hours=24)).timestamp(),
                          datetime(td.year, td.month, td.day, td.hour).timestamp()),
        "LAST_WEEK": ((datetime(td.year, td.month, td.day - td.weekday()) - relativedelta(weeks=1)).timestamp(),
                      datetime(td.year, td.month, td.day - td.weekday()).timestamp()),
        "LAST_30_DAYS": ((datetime(td.year, td.month, td.day) - relativedelta(days=30)).timestamp(),
                         datetime(td.year, td.month, td.day).timestamp()),
        "LAST_MONTH": ((datetime(td.year, td.month, td.day) - relativedelta(months=1)).timestamp(),
                       datetime(td.year, td.month, td.day).timestamp()),
        "LAST_YEAR": ((datetime(td.year, td.month, td.day) - relativedelta(years=1)).timestamp(),
                      datetime(td.year, td.month, td.day).timestamp())})

    if timespan not in _timespans:
        raise Exception(f'invalid value {timespan}, expected {_timespans.keys()}')

    return [int(i) for i in _timespans[timespan]]