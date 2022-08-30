#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['DeliverServiceInstanceObj']
__docformat__ = 'restructuredtext'

import uuid
import requests
from copy import deepcopy
from ll_sdk.utils.config_api_helper.templates.delivery_template import *


class DeliverServiceInstanceObj(dict):
    """
    Class that help build correct delivery service instance for config-api
    """

    __protocol_set_fields = {"published_protocol": "publishedProtocol",
                             "source_protocol": "sourceProtocol",
                             "published_port": "publishedPort",
                             "source_port": "sourcePort",
                             "options": "options"}

    def __init__(self):
        super(DeliverServiceInstanceObj).__init__()
        self.clear_obj()

    def _gen_rewrite_hosts(self):
        rewrite_uuid = str(uuid.uuid4())
        published_url = 'test-%s.pub.host.com' % rewrite_uuid
        source_url = 'test-%s.origin.host.com' % rewrite_uuid
        return published_url, source_url

    def clear_obj(self):
        """
        Clear all field values
        """
        self.clear()
        self._temp = deepcopy(_deliver_service_instance_template)
        self._protocol_set_temp = deepcopy(_protocol_set_template)

    def _set_base(self, **kwargs):
        """
        Set the base values of an object
        """
        for option, value in list(kwargs.items()):
            self[option] = value

    def _set_delivery_svc_instance(self, **kwargs):
        """
        Set the delivery svc values of an object
        :Parameters
            - serviceKey
            - publishedHostname
            - sourceHostname
            - publishedUrlPath
            - sourceUrlPath
            - serviceProfileName
            - serviceProfileRelativePath
            - protocolSets
            - uuid
        """
        _allowed_opts = ['serviceKey',
                         'publishedHostname',
                         'sourceHostname',
                         'publishedUrlPath',
                         'sourceUrlPath',
                         'serviceProfileName',
                         'serviceProfileRelativePath',
                         'protocolSets',
                         'uuid']

        for option, value in list(kwargs.items()):
            if option in _allowed_opts:
                self["body"][option] = value
            else:
                raise KeyError("Provided option is not supported [{0}]".format(option))

    def generate_default(self, shortname, published_host=None, source_host=None, profile_name=None,
                         published_protocol=None, source_protocol=None):
        """
        Generate an delivery service instance object populated with default values
        """
        self.clear_obj()
        self._set_base(**self._temp)
        if source_host is not None:
            self['body']['sourceHostname'] = source_host
        else:
            _, self['body']['sourceHostname'] = self._gen_rewrite_hosts()

        if published_host is not None:
            self['body']['publishedHostname'] = published_host
        else:
            self['body']['publishedHostname'], _ = self._gen_rewrite_hosts()
        if profile_name is not None:
            self.profile_name = profile_name
        self.shortname = shortname

        if bool(published_protocol) ^ bool(source_protocol):
            raise DeliverInstanceBaseException(
                '{} {} both should be with or without value'.format(published_protocol, source_protocol))
        if not isinstance(published_protocol, list):
            published_protocol = [published_protocol]
        if not isinstance(source_protocol, list):
            source_protocol = [source_protocol]
        for p, s in zip(published_protocol, source_protocol):
            self.add_protocol_set(published_protocol=p, source_protocol=s)

    # --- Protocol Set ---
    def _get_protocol_idx(self, published_protocol, source_protocol):

        protocol_sets_list = deepcopy(self['body']['protocolSets'])
        protocol_idx = next((i for i, value in enumerate(protocol_sets_list) if
                             (value['publishedProtocol'] == published_protocol and
                              value['sourceProtocol'] == source_protocol)), None)
        # if protocol_idx is False:
        #     raise DeliverInstanceBaseException("Protocol not found")
        return protocol_idx

    def clear_protocol_set(self, published_protocol=None, source_protocol=None):
        """
        Remove particular protocol set.
        If pub_protocol and source_protocol not present - clear all
        """
        if bool(source_protocol) ^ bool(published_protocol):
            raise DeliverInstanceBaseException("both pub_protocol and source_protocol should have value "
                                               "or both shouldn't: {}, {}".format(source_protocol, published_protocol))
        if published_protocol and source_protocol:
            protocol_idx = self._get_protocol_idx(published_protocol, source_protocol)
            del self['body']['protocolSets'][protocol_idx]
        else:
            self['body']['protocolSets'] = []

    def add_protocol_set(self, published_protocol='https', source_protocol='https',
                         published_port=None, source_port=None, options=None):
        """
        Add one protocol set.
        """
        protocol_set = deepcopy(self._protocol_set_temp)
        for arg, kwarg in locals().items():
            if arg in self.__protocol_set_fields and kwarg:
                protocol_set[self.__protocol_set_fields[arg]] = kwarg
        if len(self['body']['protocolSets']) < 2:
            self['body']['protocolSets'].append(protocol_set)

    def modify_protocol_set(self, published_protocol, source_protocol,
                            published_port=None, source_port=None, options=None):
        """
        Update protocol set values

        :param published_protocol:
        :param source_protocol:
        :param published_port:
        :param source_port:
        :param options:
        :return:
        """

        protocol_idx = self._get_protocol_idx(published_protocol, source_protocol)
        for arg, kwarg in locals().items():
            if arg in self.__protocol_set_fields and kwarg:
                self["body"]['protocolSets'][protocol_idx][self.__protocol_set_fields[arg]] = kwarg

    # --- Options ---
    def _get_option_idx(self, option_name, options):
        option_idx = next((i for i, item in enumerate(options) if item["name"] == option_name), False)
        if option_idx is False:
            raise DeliverInstanceBaseException('Option [{}] not present in Option Array [{}]'.format(option_name, options))
        return option_idx

    def _modify_option_object_scope(self, option_name, option_parameters, published_protocol, source_protocol,
                                    func):

        protocol_sets_list = self['body']['protocolSets']
        protocol_idx = self._get_protocol_idx(published_protocol, source_protocol)
        if protocol_idx is None:
            for protocol_set in protocol_sets_list:
                func(option_name, option_parameters, protocol_set)
        else:
            protocol_set = protocol_sets_list[protocol_idx]
            func(option_name, option_parameters, protocol_set)

    def _add_option_protocol_sets_scope(self, option_name, option_parameters, protocol_set):
        _option_object = self._prepare_option_object(option_name, option_parameters)
        option_object = deepcopy(_option_object)
        protocol_set['options'].append(option_object)

    def _modify_option_protocol_sets_scope(self, option_name, option_parameters, protocol_set):
        option_idx = self._get_option_idx(option_name, protocol_set['options'])
        if option_idx is not False:
            protocol_set['options'][option_idx]['parameters'] = option_parameters

    def _delete_option_protocol_sets_scope(self, option_name, option_parameters, protocol_set):
        option_idx = self._get_option_idx(option_name, protocol_set['options'])
        if option_idx is not False:
            del protocol_set['options'][option_idx]

    def _prepare_option_object(self, option_name, option_parameters):

        if option_parameters is None:
            parameters = []
        elif option_parameters and not isinstance(option_parameters, list):
            parameters = [option_parameters]
        else:
            parameters = option_parameters
        option_object = {'name': option_name, "parameters": parameters}

        return option_object

    def add_option(self, option_name, option_parameters=None, published_protocol=None, source_protocol=None, ):
        """

        :param option_name:
        :param option_parameters:
        :param published_protocol:
        :param source_protocol:
        :return:
        """
        self._modify_option_object_scope(option_name, option_parameters, published_protocol,
                                         source_protocol, self._add_option_protocol_sets_scope)

    def modify_options(self, option_name, option_parameters, published_protocol=None, source_protocol=None):
        """
        Modify option parameters. Only parameters.
        :param published_protocol:
        :param source_protocol:
        :param option_name:
        :param option_parameters:
        :return:
        """
        self._modify_option_object_scope(option_name, option_parameters, published_protocol,
                                         source_protocol, self._modify_option_protocol_sets_scope)

    def remove_option(self, option_name, published_protocol=None, source_protocol=None):
        """
        Remove option to specific protocol set.
        None: remove 1st option occurrence. For multi option please execute this method few times.
        :param published_protocol:
        :param source_protocol:
        :param option_name:
        :return:
        """
        option_parameters = None
        self._modify_option_object_scope(option_name, option_parameters, published_protocol,
                                         source_protocol, self._delete_option_protocol_sets_scope)

    # --- Other ---
    def process_response(self, response):
        """
        Transform json response from config-api.get_delivery_service_instance to DeliverServiceInstanceObj
        :param response: json or requests.models.Response
        :return:
        """

        if isinstance(response, requests.models.Response):
            response = response.json()
        del response['revision']
        del response['shortname']
        del response['status']
        self._set_base(**response)

    # --- Property ---
    @property
    def profile_name(self):
        return self['body']['serviceProfileName']

    @profile_name.setter
    def profile_name(self, profile_name):
        self['body']['serviceProfileName'] = profile_name

    @property
    def shortname(self):
        return self['accounts'][0]['shortname']

    @shortname.setter
    def shortname(self, shortname):
        self['accounts'][0]['shortname'] = shortname


class DeliverInstanceBaseException(BaseException):
    __module__ = 'builtins'
    pass
