#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['_deliver_service_instance_template', '_protocol_set_template']

_deliver_service_instance_template = {
    "body": {"serviceKey": {"name": "delivery"},
             "publishedHostname": "",
             "sourceHostname": "",
             "publishedUrlPath": "",
             "sourceUrlPath": "",
             "serviceProfileName": "",
             "protocolSets": []
             },
    "accounts": [{"shortname": ""}],
}

_protocol_set_template = {"publishedProtocol": "https",
                          "sourceProtocol": "https",
                          "options": []}
