#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['SSLCertObj']
__docformat__ = 'restructuredtext'

import uuid
from copy import deepcopy
from sdk.utils.config_api_helper.templates.ssl_cert_template import *


class SSLCertObj(dict):

    def __init__(self):
        self.clear_obj()

    def _set_base(self, **kwargs):
        """
        Set the base values of an object
        """
        for option, value in list(kwargs.items()):
            self[option] = value

    def clear_obj(self):
        """
        Clear all field values
        """
        self.clear()
        self._temp = deepcopy(_ssl_cert_template)

    def generate_default(self, shortname, cert, cert_key, intermediate_certs=None, cert_name=None):
        """
        Generate an SSLCertObj object populated with default values
        """
        self.clear_obj()
        self._set_base(**self._temp)

        self.shortname = shortname
        self.cert = cert
        self.cert_key = cert_key

        if intermediate_certs is not None:
            self.intermediate_certs = intermediate_certs
        if cert_name is None:
            cert_name = 'cert_{0}'.format(uuid.uuid4().urn.split('-')[-1])
        self.cert_name = cert_name

    @property
    def cert_name(self):
        return self['body']['certName']

    @cert_name.setter
    def cert_name(self, cert_name):
        self['body']['certName'] = cert_name

    @property
    def cert(self):
        return self['body']['cert']

    @cert.setter
    def cert(self, cert):
        """
        Set the body.intermediateCerts values
        """
        self['body']['cert'] = cert

    @property
    def cert_key(self):
        return self['body']['certKey']

    @cert_key.setter
    def cert_key(self, cert_key):
        """
        Set the body.intermediateCerts values
        """
        self['body']['certKey'] = cert_key

    @property
    def intermediate_certs(self):
        """
        Get the  body.intermediateCerts values
            Note: it will return value only for processed certificates
        """
        return self['body']['intermediateCerts'] if 'intermediateCerts' in self['body'] else None

    @intermediate_certs.setter
    def intermediate_certs(self, int_certs):
        """
        Set the body.intermediateCerts values
        """
        if isinstance(int_certs, list):
            int_certs = '\n'.join(int_certs)
        self['body']['cert'] += f"\n{int_certs}"

    @property
    def shortname(self):
        return self['accounts'][0]['shortname']

    @shortname.setter
    def shortname(self, shortname):
        self['accounts'][0]['shortname'] = shortname

    @property
    def fingerprint(self):
        return self['body']['fingerprints']

    @fingerprint.setter
    def fingerprint(self, fingerprint):
        if not isinstance(fingerprint, list):
            fingerprint = [fingerprint]
        self['body']['fingerprints'] = fingerprint
