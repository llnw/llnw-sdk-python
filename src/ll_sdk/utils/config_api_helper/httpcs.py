#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['HttpCsServiceInstanceObj']
__docformat__ = 'restructuredtext'

import uuid
import requests
from itertools import product
from copy import deepcopy
from sdk.utils.config_api_helper.templates.httpcs_template import *


class HttpCsServiceInstanceObj(dict):
    """
    Class that helps build correct httpcs service instance for config-api
    """
    _supported_video_formats = ['hls', 'hds', 'mss', 'dash']
    _rewrite_types = ['manifest', 'chunk']
    __protocol_set_fields = {"published_protocol": "publishedProtocol",
                             "source_protocol": "sourceProtocol",
                             "published_port": "publishedPort",
                             "source_port": "sourcePort",
                             "options": "options"}

    def __init__(self):
        super(HttpCsServiceInstanceObj).__init__()
        self.clear_obj()

    def _gen_rewrite_hosts(self):
        rewrite_uuid = str(uuid.uuid4())
        published_url = 'test-%s.pub.host.com' % rewrite_uuid
        source_url = 'test-%s.origin.host.com' % rewrite_uuid
        return published_url, source_url

    def clear_obj(self):
        """
        Clear all fields value
        """
        self.clear()
        self._temp = deepcopy(_http_cs_service_instance_template)
        self._protocol_set_temp = deepcopy(_protocol_set_temp)
        self._child_temp = deepcopy(_child_temp)
        self['body'] = {}
        self['body']['httpcsSvcInstance'] = {}
        self['body']['httpcsSvcInstance']['protocolSets'] = []
        self['body']['childHttpcsSvcInstances'] = []
        self['body']['httpcsSvcInstance']['revision'] = {}

    def set_base(self, **kwargs):
        """
        Set the base values of an object
        """
        for option, value in list(kwargs.items()):
            _value = deepcopy(value)
            self[option] = _value

    def _gen_child(self, video_format, rewrite_type):
        # required_fields = ["serviceKey", "protocolSets", "publishedUrlPath", "sourceUrlPath"]
        child_temp = deepcopy(_child_temp)
        child_temp['description'] = 'Generated by LLNW-SDK child {} - {}'.format(video_format, rewrite_type)
        child_temp['serviceKey'] = {"name": "httpcs",
                                    "videoFormat": video_format,
                                    "rewriteType": rewrite_type}
        return child_temp

    def generate_default(self, shortname, video_formats, published_host=None, source_host=None, profile_name=None,
                         published_protocol=None, source_protocol=None):
        """
        Generate an HTTPCS object
        """
        self.clear_obj()
        self.set_base(**self._temp)
        self.shortname = shortname

        if source_host is not None:
            self['body']['httpcsSvcInstance']['sourceHostname'] = source_host
        else:
            _, self['body']['httpcsSvcInstance']['sourceHostname'] = self._gen_rewrite_hosts()

        if published_host is not None:
            self['body']['httpcsSvcInstance']['publishedHostname'] = published_host
        else:
            self['body']['httpcsSvcInstance']['publishedHostname'], _ = self._gen_rewrite_hosts()

        if profile_name is not None:
            self.profile_name = profile_name

        if not isinstance(video_formats, list):
            video_formats = [video_formats]
        if not set(video_formats).issubset(self._supported_video_formats):
            raise HttpCsSvcInstanceBaseException('Supported video formats is {}'.format(self._supported_video_formats))
        for video_format, rewrite_type in product(video_formats, self._rewrite_types):
            child_temp = self._gen_child(video_format, rewrite_type)
            self['body']['childHttpcsSvcInstances'].append(child_temp)

        if bool(published_protocol) ^ bool(source_protocol):
            raise HttpCsSvcInstanceBaseException(
                '{} {} both should be with or without value'.format(published_protocol, source_protocol))
        if not isinstance(published_protocol, list):
            published_protocol = [published_protocol]
        if not isinstance(source_protocol, list):
            source_protocol = [source_protocol]
        for p, s in zip(published_protocol, source_protocol):
            self.add_protocol_set_all(published_protocol=p, source_protocol=s)

    # --- Full Instances ---

    def _get_shild_idx(self, video_formats, rewrite_type):

        idx = next((i for i, v in enumerate(self['body']['childHttpcsSvcInstances']) if
                    v['serviceKey']['videoFormat'] == video_formats and v['serviceKey']['rewriteType'] == rewrite_type),
                   False)

        if idx is False:
            raise HttpCsSvcInstanceBaseException(
                'Provided formats {}, {} not present'.format(video_formats, rewrite_type))
        return idx

    def _set_root_instance(self, **kwargs):
        """
        Set the base values of an HTTP CS instance
        """
        _allowed_opts = ['sourceHostname',
                         'serviceProfileName',
                         'protocolSets',
                         'sourceUrlPath',
                         'publishedUrlPath',
                         'publishedHostname']

        for option, value in list(kwargs.items()):
            if option not in _allowed_opts:
                raise HttpCsSvcInstanceBaseException('{} not in allowed options {}'.format(option, _allowed_opts))
            self['body']["httpcsSvcInstance"][option] = value

    def _set_child_instance(self, child_idx=None, video_formats=None, rewrite_type=None, **kwargs):
        """
        Set the Child instance values of an object
        """
        _allowed_opts = ['publishedUrlPath',
                         'sourceUrlPath',
                         'protocolSets']

        self._check_child_req(child_idx, video_formats, rewrite_type)
        # if not any([child_idx, all([video_formats, rewrite_type])]):
        #     raise HttpCsSvcInstanceBaseException('child_idx or video_formats and rewriteType MUST be provided')

        if child_idx is None:
            child_idx = self._get_shild_idx(video_formats, rewrite_type)

        for option, value in list(kwargs.items()):
            if option not in _allowed_opts:
                raise HttpCsSvcInstanceBaseException('{} not in allowed options {}'.format(option, _allowed_opts))
            self['body']["childHttpcsSvcInstances"][child_idx][option] = value

    # --- Protocol Set ---
    def _check_child_req(self, child_idx, video_formats, rewrite_type):
        if not any([child_idx, all([video_formats, rewrite_type])]):
            raise HttpCsSvcInstanceBaseException('child_idx or video_formats and rewriteType MUST be provided')

    def _gen_protocol_set(self, **kwargs):
        protocol_set = deepcopy(self._protocol_set_temp)

        for arg, kwarg in kwargs.items():
            if arg in self.__protocol_set_fields and kwarg:
                option = deepcopy(kwarg)
                protocol_set[self.__protocol_set_fields[arg]] = option

        return protocol_set

    def _check_child_idx_new(self, child_idx, video_formats, rewrite_type):

        if bool(video_formats) ^ bool(rewrite_type):
            raise HttpCsSvcInstanceBaseException(
                "video_formats: [{}], rewrite_type: [{}] should be with or without value"
                "".format(video_formats, rewrite_type))
        if child_idx is None:
            if all([video_formats, rewrite_type]):
                child_idx = self._get_shild_idx(video_formats, rewrite_type)

        return child_idx

    def _get_protocol_idx(self, published_protocol, source_protocol, protocol_sets_list):

        protocol_idx = None
        if bool(published_protocol) ^ bool(source_protocol):
            raise HttpCsSvcInstanceBaseException(
                "published_protocol: [{}], source_protocol: [{}] shouuld be with or without value"
                "".format(published_protocol, source_protocol))
        if published_protocol is not None and source_protocol is not None:
            protocol_idx = next((i for i, value in enumerate(protocol_sets_list) if
                                 (value['publishedProtocol'] == published_protocol and
                                  value['sourceProtocol'] == source_protocol)), False)
            if protocol_idx is False:
                raise HttpCsSvcInstanceBaseException("Protocol not found")
        return protocol_idx

    def add_protocol_set_all(self, published_protocol='https', source_protocol='https',
                             published_port=None, source_port=None, options=None):
        """
        Add one protocol set to root and all child instances
        """

        protocol_set = self._gen_protocol_set(published_protocol=published_protocol, source_protocol=source_protocol,
                                              published_port=published_port, source_port=source_port, options=options)
        if len(self['body']['httpcsSvcInstance']['protocolSets']) < 2:
            # Root
            root_protoco_set = deepcopy(protocol_set)
            self['body']['httpcsSvcInstance']['protocolSets'].append(root_protoco_set)
            # Children
            for childInstance in self['body']['childHttpcsSvcInstances']:
                child_protoco_set = deepcopy(protocol_set)
                childInstance['protocolSets'].append(child_protoco_set)

    def clear_root_protocol_sets(self):
        """
        Clear root protocol sets
        """
        self['body']["httpcsSvcInstance"]["protocolSets"] = []

    def clear_child_protocol_sets(self, child_idx=None, video_formats=None, rewrite_type=None):
        """
        Clear all child protocol sets or specific one.
        """
        child_idx = self._check_child_idx_new(child_idx, video_formats, rewrite_type)
        if child_idx is not None:
            self['body']["childHttpcsSvcInstances"][child_idx]["protocolSets"] = []
        else:
            for child in self['body']["childHttpcsSvcInstances"]:
                child["protocolSets"] = []

    def add_root_protocol_set(self, published_protocol='https', source_protocol='https',
                              published_port=None, source_port=None, options=None):
        """
        Add protocol set into root instance
        """

        protocol_set = self._gen_protocol_set(published_protocol=published_protocol, source_protocol=source_protocol,
                                              published_port=published_port, source_port=source_port, options=options)

        if len(self['body']["httpcsSvcInstance"]["protocolSets"]) < 2:
            self['body']["httpcsSvcInstance"]["protocolSets"].append(protocol_set)
        else:
            msg = "httpcsSvcInstance protocolSets is more than 2"
            raise HttpCsSvcInstanceBaseException(msg)

    def add_child_protocol_set(self, published_protocol, source_protocol,
                               child_idx=None, video_formats=None, rewrite_type=None,
                               published_port=None, source_port=None, options=None):
        """
        Add protocol set into child instance, if child_idx provided use specific instance otherwise all.
        """

        child_idx = self._check_child_idx_new(child_idx, video_formats, rewrite_type)
        protocol_set = self._gen_protocol_set(published_protocol=published_protocol, source_protocol=source_protocol,
                                              published_port=published_port, source_port=source_port, options=options)
        if child_idx is not None:
            self['body']["childHttpcsSvcInstances"][child_idx]["protocolSets"].append(protocol_set)
        else:
            for child in self['body']["childHttpcsSvcInstances"]:
                _protocol_set = deepcopy(protocol_set)
                child["protocolSets"].append(_protocol_set)

    def modify_root_protocol_set(self, published_protocol, source_protocol,
                                 published_port=None, source_port=None, options=None):
        """
        Modify root protocol set

        :param published_protocol:
        :param source_protocol:
        :param published_port: (optional)
        :param source_port: (optional)
        :param options: (optional)
        """
        protocol_sets_list = self['body']["httpcsSvcInstance"]["protocolSets"]
        protocol_idx = self._get_protocol_idx(published_protocol, source_protocol, protocol_sets_list)
        for arg, kwarg in locals().items():
            if arg in self.__protocol_set_fields and kwarg:
                self["body"]["httpcsSvcInstance"]['protocolSets'][protocol_idx][self.__protocol_set_fields[arg]] = kwarg

    def modify_child_protocol_set(self, published_protocol, source_protocol,
                                  child_idx=None, video_formats=None, rewrite_type=None,
                                  published_port=None, source_port=None, options=None):
        """
        Modify root protocol set

        :param published_protocol:
        :param source_protocol:
        :param child_idx:
        :param video_formats:
        :param rewrite_type:
        :param published_port: (optional)
        :param source_port: (optional)
        :param options: (optional)
        :return:
        """
        self._check_child_req(child_idx, video_formats, rewrite_type)
        if child_idx is None:
            child_idx = self._get_shild_idx(video_formats, rewrite_type)
        protocol_sets_list = self['body']["childHttpcsSvcInstances"][child_idx]["protocolSets"]
        protocol_idx = self._get_protocol_idx(published_protocol, source_protocol, protocol_sets_list)
        for arg, kwarg in locals().items():
            if arg in self.__protocol_set_fields and kwarg:
                self["body"]["childHttpcsSvcInstances"][child_idx]['protocolSets'][protocol_idx][
                    self.__protocol_set_fields[arg]] = kwarg

    # --- Options root ---
    def _get_option_idx(self, option_name, options):
        option_idx = next((i for i, item in enumerate(options) if item["name"] == option_name), False)
        return option_idx

    def _prepare_option_object(self, option_name, option_parameters):

        if option_parameters is None:
            parameters = []
        elif option_parameters and not isinstance(option_parameters, list):
            parameters = [option_parameters]
        else:
            parameters = option_parameters
        option_object = {'name': option_name, "parameters": parameters}

        return option_object

    def _modify_option_object_scope(self, option_name, option_parameters, published_protocol, source_protocol,
                                    protocol_sets_list, func):

        # protocol_sets_list = child["protocolSets"]
        protocol_idx = self._get_protocol_idx(published_protocol, source_protocol, protocol_sets_list)
        if protocol_idx is None:
            for protocol_set in protocol_sets_list:
                func(option_name, option_parameters, protocol_set)
        else:
            protocol_set = protocol_sets_list[protocol_idx]
            func(option_name, option_parameters, protocol_set)

    def _modify_option_protocol_sets_scope(self, option_name, option_parameters, protocol_set):
        option_idx = self._get_option_idx(option_name, protocol_set['options'])
        if option_idx is not False:
            protocol_set['options'][option_idx]['parameters'] = option_parameters

    def _delete_option_protocol_sets_scope(self, option_name, option_parameters, protocol_set):
        option_idx = self._get_option_idx(option_name, protocol_set['options'])
        if option_idx is not False:
            del protocol_set['options'][option_idx]

    def _add_option_protocol_sets_scope(self, option_name, option_parameters, protocol_set):
        _option_object = self._prepare_option_object(option_name, option_parameters)
        option_object = deepcopy(_option_object)
        protocol_set['options'].append(option_object)

    def _tmp_child_option_operation(self, option_name, option_parameters, published_protocol, source_protocol,
                                    child_idx, video_formats, rewrite_type, func):

        child_idx = self._check_child_idx_new(child_idx, video_formats, rewrite_type)
        if child_idx is None:
            for child in self['body']["childHttpcsSvcInstances"]:
                protocol_sets_list = child["protocolSets"]
                self._modify_option_object_scope(option_name, option_parameters, published_protocol,
                                                 source_protocol, protocol_sets_list, func)
        else:
            protocol_sets_list = self['body']["childHttpcsSvcInstances"][child_idx]["protocolSets"]
            self._modify_option_object_scope(option_name, option_parameters, published_protocol, source_protocol,
                                             protocol_sets_list, func)

    def add_root_option(self, option_name, option_parameters=None, published_protocol=None, source_protocol=None):
        """
        Add option to ROOT protocol set
        :param option_name:
        :param published_protocol: (optional)
        :param source_protocol: (optional)
        :param option_parameters: (optional)
        :return:
        """
        protocol_sets_list = self['body']["httpcsSvcInstance"]["protocolSets"]
        self._modify_option_object_scope(option_name, option_parameters, published_protocol,
                                         source_protocol, protocol_sets_list, self._add_option_protocol_sets_scope)

    def modify_root_options(self, option_name, option_parameters, published_protocol=None, source_protocol=None):
        """
        Modify option parameters. Only parameters.
        :param option_name:
        :param option_parameters:
        :param published_protocol: (optional)
        :param source_protocol:  (optional)
        :return:
        """

        protocol_sets_list = self['body']["httpcsSvcInstance"]["protocolSets"]
        self._modify_option_object_scope(option_name, option_parameters, published_protocol, source_protocol,
                                         protocol_sets_list, self._modify_option_protocol_sets_scope)

    def remove_root_option(self, option_name, published_protocol=None, source_protocol=None):
        """
        Remove option to specific protocol set.
        None: remove 1st option occurrence. For multi option please execute this method few times.
        :param option_name:
        :param published_protocol: (optional)
        :param source_protocol: (optional)
        :return:
        """
        option_parameters = None
        protocol_sets_list = self['body']["httpcsSvcInstance"]["protocolSets"]
        self._modify_option_object_scope(option_name, option_parameters, published_protocol, source_protocol,
                                         protocol_sets_list, self._delete_option_protocol_sets_scope)

    # --- Options child ---
    def add_child_option(self, option_name, option_parameters=None,
                         published_protocol=None, source_protocol=None,
                         child_idx=None, video_formats=None, rewrite_type=None):
        """
        Add option to child, to all child, to specific child, to specific protocol set in child

        :param option_name:
        :param option_parameters: (optional)
        :param published_protocol: (optional)
        :param source_protocol: (optional)
        :param child_idx: (optional)
        :param video_formats: (optional)
        :param rewrite_type: (optional)
        :return:
        """

        self._tmp_child_option_operation(option_name, option_parameters, published_protocol, source_protocol,
                                         child_idx, video_formats, rewrite_type, self._add_option_protocol_sets_scope)

    def modify_child_options(self, option_name, option_parameters,
                             published_protocol=None, source_protocol=None,
                             child_idx=None, video_formats=None, rewrite_type=None):
        """
        Modify option parameters. Only option parameters.
        In particular child option set or
        in all options sets in some child or
        in all options sets in all child where provided option exists
        :param option_name:
        :param option_parameters:
        :param published_protocol: (optional)
        :param source_protocol: (optional)
        :param child_idx: (optional)
        :param video_formats: (optional)
        :param rewrite_type: (optional)

        """
        if not isinstance(option_parameters, list):
            option_parameters = [option_parameters]
        self._tmp_child_option_operation(option_name, option_parameters, published_protocol, source_protocol,
                                         child_idx, video_formats, rewrite_type,
                                         self._modify_option_protocol_sets_scope)

    def delete_child_option(self, option_name,
                            published_protocol=None, source_protocol=None,
                            child_idx=None, video_formats=None, rewrite_type=None):
        """
        Delete option.
        In particular child option set or
        in all options sets in some child or
        in all options sets in all child where provided option exists
        :param option_name:
        :param published_protocol:
        :param source_protocol:
        :param child_idx:
        :param video_formats:
        :param rewrite_type:
        :return:
        """
        option_parameters = None
        self._tmp_child_option_operation(option_name, option_parameters, published_protocol, source_protocol,
                                         child_idx, video_formats, rewrite_type,
                                         self._delete_option_protocol_sets_scope)

    # --- Others ---
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
        self.set_base(**response)

    # --- Property ---
    @property
    def profile_name(self):
        return self['body']['httpcsSvcInstance']['serviceProfileName']

    @profile_name.setter
    def profile_name(self, profile_name):
        self['body']['httpcsSvcInstance']['serviceProfileName'] = profile_name

    @property
    def shortname(self):
        return self['accounts'][0]['shortname']

    @shortname.setter
    def shortname(self, shortname):
        self['accounts'][0]['shortname'] = shortname


class HttpCsSvcInstanceBaseException(BaseException):
    __module__ = 'builtins'
    pass