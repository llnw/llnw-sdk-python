#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from itertools import chain
from sdk.base_client import BaseRestReportingClient
from sdk.utils.reporting_api_helper.time_utils import _timespan as timespan

__all__ = ['ReportingClient']
__docformat__ = 'restructuredtext'


class ReportingClient(BaseRestReportingClient):
    REQUESTED_FIELD_DATETIME = "datetime"
    REQUESTED_FIELD_SHORTNAME = "shortname"
    REQUESTED_FIELD_URL = "url"
    REQUESTED_FIELD_PUBLISHED_HOST = "publishedHost"
    REQUESTED_FIELD_TYPE = "type"
    REQUESTED_FIELD_RANGE = "range"
    REQUESTED_FIELD_REFERRER_URL = "refUrl"
    REQUESTED_FIELD_TOTAL_REQUESTS = "totalRequests"
    REQUESTED_FIELD_OUT_REQUESTS = "outRequests"
    REQUESTED_FIELD_IN_REQUESTS = "inRequests"
    REQUESTED_FIELD_TOTAL_REQUESTS_PER_SECOND = "totalRequestsPerSec"
    REQUESTED_FIELD_OUT_REQUESTS_PER_SECOND = "outRequestsPerSec"
    REQUESTED_FIELD_IN_REQUESTS_PER_SECOND = "inRequestsPerSec"
    REQUESTED_FIELD_TOTAL_BYTES = "totalBytes"
    REQUESTED_FIELD_OUT_BYTES = "outBytes"
    REQUESTED_FIELD_IN_BYTES = "inBytes"
    REQUESTED_FIELD_TOTAL_BITS_PER_SECOND = "totalBitsPerSec"
    REQUESTED_FIELD_OUT_BITS_PER_SECOND = "outBitsPerSec"
    REQUESTED_FIELD_IN_BITS_PER_SECOND = "inBitsPerSec"
    REQUESTED_FIELD_USER_AGENT = "userAgent"

    ALL_METRIC_FIELDS = [
        REQUESTED_FIELD_TOTAL_BYTES, REQUESTED_FIELD_OUT_BYTES, REQUESTED_FIELD_IN_BYTES,
        REQUESTED_FIELD_TOTAL_BITS_PER_SECOND, REQUESTED_FIELD_OUT_BITS_PER_SECOND, REQUESTED_FIELD_IN_BITS_PER_SECOND,
        REQUESTED_FIELD_TOTAL_REQUESTS, REQUESTED_FIELD_OUT_REQUESTS, REQUESTED_FIELD_IN_REQUESTS,
        REQUESTED_FIELD_TOTAL_REQUESTS_PER_SECOND, REQUESTED_FIELD_OUT_REQUESTS_PER_SECOND,
        REQUESTED_FIELD_IN_REQUESTS_PER_SECOND
    ]

    BYTES_PER_REQUEST_REQUESTED_FIELDS = [REQUESTED_FIELD_RANGE, REQUESTED_FIELD_DATETIME, REQUESTED_FIELD_SHORTNAME,
                                          REQUESTED_FIELD_OUT_BYTES, REQUESTED_FIELD_OUT_REQUESTS]
    FILE_TYPES_REQUESTED_FIELDS = list(
        chain(*[[REQUESTED_FIELD_TYPE, REQUESTED_FIELD_DATETIME, REQUESTED_FIELD_SHORTNAME],
                ALL_METRIC_FIELDS]))
    ORIGIN_FILES_REQUESTED_FIELDS = [REQUESTED_FIELD_URL, REQUESTED_FIELD_DATETIME,
                                     REQUESTED_FIELD_SHORTNAME, REQUESTED_FIELD_IN_REQUESTS]
    PUBLISHED_HOSTS_REQUESTED_FIELDS = list(chain(*[[REQUESTED_FIELD_PUBLISHED_HOST, REQUESTED_FIELD_DATETIME,
                                                     REQUESTED_FIELD_SHORTNAME], ALL_METRIC_FIELDS]))
    REFERRER_URLS_REQUESTED_FIELDS = list(chain(*[[REQUESTED_FIELD_REFERRER_URL, REQUESTED_FIELD_DATETIME,
                                                   REQUESTED_FIELD_SHORTNAME], ALL_METRIC_FIELDS]))
    TRAFFIC_URLS_REQUESTED_FIELDS = list(
        chain(*[[REQUESTED_FIELD_URL, REQUESTED_FIELD_DATETIME, REQUESTED_FIELD_SHORTNAME],
                ALL_METRIC_FIELDS]))
    USER_AGENTS_REQUESTED_FIELDS = [REQUESTED_FIELD_USER_AGENT, REQUESTED_FIELD_DATETIME, REQUESTED_FIELD_SHORTNAME,
                                    REQUESTED_FIELD_OUT_BYTES, REQUESTED_FIELD_OUT_REQUESTS]

    def __init__(self, hostname, username, api_shared_key, schema=None, port=None, context=None,
                 default_headers=None, timeout=None):
        context = context or "reporting-api"
        schema = schema or "https"
        port = port or 80
        self.timeout = timeout or 30
        super(ReportingClient, self).__init__(hostname, context, username, api_shared_key, schema,
                                              port, default_headers)

    def _common_get(self, request_path, timeout=None, **kwargs):
        parameters = kwargs["parameters"] if "parameters" in kwargs else None
        timeout = timeout or self.timeout
        return self.get(request_path=request_path, params=parameters, timeout=timeout)

    def _common_post(self, request_path, body=None, timeout=None, **kwargs):
        timeout = timeout or self.timeout
        return self.post(request_path=request_path, data=json.dumps(body), timeout=timeout)

    def _common_put(self, request_path, body=None, timeout=None, **kwargs):
        timeout = timeout or self.timeout
        return self.put(request_path=request_path, data=json.dumps(body), timeout=timeout)

    def _common_delete(self, request_path, body=None, timeout=None, **kwargs):
        timeout = timeout or self.timeout
        return self.delete(request_path=request_path, data=json.dumps(body), timeout=timeout)

    def _make_body(self, params):
        """
        Makes params and body parameters for _send_request method.
        """
        if "timespan" in params:
            t_spam = params.pop("timespan")
            st_d, end_d = timespan(t_spam, timezone=self.TIMEZONE_DEFAULT)
            params["startDate"] = st_d
            params["endDate"] = end_d

        list_params = ["shortname", "requestedFields", "order", "sortField"]

        body_data = {param: value if param not in list_params else list(set(value)) if isinstance(value, list) else
        [value] for param, value in params.items()}

        return body_data

    def request(self, **kwargs):
        """
        Wrapper method to support general java-script approach
        """
        if not hasattr(self, kwargs['report']):
            raise AttributeError(f'Report {kwargs["report"]} not exist')
        report_name = kwargs.pop('report')
        return getattr(self, report_name)(**kwargs)

    def traffic_file_errors(self, **kwargs):
        """
        Retrieve originFileErrors data with filtering.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param urlLike`:  (optional) <str> - URL, WHERE err = 5xx (search implemented via ‘like’ statement; can be empty)
            :param urlEquals`:  (optional) <str> - URL, WHERE err = 5xx (search implemented via ‘equals’ statement; can be empty)
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField: (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "statuscodes/originFileErrors"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving originFileErrors data with filtering")
        return self._common_post(request_path=url_path, body=body)

    def traffic_bytes_per_request(self, **kwargs):
        """
        Retrieves bytesPerRequest data with filtering.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param range: (optional) <str> - Size range for filtering (like "0-512" or "32k-64k", etc.)
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField: (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "traffic/bytesPerRequest"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving bytesPerRequest data with filtering")
        return self._common_post(request_path=url_path, body=body)

    def traffic_file_types(self, **kwargs):
        """
        Retrieve fileTypes data with filtering.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - Datetime (first occurrence of the entry)
            :param endDate:  (optional) <int> - Datetime (last occurrence of the entry)
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param typeLike:  (optional) <str> - Type for filtering (search implemented via ‘like’ statement; can be empty)
            :param typeEquals:  (optional) <str> - Type for filtering (search implemented via ‘equals’ statement; can be empty)
            :param order:  (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField:  (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit:  (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset:  (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "traffic/fileTypes"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving fileTypes data with filtering")
        return self._common_post(request_path=url_path, body=body)

    def traffic_missing_files(self, **kwargs):
        """
        Retrieve originMissingFiles data with filtering.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - Datetime (first occurrence of the entry)
            :param endDate:  (optional) <int> - Datetime (last occurrence of the entry)
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param urlLike:  (optional) <str> - URL, WHERE err = 404 (search implemented via ‘like’ statement; can be empty)
            :param urlEquals:  (optional) <str> - URL, WHERE err = 404 (search implemented via ‘equals’ statement; can be empty)
            :param order:  (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField:  (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit:  (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset:  (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "statuscodes/originMissingFiles"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving originMissingFiles data with filtering")
        return self._common_post(request_path=url_path, body=body)

    def traffic_referers(self, **kwargs):
        """
        Retrieve referrerURLs data with filtering.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - Datetime (first occurrence of the entry)
            :param endDate:  (optional) <int> - Datetime (last occurrence of the entry)
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param refUrlLike`:  (optional) <str> - Referrer URL (search is implemented via ‘like’ statement; can be empty)
            :param refUrlEquals`:  (optional) <str> - Referrer URL (search is implemented via ‘equals’ statement; can be empty)
            :param order:  (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField:  (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit:  (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset:  (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "traffic/referrerURLs"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving referrerURLs data with filtering")
        return self._common_post(request_path=url_path, body=body)

    def traffic_urls(self, **kwargs):
        """
        Retrieve traffic urls data with filtering.
        
            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - Datetime (first occurrence of the entry)
            :param endDate:  (optional) <int> - Datetime (last occurrence of the entry)
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param urlLike:  (optional) <str> - URL (search is implemented via ‘like’ statement; can be empty)
            :param urlEquals:  (optional) <str> - URL (search is implemented via ‘equals’ statement; can be empty)
            :param order:  (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField:  (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit:  (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset:  (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "traffic/urls"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving traffic urls data with filtering")
        return self._common_post(request_path=url_path, body=body)

    def traffic_user_agents(self, **kwargs):
        """
        Retrieve traffic urls data with filtering.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - Datetime (first occurrence of the entry)
            :param endDate:  (optional) <int> - Datetime (last occurrence of the entry)
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param userAgentLike (optional) <str> implement like matching
            :param userAgentEquals (optional) <str> implement equals matching
            :param order:  (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param sortField:  (optional) <list> - Field used for sorting (Note: Should be among requested fields)
            :param limit:  (optional) <int> - Indicates how many results should be present in the response (used for pagination)
            :param offset:  (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
        """
        url_path = "traffic/userAgents"
        body = self._make_body(kwargs)
        self.logger.debug("Retrieving traffic user agents")
        return self._common_post(request_path=url_path, body=body)
