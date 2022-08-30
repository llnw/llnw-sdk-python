#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from urllib.parse import parse_qs
from sdk.base_client import BaseRestAuthClient

__all__ = ['ConfigApiClient']
__docformat__ = 'restructuredtext'


class ConfigApiClient(BaseRestAuthClient):
    """
    Rest client for Limelight Public config-api
    """

    def __init__(self, hostname, username, api_shared_key, schema=None, port=None, context=None,
                 default_headers=None, timeout=None):
        context = context or 'config-api/v1'
        schema = schema or 'https'
        port = port or '80'
        self.timeout = timeout or 30
        super(ConfigApiClient, self).__init__(hostname, context, username, api_shared_key, schema,
                                              port, default_headers)

    def _common_get(self, request_path, timeout=None, **kwargs):
        parameters = {}
        timeout = timeout or self.timeout
        if 'size' in kwargs and kwargs['size'] is not None:
            parameters["size"] = str(kwargs['size'])
        if 'page' in kwargs and kwargs['page'] is not None:
            parameters["page"] = str(kwargs['page'])
        if 'limit' in kwargs and kwargs['limit'] is not None:
            parameters["limit"] = str(kwargs['limit'])
        if 'parameters' in kwargs and kwargs['parameters'] is not None:
            parameters.update(parse_qs(kwargs['parameters']))
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

    # -------------------- Config API  -------------------- #

    def request(self, **kwargs):
        """
        General wrapper method
            :param kwargs: list of argument from action method
            action
            type
            service
        """
        if not hasattr(self, kwargs['action']):
            raise AttributeError(f'action {kwargs["action"]} not exist')
        action = kwargs.pop('action')
        return getattr(self, action)(**kwargs)

    def request_js(self, **kwargs):
        """
        General wrapper method
            :param kwargs: list of argument from action method
        """
        _action = 'get'  # possible values - get, search, validate, create, update, delete
        # _type = 'instance' # profile(svcprof), instance(svcinst), option(option)
        _service = 'delivery'  # applicable only for deliver/httpsc,

        m_action = getattr(kwargs, 'action', _action)
        m_service = getattr(kwargs, 'service', _service)
        m_type = getattr(kwargs, 'type', None)

        if m_type is None:
            method_name = f'{m_action}_{m_service}'
        else:
            method_name = f'{m_action}_{m_service}_{m_type}'
        if not hasattr(self, method_name):
            raise AttributeError(f'action {method_name} not exist')

        return getattr(self, method_name)(**kwargs)

    # -------------------- Config API  -------------------- #

    def get_health_check(self):
        """
        Light way to check if API is alive.
        """
        self.logger.debug("Getting health/check for service Config API")
        request_path = 'health/check'
        return self._common_get(request_path)

    def get_status(self):
        """
        Check API status, version, etc.
        """
        self.logger.debug("Getting Config APIs Status")
        request_path = 'utils/status'
        return self._common_get(request_path)

    # -------------------- Content Delivery - Get Info -------------------- #

    def list_delivery_service_instances(self, shortname, size=None, page=None):
        """
        Retrieves the delivery configurations for the provided shortname

            :param shortname: str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int
        """
        self.logger.debug(f"Getting Delivery ServiceInstances for shortname [{shortname}]")
        request_path = f'svcinst/delivery/shortname/{shortname}'
        return self._common_get(request_path, size=size, page=page)

    def list_delivery_service_profiles(self, shortname, size=None, page=None):
        """
        Retrieves the delivery service profiles per the specified shortname.

            :param shortname: str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int
        """
        self.logger.debug(f"Getting Delivery ServiceProfiles for shortname [{shortname}]")
        request_path = f'svcprof/delivery/shortname/{shortname}'
        return self._common_get(request_path, size=size, page=page)

    def search_delivery_service_profiles(self, shortname, parameters=None, size=None, page=None):
        """
        Retrieves the delivery service profiles per the specified shortname per provided searching criteria.

            :param shortname: str
            :param parameters: (optional) Searching criteria (e.i. body.useCase=DownloadLargeFile) str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int
        """
        self.logger.debug(
            f"Searching Delivery ServiceProfile for shortname [{shortname}], criteria [{parameters}]")
        request_path = f'svcprof/delivery/shortname/{shortname}/search'
        return self._common_get(request_path, size=size, page=page, parameters=parameters)

    def search_delivery_service_instance(self, shortname, parameters=None, size=None, page=None):
        """
        Retrieves the delivery service instances per the specified shortname per provided searching criteria.

            :param shortname: str
            :param parameters: (optional) Searching criteria (e.i. body.useCase=DownloadLargeFile) str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int
        """
        self.logger.debug(
            f"Searching Delivery ServiceProfile for shortname [{shortname}], criteria [{parameters}]")
        request_path = f'svcinst/delivery/shortname/{shortname}/searchAuto'
        return self._common_get(request_path, size=size, page=page, parameters=parameters)

    def get_delivery_service_profiles(self, shortname, uuid):
        """
        Retrieves the delivery service profiles per the specified shortname by uuid.

            :param shortname: str
            :param uuid: str
        """
        self.logger.debug(f"Get Delivery ServiceProfile for shortname [{shortname}] by uuid [{uuid}]")
        request_path = f'svcprof/delivery/shortname/{shortname}/{uuid}'
        return self._common_get(request_path)

    def get_delivery_service_instance(self, uuid):
        """
        Retrieves the delivery service instance per the specified shortname by uuid.

            :param uuid: str
        """
        self.logger.debug(
            f"Get Delivery ServiceProfile by uuid [{uuid}]")
        request_path = f'svcinst/delivery/{uuid}'
        return self._common_get(request_path)

    def list_delivery_service_instance_version(self, shortname, uuid):
        """
        Retrieves the delivery service instance versions or specific version.

            :param shortname: str
            :param uuid: str
            :param version: int
        """
        self.logger.debug(f"Get Delivery ServiceProfile versions for shortname [{shortname}] by uuid [{uuid}]")
        request_path = f'svcinst/delivery/{uuid}/versions'
        return self._common_get(request_path)

    def get_delivery_service_instance_version(self, shortname, uuid, version):
        """
        Retrieves the delivery service instance versions or specific version.

            :param shortname: str
            :param uuid: str
            :param version: int
        """
        self.logger.debug(
            f"Get Delivery ServiceProfile version [{version}] for shortname [{shortname}] by uuid [{uuid}]")
        request_path = f'svcinst/delivery/{uuid}/versions/{version}'
        return self._common_get(request_path)

    def list_configuration_options(self, shortname, profile_name):
        """
        Retrieves the list of available configOptions for shortname per service profile (delivery or httpcs).

            :param shortnme: str
            :param profile_name: str
        """
        self.logger.debug(f"Getting available ConfigOption for shortname [{shortname}]")
        request_path = f'configoption/shortname/{shortname}/svcProf/{profile_name}'
        return self._common_get(request_path)

    # -------------------- Content Delivery - Make changes -------------------- #

    def validate_delivery_service_instance(self, delivery_config):
        """
        Validates the delivery service instance (without creating).

            :param delivery_config: json

            always return 200 code. Contains field 'Success': True/False

                     True - config valid and can be created.
                     False - config contain errors that will be specified in response body.
        """
        self.logger.debug("Validating delivery service instance config")
        request_path = 'svcinst/delivery/validate'
        return self._common_post(request_path, body=delivery_config)

    def create_delivery_service_instance(self, delivery_config):
        """
        Creates the delivery service instance

            :param delivery_config: json

        """
        self.logger.debug("Creating delivery service instance config")
        request_path = 'svcinst/delivery'
        return self._common_post(request_path, body=delivery_config)

    def update_delivery_service_instance(self, uuid, delivery_config):
        """
        Updates the delivery service instance (Full object update)

            :param uuid: str
            :param delivery_config: json

        """
        self.logger.debug(f"Updating delivery service instance with uuid [{uuid}]")
        request_path = f'svcinst/delivery/{uuid}'
        return self._common_put(request_path, body=delivery_config)

    def delete_delivery_service_instance(self, uuid):
        """
        Deletes the delivery service instance

            :param uuid: json
        """
        self.logger.debug(f"Deleting delivery service instance with uuid [{uuid}]")
        request_path = f'svcinst/delivery/{uuid}'
        return self._common_delete(request_path)

    def inherit_delivery_service_instance(self, config, parent_uuid):
        """
        Allows creates delivery service instance with inheritance from parent config

            :param config: json
            :param parent_uuid: uuid
        """
        self.logger.debug("Inheriting delivery service instance")
        request_path = f'svcinst/delivery/inheritance?parentId={parent_uuid}'
        return self._common_post(request_path, body=config)

    def rollback_delivery_service_instance(self, uuid, version):
        """
        Allows rollback config to a specific historical version

            :param uuid: uuid
            :param version: int
        :return:
        """
        self.logger.debug(f"Posting config rollback for service instance [{uuid}]")
        request_path = f'svcinst/delivery/{uuid}/rollbackTo/{version}'
        return self._common_post(request_path, body=None)

    def clone_delivery_service_instance(self, published_host, source_host, parent_uuid):
        """
        Allows clone configuration in correct waywith new published_host, source_host

            :param published_host: str
            :param source_host: str
            :param parent_uuid: uuid
        """
        config = self.get_delivery_service_instance(parent_uuid)
        if not config.status_code == 200:
            raise BaseException(config.json())
        config = config.json()
        del config['revision']
        del config['shortname']
        del config['status']
        del config['uuid']
        config['body']['sourceHostname'] = source_host
        config['body']['publishedHostname'] = published_host
        return self.inherit_delivery_service_instance(config, parent_uuid=parent_uuid)

    # -------------------- HTTP chunk streaming - Make changes -------------------- #

    def list_httpcs_service_instances(self, shortname, size=None, page=None):
        """
        Retrieves the httpcs configurations for the provided shortname

            :param shortname: str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int
        """
        self.logger.debug(f"Getting Delivery ServiceInstances for shortname [{shortname}]")
        request_path = f'svcinst/httpcs/shortname/{shortname}'
        return self._common_get(request_path, size=size, page=page)

    def list_httpcs_service_profiles(self, shortname, size=None, page=None):
        """
        Retrieves the httpcs service profiles per the specified shortname.

            :param shortname: str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int
        """
        self.logger.debug(f"Getting Delivery ServiceProfiles for shortname [{shortname}]")
        request_path = f'svcprof/httpcs/shortname/{shortname}'
        return self._common_get(request_path, size=size, page=page)

    def search_httpcs_service_profiles(self, shortname, parameters=None, size=None, page=None):
        """
        Retrieves the httpcs service profiles per the specified shortname per provided searching criteria.

            :param shortname: str
            :param parameters: (optional) Searching criteria (e.i. body.useCase=DownloadLargeFile) str
            :param size: (optional) Default 100. str
            :param page: (optional) Default is 1. str
        """
        self.logger.debug(
            f"Searching Delivery ServiceProfile for shortname [{shortname}], criteria [{parameters}]")
        request_path = f'svcprof/httpcs/shortname/{shortname}/search'
        return self._common_get(request_path, size=size, page=page, parameters=parameters)

    def search_httpcs_service_instance(self, shortname, parameters=None, size=None, page=None):
        """
        Retrieves the httpcs service instances per the specified shortname per provided searching criteria.

            :param shortname: str
            :param parameters: (optional) Searching criteria (e.i. body.useCase=DownloadLargeFile) str
            :param size: (optional) Default 100. str
            :param page: (optional) Default is 1. str
        """
        self.logger.debug(
            f"Searching Delivery ServiceProfile for shortname [{shortname}], criteria [{parameters}]")
        request_path = f'svcinst/httpcs/shortname/{shortname}/searchAuto'
        return self._common_get(request_path, size=size, page=page, parameters=parameters)

    def get_httpcs_service_profiles(self, shortname, uuid):
        """
        Retrieves the httpcs service profiles per the specified shortname by uuid.

            :param shortname: str
            :param uuid: str
        """
        self.logger.debug(f"Get Delivery ServiceProfile for shortname [{shortname}] by uuid [{uuid}]")
        request_path = f'svcprof/httpcs/shortname/{shortname}/{uuid}'
        return self._common_get(request_path)

    def get_httpcs_service_instance(self, uuid):
        """
        Retrieves the httpcs service instance per the specified shortname by uuid.

            :param uuid: str
        """
        self.logger.debug(
            f"Get Delivery ServiceProfile by uuid [{uuid}]")
        request_path = f'svcinst/httpcs/{uuid}'
        return self._common_get(request_path)

    def list_httpcs_service_instance_version(self, shortname, uuid):
        """
        Retrieves the httpcs service instance versions or specific version.

            :param shortname: str
            :param uuid: str
            :param version: int
        """
        self.logger.debug(f"Get Delivery ServiceProfile version(s) for shortname [{shortname}] by uuid [{uuid}]")
        request_path = f'svcinst/httpcs/{uuid}/versions'
        return self._common_get(request_path)

    def get_httpcs_service_instance_version(self, shortname, uuid, version):
        """
        Retrieves the httpcs service instance versions or specific version.

            :param shortname: str
            :param uuid: str
            :param version: int
        """
        self.logger.debug(
            f"Get Delivery ServiceProfile version [{version}] for shortname [{shortname}] by uuid [{uuid}]")
        request_path = f'svcinst/httpcs/{uuid}/versions/{version}'
        return self._common_get(request_path)

    # -------------------- Content Delivery - Make changes -------------------- #

    def validate_httpcs_service_instance(self, httpcs_config):
        """
        Validates the httpcs service instance (without creating).

            :param httpcs_config: json
            :return: always return 200 code. Contains field 'Success': True/False
                     True - config valid and can be created.
                     False - config contain errors that will be specified in response body.
        """
        self.logger.debug("Validating httpcs service instance config")
        request_path = 'svcinst/httpcs/validate'
        return self._common_post(request_path, body=httpcs_config)

    def create_httpcs_service_instance(self, httpcs_config):
        """
        Creates the httpcs service instance

            :param httpcs_config: json
        """
        self.logger.debug("Creating httpcs service instance config")
        request_path = 'svcinst/httpcs'
        return self._common_post(request_path, body=httpcs_config)

    def update_httpcs_service_instance(self, uuid, httpcs_config):
        """
        Updates the httpcs service instance (Full object update)

            :param uuid: str
            :param httpcs_config: json
        """
        self.logger.debug(f"Updating httpcs service instance with uuid [{uuid}]")
        request_path = f'svcinst/httpcs/{uuid}'
        return self._common_put(request_path, body=httpcs_config)

    def delete_httpcs_service_instance(self, uuid):
        """
        Deletes the httpcs service instance

            :param uuid: str
        """
        self.logger.debug(f"Deleting httpcs service instance with uuid [{uuid}]")
        request_path = f'svcinst/httpcs/{uuid}'
        return self._common_delete(request_path)

    def inherit_httpcs_service_instance(self, config, parent_uuid):
        """
        Allows creates httpcs service instance with inheritance from parent config

            :param config: json
            :param parent_uuid: str
        """
        self.logger.debug("Inheriting delivery service instance")
        request_path = f'svcinst/httpcs/inheritance?parentId={parent_uuid}'
        return self._common_post(request_path, body=config)

    def rollback_httpcs_service_instance(self, uuid, version):
        """
        Allows rollback config to a specific historical version

            :param uuid: str
            :param version: int
        """
        self.logger.debug(f"Posting config rollback for service instance [{uuid}]")
        request_path = f'svcinst/httpcs/{uuid}/rollbackTo/{version}'
        return self._common_post(request_path, body=None)

    def clone_httpcs_service_instance(self, published_host, source_host, parent_uuid):
        """
        Allows clone configuration in correct way with new published_host, source_host

            :param published_host: str
            :param source_host: str
            :param parent_uuid: str
        """
        config = self.get_httpcs_service_instance(parent_uuid)
        assert config.status_code == 200, 'An error occurs'
        config = config.json()
        del config['revision']
        del config['shortname']
        del config['status']
        del config['uuid']
        config['body']['httpcsSvcInstance']['sourceHostname'] = source_host
        config['body']['httpcsSvcInstance']['publishedHostname'] = published_host
        return self.inherit_httpcs_service_instance(config, parent_uuid=parent_uuid)

    # -------------------- Customer Certificates-------------------- #

    def list_customer_certificates(self, shortname, size=None, page=None):
        """
        Retrieves the customer SSL certificates for the provided shortname

            :param shortname: str
            :param size: (optional) Default 100. int
            :param page: (optional) Default is 1. int

        """
        self.logger.debug(f'Getting customer - [{shortname}] Certificates')
        request_path = f'customerCertificate/shortname/{shortname}'
        return self._common_get(request_path, size=size, page=page)

    def get_customer_certificate(self, uuid):
        """
        Retrieves the customer SSL certificate via UUID

            :param uuid: str
        """
        self.logger.debug(f'Getting customer: [{uuid}] Certificate')
        request_path = f'customerCertificate/{uuid}'
        return self._common_get(request_path)

    def create_customer_certificate(self, cert_config):
        """
        Creates the customer SSL certificate

            :param cert_config: json
        """
        self.logger.debug('Creating customer certificate')
        request_path = 'customerCertificate'
        return self._common_post(request_path, body=cert_config)

    def validate_customer_certificate(self, cert_config):
        """
        Validates the customer SSL certificate

            :param cert_config: json
        """
        self.logger.debug('Validating customer certificate')
        request_path = 'customerCertificate/validate'
        return self._common_post(request_path, body=cert_config)

    def update_customer_certificate(self, uuid, cert_config):
        """
        Updates the customer SSL certificate

            :param uuid: str
            :param cert_config: json
        """
        self.logger.debug(f'Updating customer Certificate with uuid [{uuid}]')
        request_path = f'customerCertificate/{uuid}'
        return self._common_put(request_path, body=cert_config)

    def delete_customer_certificate(self, uuid):
        """
        Deletes the customer SSL certificate

            :param uuid: str
        """
        self.logger.debug(f'Deleting customer Certificate with uuid [{uuid}]')
        request_path = f'customerCertificate/{uuid}'
        return self._common_delete(request_path)

    def list_customer_certificate_versions(self, uuid):
        """
        List of customer SSL certificate versions or specific historical version

            :param uuid: str
            :param version: int

        """
        self.logger.debug(f'Getting customer Certificate [{uuid}] versions')
        request_path = f'customerCertificate/{uuid}/versions'
        return self._common_get(request_path)

    def get_customer_certificate_versions(self, uuid, version):
        """
        List of customer SSL certificate versions or specific historical version

            :param uuid: str
            :param version: int

        """
        self.logger.debug(f'Getting customer Certificate [{uuid}] versions')
        request_path = f'customerCertificate/{uuid}/versions/{version}'
        return self._common_get(request_path)

    def publish_customer_certificate(self, uuid):
        """
        Publish customer SSL certificate to the LLNW CDN Edge

            :param uuid: str
        """
        self.logger.debug('Publishing customer Certificate')
        request_path = f'customerCertificate/{uuid}/publish'
        return self._common_put(request_path)

    def withdraw_customer_certificate(self, uuid):
        """
        Withdraw customer SSL certificate from the LLNW CDN Edge

            :param uuid: str
        """
        self.logger.debug('Withdrawing customer Certificate')
        request_path = f'customerCertificate/{uuid}/withdraw'
        return self._common_delete(request_path)

    # -------------------- edgeRules -------------------- #

    def list_edgerules(self, shortname):
        """
        Return list of EdgeRules per shortname

            :param shortname: str
        """
        self.logger.debug(f'Getting edgerules for shortname [{shortname}]')
        request_path = f'edgerules/shortname/{shortname}'
        return self._common_get(request_path)

    def get_edgerule(self, shortname, uuid):
        """
        Returns specific edgeRule

            :param shortname: str
            :param uuid: str
        """
        self.logger.debug('Getting edgerules for shortname [{shortname}]')
        request_path = f'edgerules/shortname/{shortname}/{uuid}'
        return self._common_get(request_path)

    # -------------------- Ipacc -------------------- #

    def list_customer_ipacc(self, shortname):
        """
        Retrieve list of all customer IP Access Control Configuration (IPACC)

            :param shortname: str
        """
        self.logger.debug(f'Getting IPACC for shortname [{shortname}]')
        request_path = f'ipaclist/shortname/{shortname}'
        return self._common_get(request_path)

    def search_customer_ipacc(self, shortname, parameters=None):
        """
        Search customer IP Access Control Configuration

            :param shortname: str
            :param parameters: str
        """
        self.logger.debug(f'Searching for IPACC for shortname [{shortname}]')
        request_path = f'ipaclist/shortname/{shortname}/search'
        return self._common_get(request_path, parameters=parameters)

    def get_customer_ipacc(self, uuid):
        """
        Retrieve specific customer IP Access Control Configuration

            :param uuid: str
        """
        self.logger.debug(f'Getting IPACC with UUID [{uuid}]')
        request_path = f'ipaclist/{uuid}'
        return self._common_get(request_path)

    def get_customer_ipacc_blocks(self, uuid):
        """
        Retrieve specific customer IP Access Control Configuration blocks

            :param uuid:
        """
        self.logger.debug(f'Getting IPACC with UUID [{uuid}]')
        request_path = f'ipaclist/{uuid}/blocks'
        return self._common_get(request_path)

    # -------------------- DNS -------------------- #
    def list_dns_zones(self, shortname):
        self.logger.debug(f'Getting DNS zones for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone'
        return self._common_get(request_path)

    def get_dns_zone(self, shortname, zone_id):
        self.logger.debug(f'Getting DNS zones for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone_id}'
        return self._common_get(request_path)

    def create_dns_resource(self, shortname, resource):
        self.logger.debug(f'Posting DNS resource for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource'
        return self._common_post(request_path, body=resource)

    def list_dns_resource(self, shortname, size=None):
        self.logger.debug(f'Getting DNS resources for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource'
        return self._common_get(request_path, limit=size)

    def get_dns_resource(self, shortname, resource_id):
        self.logger.debug(f'Getting DNS resources for shortname {shortname} and resource {resource_id}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}'
        return self._common_get(request_path)

    def update_dns_resource_by_id(self, shortname, resource_id, resource):
        self.logger.debug(f'Updating DNS resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}'
        return self._common_put(request_path, body=resource)

    def delete_dns_resource_by_id(self, shortname, resource_id):
        self.logger.debug(f'Deleting DNS resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}'
        return self._common_delete(request_path)

    def create_dns_resource_health_check(self, shortname, resource_id, health_check):
        self.logger.debug(f'Posting DNS health check for resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}/healthcheck'
        return self._common_post(request_path, body=health_check)

    def list_dns_resource_health_check(self, shortname, resource_id, size=None):
        self.logger.debug(f'List of DNS healthcheck for resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}/healthcheck'
        return self._common_get(request_path, limit=size)

    def get_dns_resource_health_check(self, shortname, resource_id, health_check_id):
        self.logger.debug(f'Getting DNS healthcheck for resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}/healthcheck/{health_check_id}'
        return self._common_get(request_path)

    def update_dns_resource_health_check_by_id(self, shortname, resource_id, health_check_id, health_check):
        self.logger.debug(f'Updating DNS healthcheck with id {health_check_id} for resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}/healthcheck/{health_check_id}'
        return self._common_put(request_path, body=health_check)

    def delete_dns_resource_health_check_by_id(self, shortname, resource_id, health_check_id):
        self.logger.debug(f'Deleting DNS healthcheck with id {health_check_id} for resource with id {resource_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/resource/{resource_id}/healthcheck/{health_check_id}'
        return self._common_delete(request_path)

    def create_dns_failover(self, shortname, zone, failover):
        self.logger.debug(f'Posting DNS failover for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover'
        return self._common_post(request_path, body=failover)

    def list_dns_failover(self, shortname, zone, size=None):
        self.logger.debug(f'List DNS failover for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover'
        return self._common_get(request_path, limit=size)

    def get_dns_failover(self, shortname, zone, failover_id):
        self.logger.debug(f'Getting DNS failover for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover/{failover_id}'
        return self._common_get(request_path)

    def update_dns_failover_by_id(self, shortname, zone, failover_id, failover):
        self.logger.debug(f'Updating DNS failover with id {failover_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover/{failover_id}'
        return self._common_put(request_path, body=failover)

    def delete_dns_failover_by_id(self, shortname, zone, failover_id):
        self.logger.debug(f'Deleting DNS failover with id {failover_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover/{failover_id}'
        return self._common_delete(request_path)

    def create_dns_resource_to_failover(self, shortname, zone, failover_id, resource):
        self.logger.debug(f'Posting DNS resource to failover with id {failover_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover/{failover_id}/resource'
        return self._common_post(request_path, body=resource)

    def get_dns_resource_to_failover(self, shortname, zone, failover_id):
        self.logger.debug(f'Getting DNS resources from failover with id {failover_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover/{failover_id}/resource'
        return self._common_get(request_path)

    def delete_dns_resource_to_failover(self, shortname, zone, failover_id, resource_id):
        self.logger.debug(f'Deleting DNS resource with id {resource_id} from '
                          f'failover with id {failover_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/failover/{failover_id}/resource/{resource_id}'
        return self._common_delete(request_path)

    def list_dns_rule(self, shortname, size=None):
        self.logger.debug(f'List DNS rule for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/rule'
        return self._common_get(request_path, limit=size)

    def get_dns_rule(self, shortname, rule_id=None):
        self.logger.debug(f'Getting DNS rule for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/rule/{rule_id}'
        return self._common_get(request_path)

    def create_dns_rule(self, shortname, rule):
        self.logger.debug(f'Posting DNS rule for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/rule'
        return self._common_post(request_path, body=rule)

    def update_dns_rule_by_id(self, shortname, rule_id, rule):
        self.logger.debug(f'Updating DNS rule with id {rule_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/rule/{rule_id}'
        return self._common_put(request_path, body=rule)

    def delete_dns_rule_by_id(self, shortname, rule_id):
        self.logger.debug(f'Deleting DNS rule with id {rule_id} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/rule/{rule_id}'
        return self._common_delete(request_path)

    def create_dns_director_policy(self, shortname, zone, dir_policy):
        self.logger.debug(f'Posting DNS director policy for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/directorpolicy'
        return self._common_post(request_path, body=dir_policy)

    def list_dns_director_policy(self, shortname, zone):
        self.logger.debug(f'List of DNS director policy for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/directorpolicy'
        return self._common_get(request_path)

    def get_dns_director_policy(self, shortname, zone, dir_policy_id):
        self.logger.debug(f'Getting DNS director policy for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/directorpolicy/{dir_policy_id}'
        return self._common_get(request_path)

    def update_dns_director_policy_by_id(self, shortname, zone, dir_policy_id, dir_policy):
        self.logger.debug(f'Updating DNS director policy with id {dir_policy_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/directorpolicy/{dir_policy_id}'
        return self._common_put(request_path, body=dir_policy)

    def delete_dns_director_policy_by_id(self, shortname, zone, dir_policy_id):
        self.logger.debug('Deleting DNS director policy with id {dir_policy_id} for zone {zone} for shortname {shortname}')
        request_path = f'epdns/shortname/{shortname}/zone/{zone}/directorpolicy/{dir_policy_id}'
        return self._common_delete(request_path)

    def get_dns_health_checks(self):
        self.logger.debug('Getting DNS health checks')
        request_path = 'epdns/healthcheck'
        return self._common_get(request_path)

    def list_dns_job(self, size=None):
        self.logger.debug('List of DNS job status')
        request_path = 'epdns/job'
        return self._common_get(request_path, limit=size)

    def get_dns_job(self, job_id=None):
        self.logger.debug('Getting DNS job status')
        request_path = f'epdns/job/{job_id}'
        return self._common_get(request_path)

    def get_dns_country_geo_metadata(self):
        self.logger.debug('Getting geo metadata for countries')
        request_path = 'metadata/geo/countries'
        return self._common_get(request_path)

    def get_dns_state_geo_metadata(self, country_id):
        self.logger.debug(f'Getting geo metadata for states from county with id: {country_id}')
        request_path = f'metadata/geo/countries/{country_id}/states'
        return self._common_get(request_path)

    # -------------------- LDS -------------------- #

    def list_lds(self, shortname, size=None, page=None):
        """
        Retrieve list of customer lds configs

            :param shortname: str
            :param size: int
            :param page: int
        """
        self.logger.debug(f"Getting LDS for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/config'
        return self._common_get(request_path, size=size, page=page)

    def get_lds(self, shortname, uuid, size=None, page=None):
        """
        Retrieve customer lds config via UUID

            :param shortname:
            :param uuid:
            :param size:
            :param page:
        """

        self.logger.debug(f"Getting LDS for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/config/{uuid}'
        return self._common_get(request_path, size=size, page=page)

    def validate_lds(self, shortname, config):
        """
        Validates the lds config (without creating)

            :param shortname:
            :param config:

        """
        self.logger.debug(f"Validating LDS for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/config/validate'
        return self._common_post(request_path, body=config)

    def create_lds(self, shortname, config):
        """
        Creates lds configuration

            :param shortname:
            :param config:
        """
        self.logger.debug(f"Posting LDS for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/config'
        return self._common_post(request_path, body=config)

    def update_lds(self, shortname, uuid, config):
        """
        Updates lds configuration. Full update

        :param shortname: str
        :param uuid: str
        :param config: json
        """
        self.logger.debug(f"Updating LDS with uuid [{uuid}] for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/config/{uuid}'
        return self._common_put(request_path, body=config)

    def delete_lds(self, shortname, uuid):
        """
        Delete lds configuration

            :param shortname:
            :param uuid:
        """
        self.logger.debug(f"Deleting LDS with uuid [{uuid}] for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/config/{uuid}'
        return self._common_delete(request_path)

    def list_lds_fields(self, shortname):
        """
        Retrieves available lds fields

            :param shortname:
        """
        self.logger.debug(f"Getting LDS Fields for shortname [{shortname}]")
        request_path = f'lds/shortname/{shortname}/field'
        return self._common_get(request_path)

    def list_lds_compression_type(self):
        """
        Retrieves available lds compression types
        """

        self.logger.debug("Getting allowed LDS compression types")
        request_path = 'lds/compression-type'
        return self._common_get(request_path)

    def list_lds_storage_location(self):
        """
        Retrieves available lds storage location
        """
        self.logger.debug("Getting allowed LDS storage locations")
        request_path = 'lds/storage-location'
        return self._common_get(request_path)

    # -------------------- Video Live Schedule  -------------------- #

    def list_live_video_schedule(self, shortname):
        """

            :param shortname:
        """
        self.logger.debug(f"Getting all live video schedules for [{shortname}]")
        request_path = f'live/recording/shortname/{shortname}/schedules'
        return self._common_get(request_path)

    def get_live_video_schedule(self, shortname, schedule_id):
        """

            :param shortname:
            :param schedule_id:
        """

        self.logger.debug(f"Getting live video schedule [{schedule_id}] for [{shortname}]")
        request_path = f'live/recording/shortname/{shortname}/schedules/{schedule_id}'
        return self._common_get(request_path)

    def create_live_video_schedule(self, shortname, config):
        """

            :param shortname:
            :param config:
        """
        self.logger.debug(f"Creating live video schedules for [{shortname}]")
        request_path = f'live/recording/shortname/{shortname}/schedules'
        return self._common_post(request_path, body=config)

    def update_live_video_schedule(self, shortname, schedule_id, config):
        """

            :param shortname:
            :param schedule_id:
            :param config:
        """
        self.logger.debug(f"Updating live video schedule [{schedule_id}] for [{shortname}]")
        request_path = f'live/recording/shortname/{shortname}/schedules/{schedule_id}'
        return self._common_put(request_path, body=config)

    def delete_live_video_schedule(self, shortname, schedule_id):
        """

            :param shortname:
            :param schedule_id:
        """
        self.logger.debug(f"Deleting live video schedule [{schedule_id}] for [{shortname}]")
        request_path = f'live/recording/shortname/{shortname}/schedules/{schedule_id}'
        return self._common_delete(request_path)

    # -------------------- Video Live Slots  -------------------- #

    def get_live_video_overview(self, shortname):
        """

            :param shortname:
        """
        self.logger.debug(f'Getting live video overview for [{shortname}]')
        request_path = f'live/shortname/{shortname}/overview'
        return self._common_get(request_path)

    def list_live_video_slot(self, shortname):
        """

            :param shortname:
        """
        self.logger.debug(f'Getting all live video slots for [{shortname}]')
        request_path = f'live/shortname/{shortname}/slots'
        return self._common_get(request_path)

    def get_live_video_slot(self, shortname, slot_id):
        """

            :param shortname:
            :param slot_id:
        """
        self.logger.debug(f'Getting live video slot [{slot_id}] for [{shortname}]')
        request_path = f'live/shortname/{shortname}/slots/{slot_id}'
        return self._common_get(request_path)

    def get_live_video_slot_status(self, shortname, slot_id):
        """

            :param shortname:
            :param slot_id:
        """
        self.logger.debug(f'Getting live video slot [{slot_id}] status for [{shortname}]')
        request_path = f'live/shortname/{shortname}/slots/{slot_id}/status'
        return self._common_get(request_path)

    def create_live_video_slot(self, shortname, config):
        """

            :param shortname:
            :param config:
        """
        self.logger.debug(f'Creation live video slots for [{shortname}]')
        request_path = f'live/shortname/{shortname}/slots'
        return self._common_post(request_path, body=config)

    def delete_live_video_slot(self, shortname, slot_id):
        """

            :param shortname:
            :param slot_id:
        """
        self.logger.debug(f'Getting live video slot [{slot_id}] for [{shortname}]')
        request_path = f'live/shortname/{shortname}/slots/{slot_id}'
        return self._common_delete(request_path)

    # -------------------- Video WEBRTC Slots  -------------------- #

    def list_webrtc_video_slot(self, shortname):
        """

            :param shortname:
        """
        self.logger.debug(f'Getting all webrtc video slots for [{shortname}]')
        request_path = f'webrtc/shortname/{shortname}/slots'
        return self._common_get(request_path)

    def get_webrtc_video_slot(self, shortname, slot_id):
        """

            :param shortname:
            :param slot_id:
        """
        self.logger.debug(f'Getting webrtc video slot [{slot_id}] for [{shortname}]')
        request_path = f'webrtc/shortname/{shortname}/slots/{slot_id}'
        return self._common_get(request_path)

    def create_webrtc_video_slot(self, shortname, config):
        """

            :param shortname:
            :param config:
        """
        self.logger.debug(f'Creating webrtc video slots for [{shortname}]')
        request_path = f'webrtc/shortname/{shortname}/slots'
        return self._common_post(request_path, body=config)

    def delete_webrtc_video_slot(self, shortname, slot_id):
        """

            :param shortname:
            :param slot_id:
        """
        self.logger.debug(f'Deleting webrtc video slot [{slot_id}] for [{shortname}]')
        request_path = f'webrtc/shortname/{shortname}/slots/{slot_id}'
        return self._common_delete(request_path)
