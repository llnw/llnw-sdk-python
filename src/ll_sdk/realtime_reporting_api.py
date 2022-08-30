#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from sdk.base_client import BaseRestReportingClient
from sdk.utils.reporting_api_helper.time_utils import _timespan as timespan

__all__ = ['RealtimeReportingClient']
__docformat__ = 'restructuredtext'


class RealtimeReportingClient(BaseRestReportingClient):
    """
    RealtimeReportingClient client
    """
    SERVICE_HTTP = 'HTTP'
    SERVICE_HTTPS = 'HTTPS'
    SERVICE_HLS = 'HLS'
    SERVICE_HDS = 'HDS'
    SERVICE_MSS = 'MSS'
    SERVICE_DASH = 'DASH'

    REQUESTED_FIELDS_SHORTNAME = 'shortname'
    REQUESTED_FIELDS_DATETIME = 'datetime'
    REQUESTED_FIELDS_SERVICE = 'service'
    REQUESTED_FIELDS_TOTAL_BYTES = 'totalBytes'
    REQUESTED_FIELDS_OUTBYTES = 'outBytes'
    REQUESTED_FIELDS_INBYTES = 'inBytes'
    REQUESTED_FIELDS_TOTAL_BITS_PER_SEC = 'totalBitsPerSec'
    REQUESTED_FIELDS_BITS_PER_SECONDS = 'outBitsPerSec'
    REQUESTED_FIELDS_INBITS_PER_SECONDS = 'inBitsPerSec'
    REQUESTED_FIELDS_TOTAL_REQUESTS = 'totalRequests'
    REQUESTED_FIELDS_OUTREQUESTS = 'outRequests'
    REQUESTED_FIELDS_INREQUESTS = 'inRequests'
    REQUESTED_FIELDS_TOTAL_REQUESTS_PER_SEC = 'totalRequestsPerSec'
    REQUESTED_FIELDS_OUTREQUESTS_PER_SEC = 'outRequestsPerSec'
    REQUESTED_FIELDS_INREQUESTS_PER_SEC = 'inRequestsPerSec'
    REQUESTED_FIELDS_EFFICIENCY_REQUESTS = 'efficiencyRequests'
    REQUESTED_FIELDS_EFFICIENCY_BYTES = 'efficiencyBytes'
    REQUESTED_FIELDS_DNS_POLICY_FQDN = 'policyFQDN'
    REQUESTED_FIELDS_DNS_REQUESTS = 'requests'
    REQUESTED_FIELDS_DNS_BYTES = 'bytes'

    REQUESTED_FIELDS_STREAM_NAME = 'streamName'
    REQUESTED_FIELDS_CONNECTION_PROTOCOL = 'connectionProtocol'
    REQUESTED_FIELDS_DURATION = 'duration'
    REQUESTED_FIELDS_LOST_PACKETS = 'lostPackets'
    REQUESTED_FIELDS_AVG_CONNECTION_DURATION = 'avgConnectionDuration'

    REQUESTED_FIELDS_STATEID = 'stateId'
    REQUESTED_FIELDS_STATE = 'state'
    REQUESTED_FIELDS_STATE_ISO = 'stateISO'
    REQUESTED_FIELDS_COUNTRYID = 'countryId'
    REQUESTED_FIELDS_COUNTRY = 'country'
    REQUESTED_FIELDS_COUNTRY_ISO = 'countryISO'
    REQUESTED_FIELDS_CONTINENTID = 'continentId'
    REQUESTED_FIELDS_CONTINENT = 'continent'
    REQUESTED_FIELDS_CONTINENT_ISO = 'continentISO'

    REQUESTED_FIELDS_POLICY_ID = 'policyId'
    REQUESTED_FIELDS_UNIQUE_BYTES = 'uniqueBytes'
    REQUESTED_FIELDS_UNIQUE_OBJECTS = 'uniqueObjects'

    REQUESTED_FIELDS_CACHE_CODE = 'cacheCode'
    REQUESTED_FIELDS_STATUS_CODE = 'statusCode'
    REQUESTED_FIELDS_REQUEST_RESPONSE_TYPE = 'requestResponseType'

    GRANULARITY_ONE_MINUTE = 'ONE_MINUTE'
    GRANULARITY_FIVE_MINUTES = 'FIVE_MINUTES'
    GRANULARITY_HOUR = 'HOUR'
    GRANULARITY_DAY = 'DAY'

    SERVICES = [SERVICE_HTTP, SERVICE_HTTPS, SERVICE_HLS, SERVICE_HDS, SERVICE_MSS, SERVICE_DASH]

    TRAFFIC_GRANULARITIES = [GRANULARITY_FIVE_MINUTES, GRANULARITY_HOUR, GRANULARITY_DAY]

    TRAFFIC_REQUESTED_FIELDS = [REQUESTED_FIELDS_SHORTNAME, REQUESTED_FIELDS_DATETIME, REQUESTED_FIELDS_TOTAL_BYTES,
                                REQUESTED_FIELDS_OUTBYTES, REQUESTED_FIELDS_INBYTES,
                                REQUESTED_FIELDS_TOTAL_BITS_PER_SEC,
                                REQUESTED_FIELDS_BITS_PER_SECONDS, REQUESTED_FIELDS_INBITS_PER_SECONDS,
                                REQUESTED_FIELDS_TOTAL_REQUESTS, REQUESTED_FIELDS_OUTREQUESTS,
                                REQUESTED_FIELDS_INREQUESTS,
                                REQUESTED_FIELDS_TOTAL_REQUESTS_PER_SEC, REQUESTED_FIELDS_OUTREQUESTS_PER_SEC,
                                REQUESTED_FIELDS_INREQUESTS_PER_SEC, REQUESTED_FIELDS_EFFICIENCY_REQUESTS,
                                REQUESTED_FIELDS_EFFICIENCY_BYTES]

    DNS_REQUESTED_FIELDS = [REQUESTED_FIELDS_DATETIME, REQUESTED_FIELDS_SHORTNAME, REQUESTED_FIELDS_DNS_POLICY_FQDN,
                            REQUESTED_FIELDS_DNS_REQUESTS, REQUESTED_FIELDS_DNS_BYTES]

    REALTIME_STREAMING_REQUESTED_FIELDS = [
        REQUESTED_FIELDS_DATETIME, REQUESTED_FIELDS_COUNTRYID, REQUESTED_FIELDS_COUNTRY, REQUESTED_FIELDS_COUNTRY_ISO,
        REQUESTED_FIELDS_CONTINENTID, REQUESTED_FIELDS_CONTINENT, REQUESTED_FIELDS_CONTINENT_ISO,
        REQUESTED_FIELDS_SHORTNAME, REQUESTED_FIELDS_STREAM_NAME, REQUESTED_FIELDS_CONNECTION_PROTOCOL,
        REQUESTED_FIELDS_DURATION, REQUESTED_FIELDS_LOST_PACKETS, REQUESTED_FIELDS_DNS_BYTES,
        REQUESTED_FIELDS_DNS_REQUESTS,
        REQUESTED_FIELDS_AVG_CONNECTION_DURATION]

    STORAGE_REQUESTED_FIELDS = [REQUESTED_FIELDS_DATETIME, REQUESTED_FIELDS_SHORTNAME, REQUESTED_FIELDS_POLICY_ID,
                                REQUESTED_FIELDS_UNIQUE_BYTES, REQUESTED_FIELDS_UNIQUE_OBJECTS]

    GEO_REQUESTED_FIELDS = [REQUESTED_FIELDS_STATEID, REQUESTED_FIELDS_STATE, REQUESTED_FIELDS_STATE_ISO,
                            REQUESTED_FIELDS_COUNTRYID, REQUESTED_FIELDS_COUNTRY, REQUESTED_FIELDS_COUNTRY_ISO,
                            REQUESTED_FIELDS_CONTINENTID, REQUESTED_FIELDS_CONTINENT, REQUESTED_FIELDS_CONTINENT_ISO]

    GEO_METRIC_REQUESTED_FIELDS = [REQUESTED_FIELDS_OUTREQUESTS, REQUESTED_FIELDS_INBYTES,
                                   REQUESTED_FIELDS_TOTAL_REQUESTS_PER_SEC, REQUESTED_FIELDS_TOTAL_REQUESTS,
                                   REQUESTED_FIELDS_INBITS_PER_SECONDS, REQUESTED_FIELDS_OUTREQUESTS_PER_SEC,
                                   REQUESTED_FIELDS_INREQUESTS_PER_SEC, REQUESTED_FIELDS_OUTBYTES,
                                   REQUESTED_FIELDS_TOTAL_BITS_PER_SEC, REQUESTED_FIELDS_INREQUESTS,
                                   REQUESTED_FIELDS_TOTAL_BYTES, REQUESTED_FIELDS_BITS_PER_SECONDS]

    LIVESTATS_REQUESTED_FIELDS = [REQUESTED_FIELDS_DATETIME, REQUESTED_FIELDS_INREQUESTS, REQUESTED_FIELDS_OUTREQUESTS,
                                  REQUESTED_FIELDS_TOTAL_REQUESTS, REQUESTED_FIELDS_INBYTES,
                                  REQUESTED_FIELDS_OUTBYTES, REQUESTED_FIELDS_TOTAL_BYTES,
                                  REQUESTED_FIELDS_INBITS_PER_SECONDS, REQUESTED_FIELDS_BITS_PER_SECONDS,
                                  REQUESTED_FIELDS_TOTAL_BITS_PER_SEC]

    STATUSCODES_REQUESTED_FIELDS = [REQUESTED_FIELDS_CACHE_CODE, REQUESTED_FIELDS_INBYTES, REQUESTED_FIELDS_OUTBYTES,
                                    REQUESTED_FIELDS_SERVICE, REQUESTED_FIELDS_INREQUESTS, REQUESTED_FIELDS_OUTREQUESTS,
                                    REQUESTED_FIELDS_REQUEST_RESPONSE_TYPE, REQUESTED_FIELDS_DATETIME,
                                    REQUESTED_FIELDS_SHORTNAME, REQUESTED_FIELDS_STATUS_CODE]

    def __init__(self, hostname, username, api_shared_key, schema=None, port=None, context=None,
                 default_headers=None, timeout=None, timezone=None):
        context = context or 'realtime-reporting-api'
        schema = schema or 'https'
        port = port or '80'
        self.timeout = timeout or 30
        self.timezone = timezone or self.TIMEZONE_DEFAULT
        super(RealtimeReportingClient, self).__init__(hostname, context, username, api_shared_key, schema,
                                                      port, default_headers)

    def _common_get(self, request_path, timeout=None, **kwargs):
        parameters = kwargs['parameters'] if 'parameters' in kwargs else None
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
        if 'timespan' in params:
            t_spam = params.pop('timespan')
            st_d, end_d = timespan(t_spam, timezone=self.timezone)
            params['startDate'] = st_d
            params['endDate'] = end_d

        list_params = ['shortname', 'service', 'dataSegmentId', 'requestedFields', 'stateId', 'countryId',
                       'continentId', 'cacheCode', 'requestResponseType']
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

    def health_check(self):
        path = 'health/check'
        self.logger.debug("Perform health check")
        return self._common_get(path)

    # -------------------- Traffic   -------------------- #

    def traffic(self, **kwargs):
        """
        Send request to Realtime Reporting API for traffic report

            :param shortname: (required) <list> - List of shortnames
            :param service: (required) <list> - list of services
            :param datasegmentId: (required) <list> - list if present than do not specify shortname and service
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param sortField: (optional) <>list> -  Field used for sorting. Should be among requested fields.
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)
        """
        self.logger.debug(f"Get basic traffic usage data")
        url_path = 'traffic'
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def traffic_retentions(self):
        """
        Get possible retentions '/traffic' per each granularity

            :return: dictionary with granularities and corresponding retentions (in seconds)
        """
        url_path = 'traffic/retentions'
        self.logger.debug("Get possible retentions '/traffic' per each granularity")
        return self._common_get(url_path)

    # -------------------- DNS  -------------------- #

    def dns(self, **kwargs):
        """
        Send request to Realtime Reporting API for DNS report.

            :param shortname: (required) <list> - List of shortnames
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param granularity:
            :param policyFQDN:
            :param sortField: (optional) <>list> -  Field used for sorting. Should be among requested fields.
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)

        """
        self.logger.debug(f"Get RealTime DNS data")
        url_path = 'dns'
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def dns_policies(self, **kwargs):
        """
        Send request with specified method to Realtime Reporting API for DNS FQDN policies.

            :param shortname: (required) <list> - List of shortnames
            :param startDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.

        """
        url_path = 'dns/policies'
        self.logger.debug(f"Get RealTime DNS Policies")
        body = self._make_body(kwargs)
        return self._common_get(request_path=url_path, parameters=body)

    def dns_retentions(self):
        """
        Get possible retentions for '/dns' per each granularity

            :return: dictionary with granularities and corresponding retentions (in seconds)
        """
        url_path = 'dns/retentions'
        self.logger.debug("Get possible retentions for '/dns' per each granularity")
        return self._common_get(url_path)

    # -------------------- realtime streaming  -------------------- #

    def realtimestreaming(self, **kwargs):
        """
        Realtime Streaming report endpoint ('realtimestreaming?params')

            :param shortname: (required) <list> - List of shortnames
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param streamName: (optional).
            :param connectionProtocol: (optional).
            :param sortField: (optional) <>list> -  Field used for sorting. Should be among requested fields.
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)

        """
        url_path = 'realtimestreaming'
        self.logger.debug(f"Get Realtime Streaming report data")
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def realtimestreaming_streams(self, **kwargs):
        """
        Realtime Streaming metadata endpoint - Stream names ('realtimestreaming/streams?params')

            :param shortname: (required) <list> - List of shortnames
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param startDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
        """
        url_path = 'realtimestreaming/streams'
        self.logger.debug("Get list of stream names")
        return self._common_get(url_path, parameters=kwargs)

    def realtimestreaming_protocols(self, **kwargs):
        """
        Realtime Streaming metadata endpoint - Protocols ('realtimestreaming/protocols?params')

            :param shortname: (required) <list> - List of shortnames
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param startDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
        """
        url_path = 'realtimestreaming/protocols'
        self.logger.debug("Get list of protocols")
        return self._common_get(url_path, parameters=kwargs)

    def realtimestreaming_retentions(self):
        """
        Get possible retentions for 'realtimestreaming' per each granularity
        """
        url_path = 'realtimestreaming/retentions'
        self.logger.debug("Get possible retentions for 'realtimestreaming' per each granularity")
        return self._common_get(url_path)

    # -------------------- origin storage  -------------------- #

    def storage(self, **kwargs):
        """
        Send request to Realtime Reporting API for storage report.

            :param shortname: (required) <list> - List of shortnames
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param sortField: (optional) <>list> -  Field used for sorting. Should be among requested fields.
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)
        """
        self.logger.debug(f"Get basic storage data")
        url_path = 'storage'
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def storage_policies(self, **kwargs):
        """
        Send request with specified method to Realtime Reporting API for storage policies.

            :param shortname: (required) <list> - List of shortnames
            :param startDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
        """
        self.logger.debug(f"Get storage policies data")
        url_path = 'storage/policies'
        body = self._make_body(kwargs)
        return self._common_get(request_path=url_path, parameters=body)

    def storage_retentions(self):
        """
        Send request with specified method to Realtime Reporting API for strage retentions.
        """
        url_path = 'storage/retentions'
        self.logger.debug("Get information about storage data retentions per each granularity")
        return self._common_get(url_path)

    # -------------------- traffic geo  -------------------- #

    def traffic_geo(self, **kwargs):
        """
        Send request with specified method to Realtime Reporting API for geo report.

            :param shortname: (required) <list> - List of shortnames
            :param service: (required) <list> - list of services
            :param datasegmentId: (required) <list> - list if present than do not specify shortname and service
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param stateId: (optional)
            :param countryId: (optional)
            :param continentId: (optional)
            :param sortField: (optional) <>list> -  Field used for sorting. Should be among requested fields.
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)
        """
        self.logger.debug(f"Get basic Geo usage data")
        url_path = 'traffic/geo'
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def traffic_geo_retentions(self):
        """
        Get possible retentions for '/traffic/geo' per each granularity

            :return: dictionary with granularities and corresponding retentions (in seconds)
        """
        url_path = 'traffic/geo/retentions'
        self.logger.debug("Get possible retentions for '/traffic/geo' per each granularity")
        return self._common_get(url_path)

    def geo_continents(self):
        """
        Returns continents metadata

            :return: dict with id, iso, name data for each continent
        """
        path = 'geo/continents'
        self.logger.debug("Get Geo continents IDs")
        return self._common_get(path)

    def geo_countries(self, continent_id=None):
        """
        Returns countries metadata

            :param continent_id: (optional) <int> continent ID (1,2,3,5,6 or 7)
            :return: dict with id, iso, name data for each country on <continent>
        """
        path = 'geo/countries'
        params = None
        self.logger.debug("Get Geo countries IDs")
        if continent_id:
            params = {'continentId': continent_id}
        return self._common_get(path, parameters=params)

    def geo_states(self, country_id):
        """
        Returns states metadata
        Note: API supports state level only for USA (countryId=1) and Canada (countryId=2)

            :param country_id: (required) <int>  country ID (1 or 2)
            :return: dict with id, iso, name data for each state that belong to USA/Canada
        """
        path = 'geo/states'
        self.logger.debug("Get Geo states metadata")
        params = {'countryId': country_id}
        return self._common_get(path, parameters=params)

    # -------------------- Live stats  -------------------- #

    def traffic_livestats(self, **kwargs):
        """
        Live Stats report endpoint ('traffic/livestats?params')

            :param shortname: (required) <list> - List of shortnames
            :param service: (required) <list> - list of services
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param sortField: (optional) <>list> -  Field used for sorting. Should be among requested fields.
            :param order: (optional) <list> - Ordering specification, e.g. ASC or DESC
            :param offset: (optional) <int> - Tells how many first results to skip (Note: Cannot be used without order)
            :param limit: (optional) <int> - Indicates how many results should be present in the response (used for pagination)
        """
        url_path = 'traffic/livestats'
        self.logger.debug("Get live stats report data")
        kwargs['granularity'] = self.GRANULARITY_ONE_MINUTE
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def traffic_livestats_services(self, **kwargs):
        """
        Get list of services (LS).

            :param shortname: (required) <list> - List of shortnames
            :param startDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
        """
        url_path = 'traffic/livestats/services'
        self.logger.debug(f"Get list of services (LiveStats)")
        body = self._make_body(kwargs)
        return self._common_get(request_path=url_path, parameters=body)

    def traffic_livestats_retentions(self):
        """
        Get possible retentions for 'traffic/livestats' per each granularity

            :return: dictionary with granularities and corresponding retentions (in seconds)
        """
        url_path = 'traffic/livestats/retentions'
        self.logger.debug("Get possible retentions for 'traffic/livestats' per each granularity")
        return self._common_get(url_path)

    # -------------------- Status Codes  -------------------- #

    def traffic_statuscodes(self, **kwargs):
        """
        Status Codes report endpoint ('traffic/statuscodes?params')

            :param shortname: (required) <list> - List of shortnames
            :param granularity: (required) Hit _retentions method to get allowed granularity
            :param requestedFields: (required) <list> - List of result fields to be retrieved
            :param startDate: (required) <int> - start/endDate have to be within retention policy for specified granularity
            :param endDate: (optional) <int> - start/endDate have to be within retention policy for specified granularity
            :param timespan: (optional) <str>  -  start/endDate preset if present startDate and endDate will be ignored.
            :param service: (optional)
            :param cacheCode: (optional)
            :param statusCode: (optional)
            :param requestResponseType: (optional)
        """
        self.logger.debug(f"Get status codes report data,)")
        url_path = 'traffic/statuscodes'
        body = self._make_body(kwargs)
        return self._common_post(request_path=url_path, body=body)

    def traffic_statuscodes_cachecodes(self, **kwargs):
        """
        Cache codes metadata endpoint ('traffic/statuscodes/cachecodes?params').
        Returns fixed list of cache codes.

            :param shortname: (required)
            :return: ['MISS', 'HIT', 'OTHER', 'REDIRECT']
        """
        url_path = 'traffic/statuscodes/cachecodes'
        self.logger.debug(f"Get list of cache codes")
        body = self._make_body(kwargs)
        return self._common_get(request_path=url_path, parameters=body)

    def traffic_statuscodes_requestresponsetype(self, **kwargs):
        """
        Request Response Types metadata endpoint ('traffic/statuscodes/requestresponsetype?params').
        Returns fixed list of request response types.

            :param shortname: (required) <list> - List of shortnames
            :return: ['IF_MODIFIED_SINCE', 'STANDARD', 'REFRESH', 'NEGATIVELY_CACHED']
        """
        url_path = 'traffic/statuscodes/requestresponsetype'
        self.logger.debug(f"Get list of request-response types")
        body = self._make_body(kwargs)
        return self._common_get(request_path=url_path, parameters=body)

    def traffic_statuscodes_services(self, **kwargs):
        """
        Get list of services (SC).

            :param shortname: (required) <list> - List of shortnames
            :return: list of services, like: [ "HTTP", "HTTPS", "HLS" ]
        """
        url_path = 'traffic/statuscodes' + '/services'
        self.logger.debug(f"Get list of services (StatusCodes)")
        body = self._make_body(kwargs)
        return self._common_get(request_path=url_path, parameters=body)

    def traffic_statuscodes_retentions(self):
        """
        Get possible retentions for '/traffic/statuscodes' per each granularity

            :return: dictionary with granularities and corresponding retentions (in seconds)
        """
        url_path = 'traffic/statuscodes/retentions'
        self.logger.debug("Get possible retentions for '/traffic/statuscodes' per each granularity")
        return self._common_get(url_path)
