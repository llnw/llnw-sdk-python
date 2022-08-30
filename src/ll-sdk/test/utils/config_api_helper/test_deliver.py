#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from ll-sdk.utils.config_api_helper.deilver import DeliverServiceInstanceObj, DeliverInstanceBaseException

shortname = "testname"
published_host = "www.example.com"
source_host = "www.example.origin.com"
published_protocol = "https"
source_protocol = "http"
profile_name = "Test_profile"


@pytest.fixture(scope="function")
def delivery_svc_instance():
    """Fixture for generating default DeliveryServiceInstance object"""
    inst = DeliverServiceInstanceObj()
    inst.generate_default(shortname, published_host, source_host,
                          profile_name, published_protocol, source_protocol)
    return inst


@pytest.fixture(scope="function")
def add_protocol_set(delivery_svc_instance):
    """Fixture for adding protocolSet to DeliveryServiceInstance object"""
    delivery_svc_instance.add_protocol_set()


@pytest.fixture(scope="function")
def add_option(delivery_svc_instance):
    """Fixture for adding option to DeliveryServiceInstance object"""
    delivery_svc_instance.add_option("some_opt", option_parameters=["some_param"],
                                     published_protocol=published_protocol, source_protocol=source_protocol)


def test_generate_default():
    """Test: Generate default Delivery Service Instance object

    Steps:
    1. Generate default DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is generated as expected
    """
    expected = {"accounts": [{"shortname": shortname}],
                "body": {"protocolSets": [{"options": [],
                                           "publishedProtocol": published_protocol,
                                           "sourceProtocol": source_protocol}],
                         "publishedHostname": published_host,
                         "publishedUrlPath": "",
                         "serviceKey": {"name": "delivery"},
                         "serviceProfileName": profile_name,
                         "sourceHostname": source_host,
                         "sourceUrlPath": ""}}
    delivery_svc_inst = DeliverServiceInstanceObj()
    delivery_svc_inst.generate_default(shortname, published_host, source_host,
                                       profile_name, published_protocol, source_protocol)
    assert expected == delivery_svc_inst


@pytest.mark.parametrize('pub,source', [(None, None), (published_protocol, source_protocol)])
def test_clear_protocol_set(delivery_svc_instance, pub, source):
    """Test: Clear protocolSets in Delivery Service Instance object

    Steps:
    1. Clear protocolSets in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.clear_protocol_set(published_protocol=pub, source_protocol=source)
    assert not delivery_svc_instance["body"]["protocolSets"]


@pytest.mark.parametrize('pub,source', [(published_protocol, None), (None, source_protocol)])
def test_neg_clear_protocol_set(delivery_svc_instance, pub, source):
    """Test: Clear protocolSets with exception in Delivery Service Instance object

    Steps:
    1. Clear protocolSets, do not set either published or source protocol
    2. Check raised exception

    Result:
    OK: exception is raised
    """
    with pytest.raises(DeliverInstanceBaseException):
        delivery_svc_instance.clear_protocol_set(published_protocol=pub, source_protocol=source)


def test_add_protocol_set(delivery_svc_instance):
    """Test: Add protocolSet to Delivery Service Instance object

    Steps:
    1. Add additional protocolSet to DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.add_protocol_set(published_protocol="http", source_protocol="http",
                                           published_port=80, source_port=8080,
                                           options=[{"name": "some_opt", "parameters": ["some_param"]}])
    assert 2 == len(delivery_svc_instance["body"]["protocolSets"])
    prot_set = {"publishedProtocol": "http",
                "sourceProtocol": "http",
                "publishedPort": 80,
                "sourcePort": 8080,
                "options": [{"name": "some_opt", "parameters": ["some_param"]}]}
    assert prot_set == delivery_svc_instance["body"]["protocolSets"][1]


def test_add_more_protocol_set_than_allowed(delivery_svc_instance, add_protocol_set):
    """Test: Add more protocolSets than allowed to Delivery Service Instance object

    Steps:
    1. Add 2 additional protocolSets to DeliverySvcInstance object
    2. Check that only 2 protocolSets are present in generated object

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.add_protocol_set(published_protocol="http", source_protocol="http",
                                           published_port=80, source_port=8080,
                                           options=[{"name": "some_opt", "parameters": ["some_param"]}])
    assert 2 == len(delivery_svc_instance["body"]["protocolSets"])


def test_modify_protocol_set(delivery_svc_instance):
    """Test: Modify protocolSet in Delivery Service Instance object

    Steps:
    1. Modify protocolSet in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.modify_protocol_set(published_protocol=published_protocol, source_protocol=source_protocol,
                                              options=[{"name": "some_opt", "parameters": ["some_param"]}])
    assert 1 == len(delivery_svc_instance["body"]["protocolSets"])
    prot_set = {"publishedProtocol": published_protocol,
                "sourceProtocol": source_protocol,
                "options": [{"name": "some_opt", "parameters": ["some_param"]}]}
    assert prot_set == delivery_svc_instance["body"]["protocolSets"][0]


def test_add_option(delivery_svc_instance):
    """Test: Add option to protocolSet in Delivery Service Instance object

    Steps:
    1. Add option to protocolSet in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.add_option("some_opt", option_parameters=["some_param", 3],
                                     published_protocol=published_protocol, source_protocol=source_protocol)
    assert 1 == len(delivery_svc_instance["body"]["protocolSets"])
    prot_set = {"publishedProtocol": published_protocol,
                "sourceProtocol": source_protocol,
                "options": [{"name": "some_opt", "parameters": ["some_param", 3]}]}
    assert prot_set == delivery_svc_instance["body"]["protocolSets"][0]


def test_add_option_all_protocol_sets(delivery_svc_instance, add_protocol_set):
    """Test: Add option to all protocolSets in Delivery Service Instance object

    Steps:
    1. Add option to all protocolSets in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.add_option("some_opt", option_parameters=["some_param", 3])
    assert 2 == len(delivery_svc_instance["body"]["protocolSets"])
    option = [{"name": "some_opt", "parameters": ["some_param", 3]}]
    for protocol_set in delivery_svc_instance["body"]["protocolSets"]:
        assert option == protocol_set["options"]


def test_modify_options(delivery_svc_instance, add_option):
    """Test: Modify option in protocolSet in Delivery Service Instance object

    Steps:
    1. Modify option in protocolSet in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.modify_options("some_opt", ["upd_param"], published_protocol, source_protocol)
    prot_set = {"publishedProtocol": published_protocol,
                "sourceProtocol": source_protocol,
                "options": [{"name": "some_opt", "parameters": ["upd_param"]}]}
    assert prot_set == delivery_svc_instance["body"]["protocolSets"][0]


def test_modify_options_all_protocol_sets(delivery_svc_instance, add_protocol_set):
    """Test: Modify option in all protocolSets in Delivery Service Instance object

    Steps:
    1. Modify option in all protocolSets in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.add_option("some_opt", option_parameters=["some_param"])
    delivery_svc_instance.modify_options("some_opt", ["upd_param"])
    option = [{"name": "some_opt", "parameters": ["upd_param"]}]
    for protocol_set in delivery_svc_instance["body"]["protocolSets"]:
        assert option == protocol_set["options"]


def test_remove_option(delivery_svc_instance, add_option):
    """Test: Remove option from protocolSet in Delivery Service Instance object

    Steps:
    1. Remove option from protocolSet in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.remove_option("some_opt", published_protocol, source_protocol)
    prot_set = {"publishedProtocol": published_protocol,
                "sourceProtocol": source_protocol,
                "options": []}
    assert prot_set == delivery_svc_instance["body"]["protocolSets"][0]


def test_remove_options_all_protocol_sets(delivery_svc_instance, add_protocol_set):
    """Test: Remove option from all protocolSets in Delivery Service Instance object

    Steps:
    1. Remove option from all protocolSets in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    delivery_svc_instance.add_option("some_opt", option_parameters=["some_param"])
    delivery_svc_instance.remove_option("some_opt")
    for protocol_set in delivery_svc_instance["body"]["protocolSets"]:
        assert [] == protocol_set["options"]


@pytest.mark.parametrize('field', ['revision', 'status', 'shortname'])
def test_process_response(delivery_svc_instance, field):
    """Test: Convert API response to Delivery Service Instance object

    Steps:
    1. Transform API response to DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is generated as expected
    """
    api_response = {"uuid": "78df6c87-b19f-42cb-bee7-263ec58e3950",
                    "isLatest": True,
                    "isEnabled": True,
                    "revision": {"createdBy": "test_user",
                                 "createdDate": 1530022531900,
                                 "versionNumber": 3},
                    "meta": {"manifestVersion": "4",
                             "serviceIdentifier": "deliverysvcinst",
                             "serviceKey": "delivery"},
                    "status": {"state": "COMPLETED"},
                    "accounts": [{"shortname": shortname}],
                    "shortname": shortname,
                    "body": {"protocolSets": [{"publishedProtocol": published_protocol,
                                               "sourceProtocol": source_protocol,
                                               "options": [{"name": "req_send_header",
                                                            "parameters": ["X-CDN", "llnw"]}]}],
                             "serviceProfileName": profile_name,
                             "publishedHostname": published_host,
                             "sourceHostname": source_host,
                             "publishedUrlPath": "/",
                             "sourceUrlPath": "/",
                             "serviceKey": {"name": "delivery"}}}
    delivery_svc_instance.process_response(api_response)
    assert field not in delivery_svc_instance


def test_profile_name(delivery_svc_instance):
    """Test: Set Profile's name in Delivery Service Instance object

    Steps:
    1. Set profile's name in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    upd_profile_name = "Test_profile_upd"
    delivery_svc_instance.profile_name = upd_profile_name
    assert upd_profile_name == delivery_svc_instance["body"]["serviceProfileName"]
    assert delivery_svc_instance.profile_name == delivery_svc_instance["body"]["serviceProfileName"]


def test_shortname(delivery_svc_instance):
    """Test: Set shortname in Delivery Service Instance object

    Steps:
    1. Set shortname in DeliverySvcInstance object
    2. Compare expected result with actual

    Result:
    OK: deliverysvcinst object is updated as expected
    """
    upd_shortname = "updshortname"
    delivery_svc_instance.shortname = upd_shortname
    assert upd_shortname == delivery_svc_instance["accounts"][0]["shortname"]
    assert delivery_svc_instance.shortname == delivery_svc_instance["accounts"][0]["shortname"]
