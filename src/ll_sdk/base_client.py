#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['BaseRestAuthClient', 'BaseRestReportingClient']
__docformat__ = 'restructuredtext'

import time
import hmac
import hashlib
import logging
import requests


def get_timestamp():
    """Get timestamp in appropriate format.
    """
    return str(int(round(time.time() * 1000)))


def generate_hmac_hash(data, shared_key):
    """Generate limelight hmac hash based on .
    """
    if isinstance(data, str):
        data = data.encode('utf-8')

    return hmac.new(bytes.fromhex(shared_key),
                    msg=data,
                    digestmod=hashlib.sha256).hexdigest()


def build_base_url(hostname, context="/", port=80, scheme="http"):
    """
    Build valid URL
    """
    if port and int(port) != 80:
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname
    return requests.utils.urlunparse((str(scheme), str(netloc), str(context),
                                      None, None, None))


class LlnwUserAuth(requests.auth.AuthBase):
    """
    Basic Limelight Auth class for HMAC
    """
    HEADER_PRINCIPAL = 'X-LLNW-Security-Principal'
    HEADER_TOKEN = 'X-LLNW-Security-Token'
    HEADER_TIMESTAMP = 'X-LLNW-Security-Timestamp'

    def __init__(self, username, api_shared_key):
        self.username = username
        self.api_shared_key = api_shared_key

    def __call__(self, request):
        auth_time = request.headers.setdefault(self.HEADER_TIMESTAMP, get_timestamp())
        auth_url = request.url
        auth_data = request.method + auth_url.replace('?', '') + auth_time + (request.body if request.body else '')

        headers = {self.HEADER_PRINCIPAL: self.username,
                   self.HEADER_TOKEN: generate_hmac_hash(auth_data, self.api_shared_key)}
        for header, val in headers.items():
            request.headers.setdefault(header, val)
        return request


class BaseRestAuthClient(object):
    """
    Base rest client for Limelight Network public services
    """
    HEADER_PRINCIPAL = LlnwUserAuth.HEADER_PRINCIPAL
    HEADER_TOKEN = LlnwUserAuth.HEADER_TOKEN
    HEADER_TIMESTAMP = LlnwUserAuth.HEADER_TIMESTAMP

    def __init__(self, hostname, context, username, api_shared_key, schema, port, default_headers=None):
        self.username = username
        self.api_shared_key = api_shared_key
        self.logger = logging.getLogger('ll_sdk.' + self.__class__.__name__)
        self.base = build_base_url(hostname, context, port, schema)
        self.auth = LlnwUserAuth(self.username, self.api_shared_key)
        self.default_headers = default_headers or {}
        self._session = requests.Session()

    def __del__(self):
        self._session.close()

    def _make_request(self, method, url, *, timeout=300, **kwargs):
        req_headers = self.default_headers.copy()
        headers = kwargs.pop('headers', None)
        if headers:
            req_headers.update(headers)
        kwargs.setdefault('auth', self.auth)

        self.logger.debug(f"Sending {method} request to the {url}\n"
                          f"Parameters: {kwargs.get('params', '')}\n"
                          f"Headers: {req_headers}\n"
                          f"Body: {kwargs.get('data', '')}")
        resp = self._session.request(method, url, headers=req_headers, timeout=timeout, **kwargs)
        self.logger.debug(f"Getting response with URL: {resp.url}\n"
                          f"Code: {resp.status_code}\nHeaders: {resp.headers}\nBody: {resp.text}")
        return resp

    def _request(self, method, request_path, **kwargs):
        self.logger.debug(f"Performing request with User = {self.username}")
        headers = kwargs['headers'] or {}
        if not isinstance(headers, dict):
            headers = {}
        if 'content-type' not in headers:
            headers['content-type'] = 'application/json'
        full_url = f"{self.base}/{request_path}"
        kwargs['headers'] = headers

        resp = self._make_request(method, full_url, **kwargs)
        return resp

    def get(self, request_path, headers=None, params=None, **kwargs):
        return self._request('GET', request_path, headers=headers,
                             params=params, **kwargs)

    def head(self, request_path, headers=None, params=None, **kwargs):
        return self._request('HEAD', request_path, headers=headers,
                             params=params, **kwargs)

    def post(self, request_path, data, headers=None, params=None, files=None, **kwargs):
        return self._request('POST', request_path, data=data, headers=headers,
                             params=params, files=files, **kwargs)

    def put(self, request_path, data=None, headers=None, params=None, **kwargs):
        return self._request('PUT', request_path, data=data, headers=headers,
                             params=params, **kwargs)

    def patch(self, request_path, data=None, headers=None, params=None, **kwargs):
        return self._request('PATCH', request_path, data=data, headers=headers,
                             params=params, **kwargs)

    def delete(self, request_path, data=None, headers=None, params=None, **kwargs):
        return self._request('DELETE', request_path, data=data, headers=headers,
                             params=params, **kwargs)

    def options(self, request_path, data=None, headers=None, params=None, **kwargs):
        return self._request('OPTIONS', request_path, data=data, headers=headers,
                             params=params, **kwargs)


class BaseRestReportingClient(BaseRestAuthClient):
    """
    Base rest client for Limelight Network public reporting services
    """
    TIMEZONE_DEFAULT = 'MST'

    TODAY = 'TODAY'
    THIS_HOUR = 'THIS_HOUR'
    THIS_WEEK = 'THIS_WEEK'
    THIS_MONTH = 'THIS_MONTH'
    THIS_YEAR = 'THIS_YEAR'
    YESTERDAY = 'YESTERDAY'
    LAST_HOUR = 'LAST_HOUR'
    LAST_24_HOURS = 'LAST_24_HOURS'
    LAST_WEEK = 'LAST_WEEK'
    LAST_30_DAYS = 'LAST_30_DAYS'
    LAST_MONTH = 'LAST_MONTH'
    LAST_YEAR = 'LAST_YEAR'

    TIMESPANS = [TODAY, THIS_HOUR, THIS_WEEK, THIS_MONTH, THIS_YEAR, YESTERDAY, LAST_HOUR, LAST_24_HOURS,
                 LAST_WEEK, LAST_30_DAYS, LAST_MONTH, LAST_YEAR]

    def __init__(self, *args, **kwargs):
        super(BaseRestReportingClient, self).__init__(*args, **kwargs)

